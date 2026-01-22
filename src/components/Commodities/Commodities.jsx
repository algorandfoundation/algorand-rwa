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
import './Commodities.css';

const Commodities = () => {
  const [data, setData] = useState({
    market_cap: [],
    addresses: [],
    volume: [],
    holders: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChart, setActiveChart] = useState('market_cap');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = {
          market_cap: import.meta.env.VITE_COMMODITIES_MARKETCAP,
          addresses: import.meta.env.VITE_COMMODITIES_ADDRESSES,
          volume: import.meta.env.VITE_COMMODITIES_VOLUME,
          holders: import.meta.env.VITE_COMMODITIES_HOLDERS
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

              if (type === 'market_cap') {
                if (cols.length < 4) return null;
                return {
                  date: cols[0],
                  gold$: parseInt(cols[2], 10) || 0,
                  silver$: parseInt(cols[3], 10) || 0,
                  gold: parseInt(cols[4], 10) || 0,
                  total: parseInt(cols[1], 10) || 0
                };
              } else if (type === 'addresses') {
                if (cols.length < 2) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[1], 10) || 0
                };
              } else if (type === 'volume') {
                if (cols.length < 4) return null;
                return {
                  date: cols[0],
                  gold$: parseInt(cols[2], 10) || 0,
                  silver$: parseInt(cols[3], 10) || 0,
                  gold: parseInt(cols[4], 10) || 0,
                  total: parseInt(cols[1], 10) || 0
                };
              } else if (type === 'holders') {
                if (cols.length < 1) return null;
                return {
                  total: parseInt(cols[0], 10) || 0
                };
              }

              return null;
            })
            .filter(Boolean);
        };

        const [mcData, addrData, volData, holderData] = await Promise.allSettled([
          parseCSV(urls.market_cap, 'market_cap'),
          parseCSV(urls.addresses, 'addresses'),
          parseCSV(urls.volume, 'volume'),
          parseCSV(urls.holders, 'holders')
        ]);

        setData({
          market_cap: mcData.status === 'fulfilled' ? mcData.value : [],
          addresses: addrData.status === 'fulfilled' ? addrData.value : [],
          volume: volData.status === 'fulfilled' ? volData.value : [],
          holders: holderData.status === 'fulfilled' ? holderData.value : []
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
    if (type === 'holders') {
      // Holders is just a single value, no array with dates
      if (!arr || arr.length === 0) return { value: 0, delta: null };
      return { value: arr[0].total, delta: null };
    }

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

  const mcKpi = getKpiData(data.market_cap, 'market_cap');
  const addrKpi = getKpiData(data.addresses, 'addresses');
  const volKpi = getKpiData(data.volume, 'volume');
  const holderKpi = getKpiData(data.holders, 'holders');

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
      id: 'market_cap',
      label: 'Stablecoins Market Cap',
      value: `$${formatCompactNumber(mcKpi.value)}`,
      delta: mcKpi.delta,
      color: 'var(--accent-primary)',
      hasChart: true
    },
    {
      id: 'addresses',
      label: 'Monthly Active Addresses',
      value: formatCompactNumber(addrKpi.value),
      delta: addrKpi.delta,
      color: 'var(--accent-primary)',
      hasChart: true
    },
    {
      id: 'volume',
      label: 'Monthly Volume',
      value: `$${formatCompactNumber(volKpi.value)}`,
      delta: volKpi.delta,
      color: 'var(--accent-primary)',
      hasChart: true
    },
    {
      id: 'holders',
      label: 'Total Stablecoin Holders',
      value: formatCompactNumber(holderKpi.value),
      delta: null,
      color: 'var(--accent-primary)',
      hasChart: false
    }
  ];

  const chartOptions = [
    { id: 'market_cap', label: 'Market Cap' },
    { id: 'addresses', label: 'Active Addresses' },
    { id: 'volume', label: 'Volume' }
  ];

  const currentChartData = data[activeChart] || [];
  const activeColor = kpis.find(k => k.id === activeChart)?.color || '#fff';

  // Asset type colors
  const assetColors = {
    gold$: '#2d2df1',
    silver$: '#17cac6',
    gold: '#ffffffff'
  };
  const getChartConfig = () => {
    switch (activeChart) {
      case 'market_cap':
        return {
          leftLabel: 'Market Cap ($)',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: true,
          valuePrefix: '$',
          bars: [
            { key: 'gold$', name: 'GOLD$', color: assetColors.gold$ },
            { key: 'silver$', name: 'Silver$', color: assetColors.silver$ },
            { key: 'gold', name: 'Gold', color: assetColors.gold }
          ]
        };
      case 'addresses':
        return {
          leftLabel: 'Monthly Active Addresses',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: false,
          valuePrefix: '',
          bars: [
            { key: 'total', name: 'Active Addresses', color: activeColor }
          ]
        };
      case 'volume':
        return {
          leftLabel: 'Monthly Volume ($)',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: true,
          valuePrefix: '$',
          bars: [
            { key: 'gold$', name: 'GOLD$', color: assetColors.gold$ },
            { key: 'silver$', name: 'Silver$', color: assetColors.silver$ },
            { key: 'gold', name: 'Gold', color: assetColors.gold }
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
          <div
            key={kpi.id}
            className="kpi-card"
            onClick={() => kpi.hasChart && setActiveChart(kpi.id)}
            style={{ cursor: kpi.hasChart ? 'pointer' : 'default' }}
          >
            <div className="kpi-header">
              <span className="kpi-label">{kpi.label}</span>
            </div>
            <div className="kpi-main-value">
              <div className="kpi-value">{kpi.value}</div>
              {kpi.delta !== null && formatDelta(kpi.delta)}
            </div>
            {kpi.hasChart && (
              <div className={`kpi-indicator ${activeChart === kpi.id ? 'active' : ''}`}>
                Viewing Chart <ArrowUpRight size={14} />
              </div>
            )}
          </div>
        ))}
      </section>

      <section className="chart-section">
        <div className="chart-header">
          <h3>Performance Trends{activeChart === 'addresses' ? '' : ' by Asset Type'}</h3>
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
                  {chartConfig.showStacked && chartConfig.bars.length > 1 ? (
                    // Gradients for stacked bars using assetColors
                    chartConfig.bars.map((bar) => (
                      <linearGradient
                        key={`gradient-${bar.key}-${activeChart}`}
                        id={`barGradient-${bar.key}-${activeChart}`}
                        x1="0"
                        y1="0"
                        x2="0"
                        y2="1"
                      >
                        <stop offset="0%" stopColor={bar.color} stopOpacity={0.8} />
                        <stop offset="95%" stopColor={bar.color} stopOpacity={0.3} />
                      </linearGradient>
                    ))
                  ) : chartConfig.bars.length > 0 ? (
                    // Single bar gradient
                    <linearGradient
                      id={`barGradient-${activeChart}`}
                      x1="0"
                      y1="0"
                      x2="0"
                      y2="1"
                    >
                      <stop offset="0%" stopColor={activeColor} stopOpacity={0.8} />
                      <stop offset="95%" stopColor={activeColor} stopOpacity={0.3} />
                    </linearGradient>
                  ) : null}
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--border-subtle)" />
                <XAxis
                  dataKey="date"
                  stroke="var(--text-tertiary)"
                  tickLine={false}
                  axisLine={false}
                  tickFormatter={(val) => val.slice(0, 7)}
                  label={{ 
                    value: 'Date', 
                    position: 'insideBottom', 
                    offset: -15, 
                    style: { 
                      fill: 'var(--text-secondary)', 
                      textAnchor: 'middle' 
                    } }}
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
                <Legend wrapperStyle={{ paddingTop: '20px', color: 'var(--text-secondary)' }} />

                {/* Bars - stacked or single */}
                {chartConfig.bars.map((bar, index) => (
                  <Bar
                    key={bar.key}
                    yAxisId="left"
                    dataKey={bar.key}
                    name={bar.name}
                    fill={
                      chartConfig.showStacked && chartConfig.bars.length > 1
                        ? `url(#barGradient-${bar.key}-${activeChart})`
                        : chartConfig.bars.length === 1
                        ? `url(#barGradient-${activeChart})`
                        : bar.color
                    }
                    stackId={chartConfig.showStacked && chartConfig.bars.length > 1 ? 'stack' : undefined}
                    radius={
                      chartConfig.showStacked && chartConfig.bars.length > 1
                        ? index === chartConfig.bars.length - 1
                          ? [4, 4, 0, 0]
                          : [0, 0, 0, 0]
                        : [4, 4, 0, 0]
                    }
                    maxBarSize={50}
                  />
                ))}
              </ComposedChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
};

export default Commodities;