import numpy as np
from Fy_functions import formnumber2 as fnr
from itertools import combinations
"""
This program will only solve problems where all variables 
x1, x2, ... , xn >= 0
if theres one or more varibles that dont satisfy this, then
use this second solver.
"""

def solve_unconstrained(lp_data):
    # nature of data recieved => {'numVars': '', 'numConstraints': '', 'constraints': [], 'objective': 'objective', 'unconsVarsindex':'unconsVarsindex'}
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
                unconsVarsindex = lp_data['unconsVarsindex']
                return num_orig_vars, num_constraints, constraintsArray, objective, unconsVarsindex
    
    # INITIALIZE INPUTS
    num_orig_vars, num_constraints, constraintsArray, objective, unconsVarsindex = check_input(lp_data)



    ##E: get index pos of unconstrained vars
    # input_poss = input("index positions of unconstrained vars, '0 1 ...  ' first variable is index 0: ").split()
    input_poss = unconsVarsindex
    
    index_of_uncons_vars = list(map(int,input_poss))

    for x in index_of_uncons_vars:
        if x not in range(num_orig_vars):
            print('you entered an invalid location for var: first var is pos 0')
            exit()      #premature exit

    # get objective function and constraint informations
    final_numvars_consr = fnr.get_constraint(num_orig_vars,constraintsArray)


    # build the constrained A, b, C matrices
    A_matrix_consr = fnr.build_Amatrix(num_orig_vars, final_numvars_consr)
    b_matrix = fnr.build_Bmatrix()
    C_matrix_consr = fnr.build_Cmatrix(num_orig_vars, final_numvars_consr, objective)

    # print(f"A: {A_matrix_consr}\n")
    # print(f"B: {b_matrix}\n")
    # print(f"C: {C_matrix_consr}\n")

    # ====================================== ADJUST INPUTS ===========================================
    # Adjust to build the unconstrained matrices
    A_matrix,notedindexes = fnr.adjust_Amatrix(A_matrix_consr,index_of_uncons_vars)
    C_matrix = fnr.adjust_Cmatrix(C_matrix_consr,index_of_uncons_vars)

    print(f"A: {A_matrix}\n")
    print(f"B: {b_matrix}\n")
    print(f"C: {C_matrix}\n")
    # ================================================================================================

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
                if np.all(x > 0):
                    sol = {}
                    sol['x'] = x
                    sol['index'] = sq_mtrx['index']
                    sol['C'] = C
                    solutionSet.append(sol)
                
            else:
                print('This matrix is not invertible!\n')
    else:
        print('you entered an incompatible matrix, start again!!\n')


    print(f'initial solution set: {solutionSet}\n')
    # ==================================================================================
    # # ====================== END FOR PREVIOUS PROGRAM ==================================

    # FUNCTION TO COMBINE PARTIAL VALUES IF ANY (MAY ADD)
    def combinesols(solutionset,notedindexes):
        for i in notedindexes:
            compressed_sol = []
            for sol in solutionset:
                solly2 = list(sol['index'])
                if i in solly2:
                    if (i+1) in solly2:
                        tous = solly2.index(i)
                        toremv = solly2.index(i+1)

                        sol['x'][tous] -= sol['x'][toremv]

                        solly2.remove(solly2[toremv])
                        sol['x'] = np.delete(sol['x'], toremv)
                        
                sol['index'] = tuple(solly2)
                if (notedindexes.index(i) == len(notedindexes)-1):
                    compressed_sol.append(sol)
        return compressed_sol


    # LETS FETCH THE CHOSEN SOLUTION
    solutionSet = combinesols(solutionSet,notedindexes)

    # only because i am doing a JSON thing later
    for sol in solutionSet:
        sol['x'] = sol['x'].tolist()
        sol['C'] = sol['C'].tolist()
    
    # =================================================================================
    print(f'combined solution set: {solutionSet}\n')
    if solutionSet:
        results = [np.dot(sol['x'], sol['C']) for sol in solutionSet]
        print(f'results: {results}\n')

        min_index = np.argmin(results)

        # depending on this is a max problem or not, i assume its a min problem default
        chosen_solution = solutionSet[min_index]

        # print solution
        for i, idx in enumerate(chosen_solution['index']):
            print(f"x{idx} = {chosen_solution['x'][i]}")
        

    # ============================== TURN ON TO EXTRACT FEASIBLE ONLY =============================================
        # # I can extract feasible solutions
        # feasible_solutions = [sol for sol in solutionSet if all(idx < num_orig_vars for idx in sol['index'])]
        # feasible_results = [np.dot(sol['x'], sol['C']) for sol in feasible_solutions]
        # min_index_feasible = np.argmin(feasible_results)
        # chosen_feasible_solution = solutionSet[min_index_feasible]

        # # print feasible solution only
        # for i, idx in enumerate(chosen_feasible_solution['index']):
        #     print(f"feasible_sol: x{idx} = {chosen_feasible_solution['x'][i]}")
    # =============================================================================================================

    else:
        print("No solutions found!!")
    return chosen_solution