import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


def prepare_graph(graphdata):
    constraints = graphdata['constraints']
    objective = graphdata['objective']
    solution = graphdata['solution']['res']

    validpoints = []
    # Ensure the 'images' directory exists, create it if it doesn't
    targetpath = os.path.join(os.path.curdir,'images')
    os.makedirs(targetpath, exist_ok=True)

    try:
        fig = plt.figure()

        # Plot constraint functions
        fig, ax = plt.subplots()
        for i, constraint in enumerate(constraints, start=1):
            x = np.linspace(0, 10, 20)
            y = (float(constraint[3]) - float(constraint[0]) * x) / float(constraint[1])
            ax.plot(x, y, label=f'Constraint {i}')

        x = np.linspace(0, 10, 20)
        y = np.linspace(0, 10, 20)
        x, y = np.meshgrid(x, y)

        # Calculate valid points
        for ym in y:
            for i in range(len(x[0])):
                if ( int(constraints[0][0]) * x[0][i] + int(constraints[0][1]) * ym[i] <= int(constraints[0][3])) and ( int(constraints[1][0]) * x[0][i] + int(constraints[1][1]) * ym[i] <= int(constraints[1][3])):
                    validpoints.append((x[0][i],ym[i]))        

        # Plot valid points as red dot
        for vp in validpoints:
            ax.scatter(vp[0], vp[1], color='red')
        ax.scatter(solution['x'][0], solution['x'][1], color='green')
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Constraint Functions')
        ax.legend()

        constraints_path = os.path.join(targetpath,'img1.png')
        plt.savefig(constraints_path)
        plt.close()

        # Plot objective function
        fig = plt.figure()
        ax3 = fig.add_subplot(1, 1, 1, projection='3d')
        
        z = (float(objective[0]) * x + float(objective[1]) * y)
        ax3.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=0.6)
        # we can even reinclude this in the part
        for i, constraint in enumerate(constraints, start=1):
            x = np.linspace(0, 10, 20)
            y = (float(constraint[3]) - float(constraint[0]) * x) / float(constraint[1])
            ax3.plot(x, y, label=f'Constraint {i}')

        ax3.set_xlabel('x')
        ax3.set_ylabel('y')
        ax3.set_zlabel('z')
        ax3.set_title('Objective Function')


        # Plot intersection point on 3D surface
        # recieved sol
        sol = solution['x']
        ax3.scatter(sol[0], sol[1], sol[0]*float(objective[0]) + sol[1]*float(objective[1]), color='red', label='Intersection Point', s=80, alpha=1.0)
        # Tracing
        ax3.plot([sol[0], sol[0]], [sol[1], sol[1]], [0, sol[0]*float(objective[0]) + sol[1]*float(objective[1])], color='black', linestyle='dotted')

        objective_path = os.path.join(targetpath,'img2.png')
        plt.savefig(objective_path)
        plt.close()

        # Return paths to the saved image files
        return constraints_path, objective_path

    except Exception as e:
        print(f"An error occurred while preparing the graph: {e}")
        return None, None
