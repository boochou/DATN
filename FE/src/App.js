import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from '../src/screens/Homepage';
import Tech from './screens/Tech';
import SubdomainScanner from './screens/Subdomain'
import DomainChecker from './screens/Checkdomain'
import ResourceScanner from './screens/ResourceScanner';
import ConfigPage from './screens/Config';
import ApiAnalysis from './screens/API';
import Recommendation from './screens/Recommendation';
import SQLiScanner from './screens/SQLiScanner';

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/DomainChecker" element={<DomainChecker />} />
        <Route path="/SubdomainScanner" element={<SubdomainScanner />} />
        <Route path="/Tech" element={<Tech />} />
        <Route path="/ResourceScanner" element={<ResourceScanner />} />
        <Route path="/Config" element={<ConfigPage />} />
        <Route path="/api" element={<ApiAnalysis />} />
        <Route path="/rcm" element={<Recommendation />} />
        <Route path="/scanner" element={<SQLiScanner />} />
      </Routes>
    </Router>
  );
}
