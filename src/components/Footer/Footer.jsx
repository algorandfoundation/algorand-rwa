import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container footer-content">
        <div className="footer-section">
          <h4 className="footer-title">Data Sources</h4>
          <div className="footer-sources">
            <span>Defillama</span>
            <span className="footer-separator">•</span>
            <span>Nodely DW</span>
            <span className="footer-separator">•</span>
            <span>Yahoo Finance</span>
          </div>
        </div>

        <div className="footer-section">
          <p className="footer-text">
            If you have an RWA project on Algorand contact us so it can be added.
          </p>
        </div>

        <div className="footer-section">
          <p className="footer-powered">
            Dashboard powered by <strong>Algorand Foundation BI Team</strong>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

