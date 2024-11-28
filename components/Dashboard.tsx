import React, { useState, useEffect } from 'react';

interface GatewayMetrics {
  totalRequests: number;
  successfulRequests: number;
  failedRequests: number;
}

const GatewayDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<GatewayMetrics>({
    totalRequests: 0,
    successfulRequests: 0,
    failedRequests: 0,
  });

  const fetchMetrics = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_METRICS_URL}/metrics`);
      if (!response.ok) {
        throw new Error('Failed to fetch metrics');
      }
      const data: GatewayMetrics = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Error fetching gateway metrics:', error);
    }
  };

  useEffect(() => {
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h2>Gateway Dashboard</h2>
      <div>Total Requests: {metrics.totalRequests}</div>
      <div>Successful Requests: {metrics.successfulRequests}</div>
      <div>Failed Requests: {metrics.failedRequests}</div>
    </div>
  );
};

export default GatewayDashboard;