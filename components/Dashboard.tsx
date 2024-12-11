import React, { useState, useEffect } from 'react';

interface GatewayMetrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
}

const GatewayMetricsDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<GatewayMetrics>({
    totalRequests: 0,
    successfulRequests: 0,
    failedRequests: 0,
  });

  const fetchGatewayMetrics = async (): Promise<void> => {
    try {
      const response = await fetch(`${process.env.REACT_APP_METRICS_URL}/metrics`);
      const metricsData: GatewayMetrics = await response.json();
      
      if (!metricsData) {
        throw new Error('Metrics fetch operation failed.');
      }
      setMetrics(metricsData);
    } catch (error) {
      console.error('Error while fetching gateway metrics:', error);
    }
  };

  useEffect(() => {
    fetchGatewayMetrics();
    const metricsRefreshInterval = setInterval(fetchGatewayMetrics, 30000);

    return () => clearInterval(metricsRefreshInterval);
  }, []);

  return (
    <div>
      <h2>Gateway Metrics Dashboard</h2>
      <div>Total Requests: {metrics.totalRequests}</div>
      <div>Successful Requests: {metrics.successfulRequests}</div>
      <div>Failed Requests: {metrics.failedRequests}</div>
    </div>
  );
};

export default GatewayMetricsDashboard;