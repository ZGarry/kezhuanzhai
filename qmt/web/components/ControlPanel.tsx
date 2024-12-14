'use client';

import { useState, useEffect } from 'react';

interface SystemStatus {
  isRunning: boolean;
  lastUpdate: string;
  tradingDay: boolean;
  memoryUsage: number;
  cpuUsage: number;
}

export default function ControlPanel() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      setStatus(data);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStartSystem = async () => {
    try {
      await fetch('/api/control/start', { method: 'POST' });
      fetchStatus();
    } catch (error) {
      console.error('Failed to start system:', error);
    }
  };

  const handleStopSystem = async () => {
    try {
      await fetch('/api/control/stop', { method: 'POST' });
      fetchStatus();
    } catch (error) {
      console.error('Failed to stop system:', error);
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-200 rounded w-1/4"></div>
        <div className="h-32 bg-gray-200 rounded"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">系统控制</h2>
        <div className="flex space-x-4">
          <button
            onClick={handleStartSystem}
            disabled={status?.isRunning}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors
              ${status?.isRunning 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-green-500 hover:bg-green-600'}`}
          >
            启动系统
          </button>
          <button
            onClick={handleStopSystem}
            disabled={!status?.isRunning}
            className={`px-4 py-2 rounded-md text-white font-medium transition-colors
              ${!status?.isRunning 
                ? 'bg-gray-400 cursor-not-allowed' 
                : 'bg-red-500 hover:bg-red-600'}`}
          >
            停止系统
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">系统状态</h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">运行状态</span>
              <span className={status?.isRunning ? 'text-green-500' : 'text-red-500'}>
                {status?.isRunning ? '运行中' : '已停止'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">最后更新</span>
              <span className="text-gray-900">{status?.lastUpdate}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">交易日</span>
              <span className="text-gray-900">{status?.tradingDay ? '是' : '否'}</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <h3 className="text-lg font-medium text-gray-900 mb-4">资源监控</h3>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-gray-600">内存使用</span>
                <span className="text-gray-900">{status?.memoryUsage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${status?.memoryUsage}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-gray-600">CPU使用</span>
                <span className="text-gray-900">{status?.cpuUsage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full" 
                  style={{ width: `${status?.cpuUsage}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 