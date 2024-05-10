// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ConstrainedSolver from './ConstrainedSolver';
import UnconstrainedSolver from './UnconstrainedSolver';
import SolverGrapher from './SolverGrapher';

const App = () => {
  return (
    <Router>
      <header></header>
      <div>
        <nav>
          <Link to="/"><button>Constrained Solver</button></Link>
          <div style={{marginTop:'2px', marginBottom:'2px'}}/>
          <Link to="/unconstrained"><button>Unconstrained Solver</button></Link>
        </nav>

        <Routes>
            <Route path="/" element={<ConstrainedSolver />} />
          <Route path="/unconstrained" element={<UnconstrainedSolver />} />
          <Route path="/solver_grapher" element={<SolverGrapher />} />
        </Routes>
      </div>
      <footer></footer>
    </Router>
  );
};

export default App;
