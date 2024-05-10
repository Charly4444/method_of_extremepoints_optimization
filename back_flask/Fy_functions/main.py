import numpy as np
from Fy_functions import standard_form as sfc
from itertools import combinations
"""
This program will only solve problems where all variables 
x1, x2, ... , xn >= 0
if theres one or more varibles that dont satisfy this, then
use the second solver.
"""
def solve_constrained(lp_data):
    # nature of data recieved => {'numVars': '', 'numConstraints': '', 'constraints': []}
    solutionSet = []
    
    # HELPER FUNCTION
    def check_input(lp_data):
        if lp_data['numVars'] == '' or lp_data['numConstraints'] == '' or lp_data['constraints'] == []:
            print('You cant solve nothing')
            return 0,0,[]
        else:
            if len(lp_data['constraints']) < int(lp_data['numConstraints']):
                print('Incomplete constraints')
                return 0,0,[]
            else:
                num_orig_vars = int(lp_data['numVars'])
                num_constraints = int(lp_data['numConstraints'])
                constraintsArray = lp_data['constraints']
                objective = lp_data['objective']
                return num_orig_vars, num_constraints, constraintsArray, objective
    
    # INITIALIZE INPUTS
    num_orig_vars, num_constraints, constraintsArray, objective = check_input(lp_data)
    
               
    # no of vars, & constraints
    # num_orig_vars = int(input("Enter the number of original decision variables: "))
    # num_constraints = int(input("Enter the number of constraints: "))

    # ====================================================
    # # get objective function and constraint informations
    final_num_vars = sfc.get_constraint(num_orig_vars,constraintsArray)

    
    # build A, b, C matrices        in that order
    A_matrix = sfc.build_Amatrix(num_orig_vars, final_num_vars)
    b_matrix = sfc.build_Bmatrix()
    C_matrix = sfc.build_Cmatrix(num_orig_vars, final_num_vars, objective)


    print(f"A: {A_matrix}\n")
    print(f"B: {b_matrix}\n")
    print(f"C: {C_matrix}\n")



    # function to generate all square matrices
    def generate_square_matrices(A_mx, C_mx):
        all_setparty = []
        m, n = A_mx.shape
        # get all combs
        index_tuples = list(combinations(range(n), m))

        for index in index_tuples:
            onepart = {}
            onepart['A_mx'] = A_mx[:, index]
            onepart['C_mx'] = C_mx[list(index)]     #b/c => C_mx is a 1D array
            onepart['index'] = index
            
            all_setparty.append(onepart)
        return all_setparty



    # ====================compute Rank of matrix A ==================
    rank = np.linalg.matrix_rank(A_matrix)
    print(f"Rank of the matrix: {rank}\n")
    numrows = A_matrix.shape[0]

    if numrows == rank:
        ## generate all possible, m-by-m matrices

        ## {A_mx:[[ndarray]], C_mx:[[ndarray]], index: tuple}
        sets_square_matrices = generate_square_matrices(A_matrix, C_matrix)
        
        ## for-each matrix check if determinant is not 0, Proceed
        for sq_mtrx in sets_square_matrices:
            F = sq_mtrx['A_mx']
            C = sq_mtrx['C_mx']

            det = np.linalg.det(F)
            print(f"{F}, det:= {det}\n")

            if det != 0:
                ## so, its invertible we solve and get value

                ## Solve the linear system Fx = b_matrix
                x = np.linalg.solve(F, b_matrix)
                print(f"Solution vector x: {x}\n")
                
                ## then, store as possible soln
                ## I am converting to list because I will use JSON  
                if np.all(x > 0):
                    sol = {}
                    sol['x'] = x.tolist()
                    sol['index'] = sq_mtrx['index']
                    sol['C'] = C.tolist()
                    solutionSet.append(sol)
                
            else:
                print('This matrix is not invertible!\n')
    else:
        print('you entered an incompatible matrix, start again!!\n')


    # ==================================================================================
        # LETS FETCH THE CHOSEN SOLUTION

    print(f'the solution set: {solutionSet}')
    if solutionSet:
        results = [np.dot(sol['x'], sol['C']) for sol in solutionSet]
        print(f'results: {results}')

        min_index = np.argmin(results)

        # depending on this is a max problem or not, i assume its a min problem default
        chosen_solution = solutionSet[min_index]

        # I can extract feasible solutions ===TURN ON=======
        feasible_solutions = [sol for sol in solutionSet if all(idx < num_orig_vars for idx in sol['index'])]
        feasible_results = [np.dot(sol['x'], sol['C']) for sol in feasible_solutions]
        min_index_feasible = np.argmin(feasible_results)
        chosen_feasible_solution = solutionSet[min_index_feasible]

        # print solution
        for i, idx in enumerate(chosen_solution['index']):
            print(f"x{idx} = {chosen_solution['x'][i]}")

        # print feasible solution only
        for i, idx in enumerate(chosen_feasible_solution['index']):
            print(f"feasible_sol: x{idx} = {chosen_feasible_solution['x'][i]}")

    else:
        print("No solutions found!!")
    
    return chosen_feasible_solution
