import React, { useState } from 'react';
import { ChevronDown } from 'lucide-react';
import './FAQ.css';

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleFaq = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  const faqs = [
    {
      question: "What are Active Addresses?",
      answer: (
        <>
          <p><strong>Active Addresses</strong> are onchain wallets that have interacted at least once during that month with the given application.</p>
          <p>This metric helps measure:</p>
          <ul>
            <li>User engagement with the application</li>
            <li>Monthly activity levels</li>
            <li>Growth in active user base</li>
          </ul>
          <p>A wallet is counted as active if it performs any transaction with the application during the calendar month.</p>
        </>
      )
    },
    {
      question: "What are Micropayments?",
      answer: (
        <>
          <p><strong>Micropayments</strong> focus on ALGO and USDC payments which have a value of less than $250. In addition to this, HAFN is also included as a micropayment method.</p>
          <p>This metric tracks:</p>
          <ul>
            <li>ALGO payments &lt; $250</li>
            <li>USDC payments &lt; $250</li>
            <li>All HAFN transactions</li>
          </ul>
        </>
      )
    },
    {
      question: "Which Stablecoins are tracked?",
      answer: (
        <>
          <p>The stablecoins considered are:</p>
          <ul>
            <li><strong>USDC</strong> (USD Coin)</li>
            <li><strong>USDT</strong> (Tether)</li>
            <li><strong>xUSD</strong></li>
            <li><strong>goUSD</strong></li>
          </ul>
          <p><strong>Important:</strong> The mints and burns are <strong>not included</strong> on the dashboard.</p>
        </>
      )
    },
    {
      question: "What Commodities are included?",
      answer: (
        <>
          <p>The assets considered are:</p>
          <p><strong>From Meld Gold:</strong></p>
          <ul>
            <li><strong>GOLD$</strong> - Tokenized gold</li>
            <li><strong>SILVER$</strong> - Tokenized silver</li>
          </ul>
          <p><strong>From ASA.Gold:</strong></p>
          <ul>
            <li><strong>Gold</strong> - Gold-backed tokens</li>
          </ul>
        </>
      )
    },
    {
      question: "What is Private Credit based on?",
      answer: (
        <>
          <p>Private Credit relies on <strong>Folks Finance Lending</strong> platform.</p>
          <p>This includes all lending and borrowing activities on the Folks Finance protocol.</p>
        </>
      )
    },
    {
      question: "What is Real Estate based on?",
      answer: (
        <>
          <p>Real Estate relies on <strong>Lofty</strong> platform.</p>
          <p>This includes all tokenized real estate activities and transactions on Lofty.</p>
        </>
      )
    },
    {
      question: "What is Loyalty based on?",
      answer: (
        <>
          <p>Loyalty relies on <strong>WorldChess wcpp program</strong>.</p>
          <p>This tracks all activities related to the WorldChess loyalty points and rewards program.</p>
        </>
      )
    }
  ];

  return (
    <div className="faq-container">
      <div className="faq-header">
        <h1>Frequently Asked Questions</h1>
        <p>Find answers to common questions about the metrics and data in this dashboard.</p>
      </div>

      <div className="faq-list">
        {faqs.map((faq, index) => (
          <div key={index} className="faq-item">
            <button
              className={`faq-question ${openIndex === index ? 'active' : ''}`}
              onClick={() => toggleFaq(index)}
            >
              <span>{faq.question}</span>
              <ChevronDown
                size={20}
                className={`chevron ${openIndex === index ? 'rotate' : ''}`}
              />
            </button>
            <div className={`faq-answer ${openIndex === index ? 'open' : ''}`}>
              <div className="faq-answer-content">
                {faq.answer}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FAQ;