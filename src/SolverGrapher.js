import React from 'react';
import { useLocation } from 'react-router-dom';



const SolverGrapher = () => {
    const location = useLocation();
    const { solution, constraints } = location.state;

    // Function to format each constraint
    const formatConstraint = (constraint) => {
        const coefficient1 = constraint[0];
        const coefficient2 = constraint[1];
        const operator = constraint[2];
        const value = constraint[3];

        return `${coefficient1}x + ${coefficient2}y ${operator} ${value}`;
    };

    return (
        <div>
            <h2>Equation</h2>
            {/* Display the equation that was solved */}
            <div>
                <h2>Constraints</h2>
                {/* Display formatted constraints here */}
                {constraints.map((constraint, index) => (
                    <p key={index}>{formatConstraint(constraint)}</p>
                ))}
            </div>

            <h2>Graph</h2>
            <div className='grapher_cont'>
                <div className='grapher_igbox'>
                    <img className='grapher_ig' src={`http://localhost:5000/images/img1.png?${new Date().getTime()}`} alt='graph1'></img>
                </div>
                <div className='grapher_igbox'>
                    <img className='grapher_ig' src={`http://localhost:5000/images/img2.png?${new Date().getTime()}`} alt='graph2'></img>
                </div>
            </div>

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

export default SolverGrapher;
