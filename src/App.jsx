import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Overview from './components/Overview/Overview';
import Micropayments from './components/Micropayments/Micropayments';
import PeraWalletCard from './components/PeraWalletCard/PeraWalletCard';
import Stablecoins from './components/Stablecoins/Stablecoins';
import Commodities from './components/Commodities/Commodities';
import PrivateCredit from './components/PrivateCredit/PrivateCredit';
import RealEstate from './components/RealEstate/RealEstate';
import Certificates from './components/Certificates/Certificates';
import Loyalty from './components/Loyalty/Loyalty';
import FAQ from './components/FAQ/FAQ';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Overview />} />
          <Route path="micropayments" element={<Micropayments />} />
          <Route path="pera-wallet-card" element={<PeraWalletCard />} />
          <Route path="stablecoins" element={<Stablecoins />} />
          <Route path="commodities" element={<Commodities />} />
          <Route path="private-credit" element={<PrivateCredit />} />
          <Route path="real-estate" element={<RealEstate />} />
          <Route path="certificates" element={<Certificates />} />
          <Route path="loyalty" element={<Loyalty />} />
          <Route path="faq" element={<FAQ />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
