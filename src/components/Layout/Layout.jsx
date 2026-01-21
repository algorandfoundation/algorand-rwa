import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import './Layout.css';
import classNames from 'classnames';

const tabs = [
    { name: 'Overview', path: '/' },
    { name: 'Micropayments', path: '/micropayments' },
    { name: 'Pera Wallet Card', path: '/pera-wallet-card' },
    { name: 'Stablecoins', path: '/stablecoins' },
    { name: 'Commodities', path: '/commodities' },
    { name: 'Private Credit', path: '/private-credit' },
    { name: 'Real Estate', path: '/real-estate' },
    { name: 'Certificates', path: '/certificates' },
    { name: 'Loyalty', path: '/loyalty' },
    { name: 'FAQ', path: '/faq' },
];

const Layout = () => {
    return (
        <div className="layout">
            <header className="header">
                <div className="container header-content">
                    <div className="brand">Real World Assets on Algorand</div>
                    <nav className="nav">
                        {tabs.map((tab) => (
                            <NavLink
                                key={tab.path}
                                to={tab.path}
                                className={({ isActive }) =>
                                    classNames('nav-link', { active: isActive })
                                }
                            >
                                {tab.name}
                            </NavLink>
                        ))}
                    </nav>
                </div>
            </header>
            <main className="main-content container">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
