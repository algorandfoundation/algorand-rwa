import React, { useEffect, useState } from 'react';
import {
  ComposedChart,
  Bar,
  Area,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { ArrowUpRight } from 'lucide-react';
import './RealEstate.css';

const RealEstate = () => {
  const [data, setData] = useState({
    market_cap: [],
    addresses: [],
    volume: [],
    properties: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeChart, setActiveChart] = useState('market_cap');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const urls = {
          market_cap: import.meta.env.VITE_REALESTATE_MARKETCAP,
          addresses: import.meta.env.VITE_REALESTATE_ADDRESSES,
          volume: import.meta.env.VITE_REALESTATE_VOLUME,
          properties: import.meta.env.VITE_REALESTATE_PROPERTIES
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
                if (cols.length < 2) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[1], 10) || 0
                };
              } else if (type === 'addresses') {
                if (cols.length < 2) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[1], 10) || 0
                };
              } else if (type === 'volume') {
                if (cols.length < 2) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[7], 10) || 0
                };
              } else if (type === 'properties') {
                if (cols.length < 3) return null;
                return {
                  date: cols[0],
                  total: parseInt(cols[2], 10) || 0
                };
              }

              return null;
            })
            .filter(Boolean);
        };

        const [mcData, addrData, volData, propData] = await Promise.allSettled([
          parseCSV(urls.market_cap, 'market_cap'),
          parseCSV(urls.addresses, 'addresses'),
          parseCSV(urls.volume, 'volume'),
          parseCSV(urls.properties, 'properties')
        ]);

        setData({
          market_cap: mcData.status === 'fulfilled' ? mcData.value : [],
          addresses: addrData.status === 'fulfilled' ? addrData.value : [],
          volume: volData.status === 'fulfilled' ? volData.value : [],
          properties: propData.status === 'fulfilled' ? propData.value : []
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
    if (type === 'properties') {
      if (!arr || arr.length === 0) return { value: 0, delta: null };
      return { value: arr[arr.length - 1].total, delta: null };
    }

    if (!arr || arr.length === 0) return { value: 0, delta: null };

    const lastIndex = arr.length - 1;
    const current = arr[lastIndex].total;

    let previous = null;
    let delta = null;

    if (type === 'market_cap') {
      // For market cap, compare with index-30 (30 periods ago)
      const compareIndex = lastIndex - 30;
      if (compareIndex >= 0) {
        previous = arr[compareIndex].total;
        delta = previous ? (current / previous) - 1 : null;
      }
    } else {
      // For other metrics, compare with previous period
      previous = lastIndex > 0 ? arr[lastIndex - 1].total : null;
      delta = previous ? (current / previous) - 1 : null;
    }

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
  const propKpi = getKpiData(data.properties, 'properties');

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
      label: 'Real Estate Market Cap',
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
      id: 'properties',
      label: 'Total Properties',
      value: formatCompactNumber(propKpi.value),
      delta: null,
      color: 'var(--accent-primary)',
      hasChart: false
    }
  ];

  const chartOptions = [
    { id: 'market_cap', label: 'Market Cap' },
    { id: 'addresses', label: 'Active Addresses' },
    { id: 'volume', label: 'Monthly Volume' },
    { id: 'properties', label: 'TokenizedProperties' }
  ];

  const currentChartData = data[activeChart] || [];
  const activeColor = kpis.find(k => k.id === activeChart)?.color || '#fff';


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
            { key: 'total', name: 'Market Cap', color: activeColor }
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
            { key: 'total', name: 'Monthly Volume', color: activeColor }
          ]
        };
      case 'properties':
        return {
          leftLabel: 'Total Properties',
          rightLabel: '',
          hasRightAxis: false,
          showStacked: true,
          valuePrefix: '',
          bars: [
            { key: 'total', name: 'Total Tokenized Properties', color: activeColor }
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
                  {activeChart !== 'market_cap' && (
                    <linearGradient id={`barGradient-${activeChart}`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={activeColor} stopOpacity={0.8} />
                      <stop offset="95%" stopColor={activeColor} stopOpacity={0.3} />
                    </linearGradient>
                  )}
                  {activeChart === 'market_cap' && (
                    <linearGradient id={`areaGradient-${activeChart}`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor={activeColor} stopOpacity={0.4} />
                      <stop offset="100%" stopColor={activeColor} stopOpacity={0.05} />
                    </linearGradient>
                  )}
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

                {/* Area chart for market_cap, Bars for others */}
                {activeChart === 'market_cap' ? (
                  chartConfig.bars.map((bar, index) => (
                    <Area
                      key={bar.key}
                      yAxisId="left"
                      type="monotone"
                      dataKey={bar.key}
                      name={bar.name}
                      fill={`url(#areaGradient-${activeChart})`}
                      stroke={activeColor}
                      strokeWidth={2}
                    />
                  ))
                ) : (
                  chartConfig.bars.map((bar, index) => (
                    <Bar
                      key={bar.key}
                      yAxisId="left"
                      dataKey={bar.key}
                      name={bar.name}
                      fill={chartConfig.bars.length > 1 && chartConfig.showStacked ? bar.color : `url(#barGradient-${activeChart})`}
                      stackId={chartConfig.showStacked && chartConfig.bars.length > 1 ? 'stack' : undefined}
                      radius={
                        chartConfig.showStacked && chartConfig.bars.length > 1
                          ? (index === chartConfig.bars.length - 1 ? [4, 4, 0, 0] : [0, 0, 0, 0])
                          : [4, 4, 0, 0]
                      }
                      maxBarSize={50}
                    />
                  ))
                )}
              </ComposedChart>
            </ResponsiveContainer>
          )}
        </div>
      </section>
    </div>
  );
};

export default RealEstate;