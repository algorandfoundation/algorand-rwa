# Real World Assets on Algorand Dashboard

A comprehensive dashboard for tracking and visualizing Real World Assets (RWA) on the Algorand blockchain. This application provides insights into various RWA categories including stablecoins, commodities, real estate, private credit, micropayments, and more.

## Features

- 📊 **Interactive Charts**: Visualize data with responsive charts powered by Rechart
- 📱 **Responsive Design**: Optimized for desktop and mobile devices
- 🔄 **Real-time Data**: Fetches data from multiple sources via CSV endpoints
- 📈 **Multiple Metrics**: Track market cap, volume, addresses, and more across different asset types
- 🎨 **Modern UI**: Clean, modern interface with smooth animations

## Tech Stack

- **React 19** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Recharts** - Charting library
- **Lucide React** - Icon library
- **CSS Variables** - Theme system for light/dark mode

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd algorand-rwa
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the root directory with your data source URLs:
```env
VITE_MICROPAYMENTS_TRANSACTIONS=<your-url>
VITE_MICROPAYMENTS_ADDRESSES=<your-url>
VITE_MICROPAYMENTS_VOLUME=<your-url>
VITE_STABLECOINS_MARKETCAP=<your-url>
VITE_STABLECOINS_ADDRESSES=<your-url>
VITE_STABLECOINS_VOLUME=<your-url>
VITE_COMMODITIES_MARKETCAP=<your-url>
VITE_COMMODITIES_ADDRESSES=<your-url>
VITE_COMMODITIES_VOLUME=<your-url>
VITE_REALESTATE_MARKETCAP=<your-url>
VITE_REALESTATE_ADDRESSES=<your-url>
VITE_REALESTATE_VOLUME=<your-url>
VITE_REALESTATE_PROPERTIES=<your-url>
# Add other environment variables as needed
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Project Structure

```
src/
├── components/
│   ├── Layout/          # Main layout with header and navigation
│   ├── Footer/          # Footer component
│   ├── Overview/        # Overview dashboard
│   ├── Micropayments/   # Micropayments metrics
│   ├── Stablecoins/    # Stablecoin metrics
│   ├── Commodities/     # Commodity metrics
│   ├── RealEstate/      # Real estate metrics
│   ├── PrivateCredit/   # Private credit metrics
│   ├── Certificates/    # Certificate metrics
│   ├── Loyalty/         # Loyalty program metrics
│   ├── PeraWalletCard/  # Pera Wallet Card metrics
│   └── FAQ/             # Frequently asked questions
├── App.jsx              # Main app component with routing
├── main.jsx             # Application entry point
└── index.css            # Global styles and theme variables
```

## Data Sources

The dashboard aggregates data from multiple sources:

- **Defillama** - DeFi data and analytics
- **Nodely DW** - Blockchain data warehouse
- **Yahoo Finance** - Financial market data

## Contributing

If you have an RWA project on Algorand and would like it to be added to the dashboard, please contact the Algorand Foundation BI Team.

## License

This project is maintained by the Algorand Foundation BI Team.

## Support

For questions or support, please contact the Algorand Foundation BI Team.

---

**Dashboard powered by Algorand Foundation BI Team**
