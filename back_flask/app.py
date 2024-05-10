from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from Fy_functions import main, main2, graphgen
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow requests from http://localhost:3000

# Define the directory where images are stored
image_directory = os.path.join(os.path.curdir, 'images')

# Route to serve the React app
@app.route('/')
def serve_react_app():
    return send_from_directory('./static', 'index.html')

# Route to serve static files (CSS, JavaScript, images, etc.)
@app.route('/static/<path:path>')
def serve_static_files(path):
    return send_from_directory('./static', path)

# Route to serve image proper
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(image_directory, filename)

@app.route('/solve_constrained',methods=["POST"])
def solve_constrained():

    # Call your solver function with the the request data in
    solution_set = main.solve_constrained(request.json)
    
    print('I called the function')

    # Check if solution_set is empty or None
    if solution_set is None:
        raise ValueError("No data returned from solve_constrained function")

    # Return the result as JSON
    return jsonify({'res': solution_set})
    

@app.route('/solve_unconstrained',methods=["POST"])
def solve_unconstrained():

    # Call your solver function with the the request data in
    solution_set = main2.solve_unconstrained(request.json)
    
    print('I called function 2')
    
    # Check if solution_set is empty or None
    if solution_set is None:
        raise ValueError("No data returned from solve_constrained function")

    # Return the result as JSON
    return jsonify({'res': solution_set})
    

@app.route('/generate_graph',methods=["POST"])
def generate_graph():

    # Call the grapher function with the the request data in
    solution_set = graphgen.prepare_graph(request.json)
    
    print('I called generating graph!')
    
    # Check if solution_set is empty or None
    if solution_set is None:
        raise ValueError("No data returned from solve_constrained function")

    # Return the result as JSON
    return jsonify({'res': solution_set})



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
