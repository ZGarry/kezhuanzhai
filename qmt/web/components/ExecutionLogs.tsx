import { useState, useEffect } from 'react';

export default function ExecutionLogs() {
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const response = await fetch('/api/logs');
        const data = await response.json();
        setLogs(data.logs);
      } catch (error) {
        console.error('Failed to fetch logs:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
    const interval = setInterval(fetchLogs, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-6 bg-gray-200 rounded"></div>
        ))}
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold">操作记录</h2>
        <span className="text-sm text-gray-500">每30秒自动刷新</span>
      </div>
      
      <div className="space-y-2">
        {logs.map((log, index) => (
          <div
            key={index}
            className="p-3 bg-gray-50 rounded-lg text-sm text-gray-700 font-mono"
          >
            {log}
          </div>
        ))}
      </div>
    </div>
  );
} 