// ConstrainedSolver.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ConstrainedSolver = () => {
        const [numVars, setNumVars] = useState('');
        const [numConstraints, setNumConstraints] = useState('');
        const [constraints, setConstraints] = useState([]);
        const [objective, setObjective] = useState([])
        const [solution, setSolution] = useState(null);
        const navigate = useNavigate();

        // recieve the number of constraint as well as the sign and constant involved
        const handleAddConstraint = () => {
            if (constraints.length<parseInt(numVars)){
                const newRow = new Array(parseInt(numVars, 10) + 2).fill('');
                const updatedConstraints = [...constraints, newRow];
                setConstraints(updatedConstraints);
            }
        };

        // prepare to recieve objective function
        
        const handleObjectiveChange = (e,itmix) => {
            const objectivecpy = [...objective];
            objectivecpy[itmix] = e.target.value;
            setObjective(objectivecpy);
        }

        const handleSolve = ()=>{
            fetch('http://localhost:5000/solve_constrained', 
                {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json',},
                    body: JSON.stringify({
                                numVars: numVars,
                                numConstraints: numConstraints,
                                constraints: constraints,
                                objective: objective,
                            }),
                })
                .then(res => res.json())
                .then(data => {
                    setSolution(data);
                })
                .catch(error => console.error('Error:', error));
            }

        const handleConstraintChange = (e, rowIndex, colIndex) => {
            const updatedConstraints = [...constraints];
            updatedConstraints[rowIndex][colIndex] = e.target.value;
            setConstraints(updatedConstraints);
        };

        const handleShowGraph = () => {
            // Send a POST request to the backend to generate graphs
            fetch('http://localhost:5000/generate_graph', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    constraints: constraints,
                    objective: objective,
                    solution: solution
                }),
            })
            .then(() => {
                // Navigate to the SolverGrapher page
                navigate('/solver_grapher', { state: { solution: solution, constraints: constraints } });
            })
            .catch(error => {
                console.error('Error generating graph:', error);
                // Handle error
            });
        };
    
    return (
        <div className='power_content'>
            <h2>Constrained Solver</h2>
            <div className='top_sets'>
                <label>
                    Number of variables:
                    <input type="number" value={numVars} onChange={(e) => {setNumVars(e.target.value)}} />
                </label>

                <label>
                    Number of constraints:
                    <input type="number" value={numConstraints} onChange={(e) => setNumConstraints(e.target.value)} />
                </label>
                <button onClick={handleAddConstraint}>Add Constraint</button>
            </div>
            

            <div className='our_inputs'>
            {constraints.map((row, rowIndex) => (
                <div key={rowIndex}>
                {row.map((cell, colIndex) => (
                    <input key={colIndex} value={cell} onChange={(e) => handleConstraintChange(e, rowIndex, colIndex)} />
                ))}
                </div>
            ))}
            </div>

            <h4>Objectives:</h4>
            {numVars !== '' && constraints.length === parseInt(numConstraints) && (
                
                <div className='our_inputs'>
                    {(new Array(parseInt(numVars, 10)).fill('')).map((value, index) => (
                        
                            <input
                                key={index}
                                
                                onChange={(e) => handleObjectiveChange(e, index)}
                            />
                        
                    ))}
                </div>
            )}

            {numVars !== '' && constraints.length === parseInt(numConstraints) && (
                <button onClick={handleSolve}>Solve</button>
            )}

            
            {/* Show graph button */}
            {solution && numVars <= 2 && (
                <button className='red-button' onClick={handleShowGraph}>Exit and Show Graph</button>
            )}
            
            {/* Render solution */}

            {solution && (
                <div>
                    <h3>Solution</h3>
                    {solution.res.index.map((index, i) => (
                        <p key={i}> x{index} = {solution.res.x[i]} </p>
                    ))}
                </div>
            )}

        </div>
    );
};

export default ConstrainedSolver;
