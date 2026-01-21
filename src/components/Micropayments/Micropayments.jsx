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
import './Micropayments.css';

const Micropayments = () => {
  const [data, setData] = useState({
    transactions: [],
    addresses: [],
    volume: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChart, setActiveChart] = useState('transactions');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = {
          transactions: import.meta.env.VITE_MICROPAYMENTS_TRANSACTIONS,
          addresses: import.meta.env.VITE_MICROPAYMENTS_ADDRESSES,
          volume: import.meta.env.VITE_MICROPAYMENTS_VOLUME
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
              if (cols.length < 2) return null;

              const date = cols[0];

              if (type === 'transactions') {
                return {
                  date,
                  algo: parseInt(cols[1], 10) || 0,
                  stable: parseInt(cols[2], 10) || 0,
                  hafn: parseInt(cols[3], 10) || 0,
                  total: parseInt(cols[4], 10) || 0
                };
              } else if (type === 'addresses') {
                return {
                  date,
                  algo: parseInt(cols[1], 10) || 0,
                  stable: parseInt(cols[2], 10) || 0,
                  hafn: parseInt(cols[3], 10) || 0,
                  total: parseInt(cols[4], 10) || 0
                };
              } else if (type === 'volume') {
                return {
                  date,
                  algo: parseFloat(cols[1]) || 0,
                  stable: parseFloat(cols[2]) || 0,
                  hafn: parseFloat(cols[3]) || 0,
                  total: parseFloat(cols[4]) || 0
                };
              }

              return null;
            })
            .filter(Boolean);
        };

        const [txData, addrData, volData] = await Promise.allSettled([
          parseCSV(urls.transactions, 'transactions'),
          parseCSV(urls.addresses, 'addresses'),
          parseCSV(urls.volume, 'volume')
        ]);

        setData({
          transactions: txData.status === 'fulfilled' ? txData.value : [],
          addresses: addrData.status === 'fulfilled' ? addrData.value : [],
          volume: volData.status === 'fulfilled' ? volData.value : []
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
    const current = type === 'addresses' ? arr[lastIndex].cumulative : arr[lastIndex].total;
    const previous = lastIndex > 0 ? (type === 'addresses' ? arr[lastIndex - 1].cumulative : arr[lastIndex - 1].total) : null;

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

  const txKpi = getKpiData(data.transactions, 'transactions');
  const addrKpi = getKpiData(data.addresses, 'addresses');
  const volKpi = getKpiData(data.volume, 'volume');

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
      label: 'Total Payments',
      value: formatCompactNumber(txKpi.value),
      delta: txKpi.delta,
      color: 'var(--accent-primary)'
    },
    {
      id: 'addresses',
      label: 'Total Unique Addresses',
      value: formatCompactNumber(addrKpi.value),
      delta: addrKpi.delta,
      color: 'var(--accent-secondary)'
    },
    {
      id: 'volume',
      label: 'Total Volume',
      value: `$${formatCompactNumber(volKpi.value)}`,
      delta: volKpi.delta,
      color: 'var(--accent-purple)'
    }
  ];

  const chartOptions = [
    { id: 'transactions', label: 'Payments' },
    { id: 'addresses', label: 'Active Addresses' },
    { id: 'volume', label: 'Volume' }
  ];

  const currentChartData = data[activeChart] || [];
  const activeColor = kpis.find(k => k.id === activeChart)?.color || '#fff';

  // Asset type colors
  const assetColors = {
    algo: '#2d2df1',
    stable: '#17cac6',
    hafn: '#ffffffff'
  };

  const getChartConfig = () => {
    switch (activeChart) {
      case 'transactions':
        return {
          leftLabel: 'Monthly Payments',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: true,
          valuePrefix: '',
          bars: [
            { key: 'algo', name: 'ALGO', color: assetColors.algo },
            { key: 'stable', name: 'Stablecoins', color: assetColors.stable },
            { key: 'hafn', name: 'HAFN', color: assetColors.hafn }
          ]
        };
      case 'addresses':
        return {
          leftLabel: 'Monthly Active',
          rightLabel: 'Total Unique',
          hasRightAxis: true,
          showStacked: true,
          valuePrefix: '',
          bars: [
            { key: 'algo', name: 'ALGO', color: assetColors.algo },
            { key: 'stable', name: 'Stablecoins', color: assetColors.stable },
            { key: 'hafn', name: 'HAFN', color: assetColors.hafn }
          ],
          line: { key: 'cumulative', name: 'Total Unique' }
        };
      case 'volume':
        return {
          leftLabel: 'Monthly Volume ($)',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: true,
          valuePrefix: '$',
          bars: [
            { key: 'algo', name: 'ALGO', color: assetColors.algo },
            { key: 'stable', name: 'Stablecoins', color: assetColors.stable },
            { key: 'hafn', name: 'HAFN', color: assetColors.hafn }
          ]
        };
      default:
        return {
          leftLabel: 'Monthly',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: false,
          valuePrefix: '',
          bars: []
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
          <h3>Performance Trends by Asset Type</h3>
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
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
                <XAxis
                  dataKey="date"
                  stroke="var(--text-tertiary)"
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
                    offset: -10,
                    style: { fill: 'var(--text-secondary)', textAnchor: 'middle' }
                  }}
                />
                {chartConfig.hasRightAxis && (
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
                      offset: -10,
                      style: { fill: 'var(--text-secondary)', textAnchor: 'middle' }
                    }}
                  />
                )}
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
                <Legend wrapperStyle={{ paddingTop: '20px' }} />

                {/* Stacked Bars for each asset type */}
                {chartConfig.bars.map((bar, index) => (
                  <Bar
                    key={bar.key}
                    yAxisId="left"
                    dataKey={bar.key}
                    name={bar.name}
                    fill={bar.color}
                    stackId="stack"
                    radius={index === chartConfig.bars.length - 1 ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                    maxBarSize={50}
                  />
                ))}

                {/* Cumulative Line (only for addresses) */}
                {chartConfig.hasRightAxis && chartConfig.line && (
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey={chartConfig.line.key}
                    name={chartConfig.line.name}
                    stroke={activeColor}
                    strokeWidth={3}
                    dot={{ r: 4, fill: 'var(--bg-card)', stroke: activeColor, strokeWidth: 2 }}
                    activeDot={{ r: 6 }}
                  />
                )}
              </ComposedChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
};

export default Micropayments;