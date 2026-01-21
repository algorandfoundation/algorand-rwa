import React, { useEffect, useState } from 'react';
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { ArrowUpRight } from 'lucide-react';
import './Loyalty.css';

const Loyalty = () => {
  const [data, setData] = useState({
    transactions: [],
    addresses: [],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChart, setActiveChart] = useState('market_cap');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = {
          transactions: import.meta.env.VITE_LOYALTY_TRANSACTIONS,
          addresses: import.meta.env.VITE_LOYALTY_ADDRESSES,
        };

        const parseCSV = async (url, type) => {
          if (!url) return [];
          const response = await fetch(url);
          if (!response.ok) throw new Error(`Failed to fetch ${type}`);
          const text = await response.text();
          const rows = text.split('\n').slice(1);
          return rows
            .map(row => {
              const cols = row.split(',');

              if (type === 'transactions') {
                if (cols.length < 3) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[1], 10) || 0,
                  cumulative: parseInt(cols[2], 10) || 0
                };
              } else if (type === 'addresses') {
                if (cols.length < 3) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[1], 10) || 0,
                  cumulative: parseInt(cols[2], 10) || 0
                };
              }

              return null;
            })
            .filter(Boolean);
        };

        const [transactionsData, addressesData] = await Promise.allSettled([
          parseCSV(urls.transactions, 'transactions'),
          parseCSV(urls.addresses, 'addresses'),
        ]);

        setData({
          transactions: transactionsData.status === 'fulfilled' ? transactionsData.value : [],
          addresses: addressesData.status === 'fulfilled' ? addressesData.value : [],
        });
      } catch (err) {
        console.error("Error loading data", err);
        setError("Failed to load some data feeds");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getKpiData = (arr, type) => {
    if (!arr || arr.length === 0) return { value: 0, delta: null };

    const lastIndex = arr.length - 1;
    const current = arr[lastIndex].total;
    const previous = lastIndex > 0 ? arr[lastIndex - 1].total : null;

    const delta = previous ? (current / previous) - 1 : null;

    return { value: current, delta };
  };

  const formatCompactNumber = (num) => {
    if (num === undefined || num === null) return '0';
    return Intl.NumberFormat('en-US', {
      notation: "compact",
      maximumFractionDigits: 1
    }).format(num);
  };

  const formatFullNumber = (num) => {
    if (num === undefined || num === null) return '0';
    return Intl.NumberFormat('en-US', {
      maximumFractionDigits: 0
    }).format(num);
  };

  const formatTooltipNumber = (num) => {
    if (num === undefined || num === null) return '0';
    if (num < 10000) {
      return formatFullNumber(num);
    }
    return formatCompactNumber(num);
  };

  const transactionsKpi = getKpiData(data.transactions, 'transactions');
  const addressesKpi = getKpiData(data.addresses, 'addresses');

  const formatDelta = (delta) => {
    if (delta === null) return null;
    const percentage = (delta * 100).toFixed(2);
    const isPositive = delta >= 0;
    return (
      <span className={`kpi-delta ${isPositive ? 'positive' : 'negative'}`}>
        {isPositive ? '+' : ''}{percentage}%
      </span>
    );
  };

  const kpis = [
    {
      id: 'transactions',
      label: 'Monthly Transactions',
      value: `${formatCompactNumber(transactionsKpi.value)}`,
      delta: transactionsKpi.delta,
      color: 'var(--accent-primary)',
      hasChart: true
    },
    {
      id: 'addresses',
      label: 'Monthly Active Addresses',
      value: formatCompactNumber(addressesKpi.value),
      delta: addressesKpi.delta,
      color: 'var(--accent-secondary)',
      hasChart: true
    }
  ];

  const chartOptions = [
    { id: 'transactions', label: 'Transactions' },
    { id: 'addresses', label: 'Addresses' },
  ];

  const currentChartData = data[activeChart] || [];
  const activeColor = kpis.find(k => k.id === activeChart)?.color || '#fff';


  const getChartConfig = () => {
    switch (activeChart) {
      case 'transactions':
        return {
          leftLabel: 'Monthly Transactions',
          rightLabel: 'Total Transactions',
          monthlyName: 'Monthly Transactions',
          cumulativeName: 'Total Transactions',
          valuePrefix: '',
          valueSuffix: ''
        };
      case 'addresses':
        return {
          leftLabel: 'Monthly Active Addresses',
          rightLabel: 'Total Unique Addresses',
          monthlyName: 'Monthly Active Addresses',
          cumulativeName: 'Total Unique Addresses',
          valuePrefix: '',
          valueSuffix: ''
        };
      default:
        return {
          leftLabel: 'Monthly',
          rightLabel: 'Cumulative',
          monthlyName: 'Monthly',
          cumulativeName: 'Cumulative',
          valuePrefix: '',
          valueSuffix: ''
        };
    }
  };

  const chartConfig = getChartConfig();

  return (
    <div className="overview-container fade-in">
      <section className="kpi-grid">
        {kpis.map((kpi) => (
          <div key={kpi.id} className="kpi-card" onClick={() => setActiveChart(kpi.id)}>
            <div className="kpi-header">
              <span className="kpi-label">{kpi.label}</span>
            </div>
            <div className="kpi-main-value">
              <div className="kpi-value">{kpi.value}</div>
              {kpi.delta !== null && formatDelta(kpi.delta)}
            </div>
            <div className={`kpi-indicator ${activeChart === kpi.id ? 'active' : ''}`}>
              Viewing Chart <ArrowUpRight size={14} />
            </div>
          </div>
        ))}
      </section>

      <section className="chart-section">
        <div className="chart-header">
          <h3>Performance Trends</h3>
          <div className="chart-pills">
            {chartOptions.map((opt) => (
              <button
                key={opt.id}
                className={`pill ${activeChart === opt.id ? 'active' : ''}`}
                onClick={() => setActiveChart(opt.id)}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        <div className="chart-container">
          {loading ? (
            <div className="loading-state">Loading Data...</div>
          ) : currentChartData.length === 0 ? (
            <div className="empty-state">No data available for this metric</div>
          ) : (
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={currentChartData}>
                <defs>
                  <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor={activeColor} stopOpacity={0.8} />
                    <stop offset="95%" stopColor={activeColor} stopOpacity={0.3} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
                <XAxis
                  dataKey="date"
                  stroke="var(--text-secondary)"
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => val.slice(0, 7)}
                  label={{ value: 'Date', position: 'insideBottom', offset: -15 }}
                />
                <YAxis
                  yAxisId="left"
                  orientation="left"
                  stroke="var(--text-tertiary)"
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={formatCompactNumber}
                  label={{
                    value: chartConfig.leftLabel,
                    position: 'insideLeft',
                    angle: -90,
                    offset: 0,
                    style: { fill: 'var(--text-secondary)', textAnchor: 'middle' }
                  }}
                />
                <YAxis
                  yAxisId="right"
                  orientation="right"
                  stroke="var(--text-tertiary)"
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={formatCompactNumber}
                  label={{
                    value: chartConfig.rightLabel,
                    position: 'insideRight',
                    angle: 90,
                    offset: 0,
                    style: { fill: 'var(--text-secondary)', textAnchor: 'middle' }
                  }}
                />
                <Tooltip
                  contentStyle={{ backgroundColor: 'var(--bg-card)', borderColor: 'var(--border-highlight)' }}
                  itemStyle={{ color: 'var(--text-primary)' }}
                  formatter={(value, name) => {
                    const prefix = chartConfig.valuePrefix;
                    const formatted = formatTooltipNumber(value);
                    return [
                      `${prefix}${formatted}`,
                      name
                    ];
                  }}
                />
                <Legend wrapperStyle={{ paddingTop: '20px', color: '#ffffff' }} />
                <Bar
                  yAxisId="left"
                  dataKey="total"
                  name={chartConfig.monthlyName}
                  fill="url(#barGradient)"
                  radius={[4, 4, 0, 0]}
                  maxBarSize={50}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="cumulative"
                  name={chartConfig.cumulativeName}
                  stroke={'#17cac6'}
                  strokeWidth={3}
                  dot={{ r: 4, fill: 'var(--bg-card)', stroke: '#17cac6', strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                />
              </ComposedChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
};

export default Loyalty;