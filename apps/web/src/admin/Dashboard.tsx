import React, { useState, useEffect } from 'react';

interface Metrics {
  gmv: number;
  revenue: number;
  active_users: number;
  parse_accuracy: number;
  api_health_score: number;
  conversion_rate: number;
  total_searches_today: number;
  total_products_parsed: number;
}

interface Alert {
  id: string;
  type: string;
  message: string;
  timestamp: string;
  severity: string;
}

interface TrendingProduct {
  name: string;
  searches: number;
  conversion: number;
}

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [trending, setTrending] = useState<TrendingProduct[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
    // Refresh every 30 seconds
    const interval = setInterval(fetchDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch all dashboard data in parallel
      const [metricsRes, alertsRes, trendingRes, chartRes] = await Promise.all([
        fetch('http://localhost:5000/api/admin/dashboard/metrics'),
        fetch('http://localhost:5000/api/admin/dashboard/alerts'),
        fetch('http://localhost:5000/api/admin/dashboard/trending'),
        fetch('http://localhost:5000/api/admin/dashboard/chart-data')
      ]);

      const metricsData = await metricsRes.json();
      const alertsData = await alertsRes.json();
      const trendingData = await trendingRes.json();
      const chartDataRes = await chartRes.json();

      setMetrics(metricsData);
      setAlerts(alertsData);
      setTrending(trendingData);
      setChartData(chartDataRes);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-lg text-gray-600">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard Overview</h1>
        <p className="mt-2 text-gray-600">Real-time business metrics and system health</p>
      </div>

      {/* Alerts Section */}
      {alerts.length > 0 && (
        <div className="mb-6">
          {alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-4 mb-2 rounded-lg border ${
                alert.type === 'warning'
                  ? 'bg-yellow-50 border-yellow-200 text-yellow-800'
                  : 'bg-blue-50 border-blue-200 text-blue-800'
              }`}
            >
              <div className="flex justify-between items-center">
                <div className="flex items-center">
                  <span className="mr-2">
                    {alert.type === 'warning' ? '⚠️' : 'ℹ️'}
                  </span>
                  <span>{alert.message}</span>
                </div>
                <span className="text-sm opacity-75">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* GMV Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">GMV Today</p>
              <p className="text-2xl font-bold text-gray-900">
                {metrics && formatCurrency(metrics.gmv)}
              </p>
            </div>
            <div className="text-3xl">💰</div>
          </div>
          <div className="mt-2">
            <span className="text-sm text-green-600">↑ 12.5%</span>
            <span className="text-sm text-gray-500 ml-2">from yesterday</span>
          </div>
        </div>

        {/* Revenue Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Revenue</p>
              <p className="text-2xl font-bold text-gray-900">
                {metrics && formatCurrency(metrics.revenue)}
              </p>
            </div>
            <div className="text-3xl">📈</div>
          </div>
          <div className="mt-2">
            <span className="text-sm text-green-600">↑ 8.3%</span>
            <span className="text-sm text-gray-500 ml-2">from yesterday</span>
          </div>
        </div>

        {/* Active Users Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-gray-900">
                {metrics?.active_users.toLocaleString()}
              </p>
            </div>
            <div className="text-3xl">👥</div>
          </div>
          <div className="mt-2">
            <span className="text-sm text-green-600">↑ 5.2%</span>
            <span className="text-sm text-gray-500 ml-2">from yesterday</span>
          </div>
        </div>

        {/* Parser Accuracy Card */}
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Parser Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">
                {metrics && formatPercentage(metrics.parse_accuracy)}
              </p>
            </div>
            <div className="text-3xl">🎯</div>
          </div>
          <div className="mt-2">
            <span className={`text-sm ${metrics && metrics.parse_accuracy > 0.95 ? 'text-green-600' : 'text-yellow-600'}`}>
              {metrics && metrics.parse_accuracy > 0.95 ? '✓ Above target' : '⚠ Below target'}
            </span>
          </div>
        </div>
      </div>

      {/* Secondary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* API Health */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">System Health</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">API Health</span>
              <span className={`font-semibold ${metrics && metrics.api_health_score > 0.95 ? 'text-green-600' : 'text-yellow-600'}`}>
                {metrics && formatPercentage(metrics.api_health_score)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Conversion Rate</span>
              <span className="font-semibold">
                {metrics && formatPercentage(metrics.conversion_rate)}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Searches Today</span>
              <span className="font-semibold">
                {metrics?.total_searches_today.toLocaleString()}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Products Parsed</span>
              <span className="font-semibold">
                {metrics?.total_products_parsed.toLocaleString()}
              </span>
            </div>
          </div>
        </div>

        {/* Trending Products */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Trending Products</h3>
          <div className="space-y-3">
            {trending.slice(0, 5).map((product, idx) => (
              <div key={idx} className="flex justify-between items-center">
                <div className="flex items-center">
                  <span className="text-gray-400 mr-2">{idx + 1}.</span>
                  <span className="text-gray-700">{product.name}</span>
                </div>
                <div className="text-right">
                  <div className="text-sm font-semibold">{product.searches}</div>
                  <div className="text-xs text-gray-500">
                    {formatPercentage(product.conversion)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-2">
            <button className="w-full text-left px-4 py-2 bg-blue-50 text-blue-700 rounded hover:bg-blue-100 transition-colors">
              🔬 Test Parser
            </button>
            <button className="w-full text-left px-4 py-2 bg-green-50 text-green-700 rounded hover:bg-green-100 transition-colors">
              📊 View Reports
            </button>
            <button className="w-full text-left px-4 py-2 bg-purple-50 text-purple-700 rounded hover:bg-purple-100 transition-colors">
              🔧 System Settings
            </button>
            <button className="w-full text-left px-4 py-2 bg-yellow-50 text-yellow-700 rounded hover:bg-yellow-100 transition-colors">
              📝 View Logs
            </button>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">24-Hour Activity</h3>
        <div className="h-64 flex items-end space-x-2">
          {chartData.map((data, idx) => (
            <div key={idx} className="flex-1 flex flex-col items-center">
              <div
                className="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                style={{
                  height: `${(data.searches / 5)}px`,
                  minHeight: '4px'
                }}
                title={`${data.hour}: ${data.searches} searches, ${formatCurrency(data.revenue)}`}
              />
              {idx % 3 === 0 && (
                <span className="text-xs text-gray-500 mt-1">{data.hour}</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;