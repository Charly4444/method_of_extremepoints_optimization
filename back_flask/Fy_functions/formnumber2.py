import numpy as np
"""
This program is written to take any Linear Programming problem with 
at least one constrained, and at least one or more unconstrained vars
and search for a solution.
The coefficients of the expressions must be entered in the same order,
Also, User doesnt need to pay attention to the slack coefficients, it is 
automatically handled in the program
"""

# some initial vars
all_constraints = []
A_matrix = []
b_matrix = []
C_Matrix = []


# read in all constraints
def get_constraint(num_orig_vars,constraintsArray):
    all_myconstraints = []
    
    total_vars = num_orig_vars
    # GOING THROUGH TO BUILD THE CONSTRAINTS
    for constraint_parts in constraintsArray:

        constraint = {}
        
        constraint['constraint_coef'] = constraint_parts[:-2]
        constraint['constraint_op'] = constraint_parts[-2]
        constraint['constraint_cons'] = constraint_parts[-1]
        
        # update no of vars
        if constraint_parts[-2] == '<=':
            constraint['slack'] = 1
            total_vars+=1
        elif constraint_parts[-2] == '>=':
            constraint['slack'] = -1
            total_vars+=1
        else:
            constraint['slack'] = 0

        all_myconstraints.append(constraint)
    all_constraints[:] = all_myconstraints
    return total_vars

# build A matrix
def build_Amatrix(num_orig_vars, final_numvars_consr):
    A_matrixofChars = []

    i = 0
    
    for cons in all_constraints:
        if cons['slack']==1 or cons['slack']==-1:
            if i!=0:
                num_zeroes_before = i*[0]
            else:
                num_zeroes_before=''
            sk=[cons['slack']]
            if ((final_numvars_consr - num_orig_vars -1 - i) != 0):
                num_zeroes_after = (final_numvars_consr - num_orig_vars - 1 - i)*[0]
            else:
                num_zeroes_after=''
            i+=1  

        else:
            num_zeroes_before=''
            sk=''
            if ((final_numvars_consr - num_orig_vars) !=0):
                num_zeroes_after = (final_numvars_consr - num_orig_vars)*[0]
            else:
                num_zeroes_after=''
        
        # concatenate and append to A_matrixofChars => that completes the basic cycle
        A_matrixofChars.append(cons['constraint_coef'] + list(map(str, num_zeroes_before)) + list(map(str, sk)) + list(map(str, num_zeroes_after)))
    # print(f"row: {A_matrixofChars}\n")
    
    arrays_of_numbers = [np.array(list(map(float, sublist))) for sublist in A_matrixofChars]
    stacked_Amatrix = np.vstack(arrays_of_numbers)
    return stacked_Amatrix


def build_Bmatrix():
    b_values = [float(cons['constraint_cons']) for cons in all_constraints]
    b_matrix = np.array(b_values)
    return b_matrix


# get terms of the objectuive function
def get_objectivefcn(num_orig_vars):
    objective_part = input(f"Enter the {num_orig_vars} variables of objectiveFunction as 'a1 a2 ... an: ").split()
    return objective_part

def build_Cmatrix(num_orig_vars, final_numvars_consr, objective):
    # take objective
    objective_part = objective

    if ((final_numvars_consr - num_orig_vars) !=0):
        num_zeroes_after = (final_numvars_consr - num_orig_vars)*[0]
    else:
        num_zeroes_after=''
    
    c_valuesChar = objective_part + list(map(str, num_zeroes_after))
#   = = = = =
    c_values = [float(val) for val in c_valuesChar]
    c_matrix = np.array(c_values)
    return c_matrix


# ============================ PART FOR UNCONSTRAINED MODS ==================================
# This part takes care of the unconstrained modifications...
    
# Adjust the A matrix
def adjust_Amatrix(A, index_of_uncons_vars):
    notedpairs=[]
    n=0     #b/c upon each replacement n stretches the matrix
    for i in index_of_uncons_vars:
        orig_coeff = A[:, (i+n)]  # Extract the original coefficient at index i
        
        # Create vectors representing the positive and negative parts of the variable
        new_pos_col = orig_coeff
        new_neg_col = -orig_coeff
        
        # Replace the original column with the positive and negative parts
        A[:, (i+n)] = new_pos_col
        A = np.insert(A, (i+n) + 1, new_neg_col, axis=1)
        
        # make note of the new positions
        notedpairs.append(i+n)
        n+=1

        
    return A,notedpairs
    
# Adjust the C matrix
def adjust_Cmatrix(C, index_of_uncons_vars):
    n=0
    for i in index_of_uncons_vars:
        orig_coeff = C[(i+n)]

        new_pos_col = orig_coeff
        new_neg_col = -orig_coeff
        
        C[(i+n)] = new_pos_col
        C = np.insert(C, (i+n)+1, new_neg_col)  # Add zero coefficients for the new variables
        n+=1
    return C



# ==========================================================================================
# Main program
# this part is valid if I run this file directly from here (ok)
if __name__ == "__main__":
    # no of vars
    num_orig_vars = int(input("Enter the number of original decision variables: "))
    
    # no of constraints
    num_constraints = int(input("Enter the number of constraints: "))
    
    # # no of unconstrained vars
    # num_uncons_vars = int(input("Enter the number of unconstrained vars: "))

    ##E: index pos of unconstrained vars
    input_poss = input("index positions of unconstrained vars, '0 1 ...  ' first variable is index 0: ").split()
    index_of_uncons_vars = list(map(int,input_poss))
    
    for x in index_of_uncons_vars:
        if x not in range(num_orig_vars):
            print('you entered an invalid location for var: first var is pos 0')
            exit()      #premature exit

    

    # get constraint <<cons>>
    final_numvars_consr = get_constraint(num_orig_vars,num_constraints)

    # build A matrix <<cons>>
    A_matrix = build_Amatrix(num_orig_vars, final_numvars_consr)
    print(f"constrained A mtx: {A_matrix}\n")

    # build b_Matrix <<Cons>>
    b_matrix = build_Bmatrix()
    print(f"B: {b_matrix}\n")

    # build C_Matrix / <<this includes getting the objective function>> <<Cons>>
    c_matrix = build_Cmatrix(num_orig_vars, final_numvars_consr)
    print(f"constrained C mtx: {c_matrix}\n")


    # =======================================================================================
    # NOW ADJUST COEFFICIENTS (A & C matrix) FOR UNCONSTRAINED 
    A_matrix,notedindexes = adjust_Amatrix(A_matrix, index_of_uncons_vars)
    print(f"Final A mtx: {A_matrix}\n")

    C_matrix = adjust_Cmatrix(c_matrix, index_of_uncons_vars)
    print(f"Final C mtx: {C_matrix}\n")
# ========================== AESTHETIC CODE JUST TO SHOW THE ELEMENTS=========================
# Not, necessary but just to see which variables are using pairs of any kind
    # print (notedindexes)
    