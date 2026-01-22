import React, { useEffect, useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import './Layout.css';
import classNames from 'classnames';
import Footer from '../Footer/Footer';

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
    const [theme, setTheme] = useState('light');
    

    const darkMode = theme === 'dark';

    useEffect(() => {
        document.documentElement.dataset.theme = theme;
    }, [theme]);

    const toggleTheme = () => {
        setTheme(darkMode ? 'light' : 'dark');
    };

    return (
        <div className="layout">
            <header className="header">
                <div className="container header-content">

                    {/* IMAGE FIRST */}
                    <div className="header-hero">
                        <img
                            src={darkMode ? '/algorand_dark_theme.png' : '/algorand_light_theme.png'}
                            alt="Algorand themed illustration"
                            className="header-hero-image"
                            crossOrigin="anonymous"
                        />
                    </div>

                    {/* HEADER ROW */}
                    <div className="header-top">
                        <div className="header-spacer" />

                        <div className="brand">
                            Real World Assets on Algorand
                        </div>

                        <button
                            type="button"
                            className="theme-toggle"
                            onClick={toggleTheme}
                            aria-label="Toggle dark mode"
                        >
                            {darkMode ? (
                                /* sun icon */
                                <svg className="theme-toggle-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
                                    />
                                </svg>
                            ) : (
                                /* moon icon */
                                <svg className="theme-toggle-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                                    />
                                </svg>
                            )}
                        </button>
                    </div>

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
            <Footer />
        </div>
    );
};
export default Layout;
