'use client';

import { useState } from 'react';
import Tabs from '@/components/Tabs';
import Documentation from '@/components/Documentation';
import ExecutionLogs from '@/components/ExecutionLogs';
import ControlPanel from '@/components/ControlPanel';

export default function Home() {
  const [activeTab, setActiveTab] = useState('control');

  const tabs = [
    { id: 'control', label: '控制面板' },
    { id: 'logs', label: '操作记录' },
    { id: 'documentation', label: '系统文档' }
  ];

  const renderContent = () => {
    switch(activeTab) {
      case 'control':
        return <ControlPanel />;
      case 'logs':
        return <ExecutionLogs />;
      case 'documentation':
        return <Documentation />;
      default:
        return <ControlPanel />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">齿轮系统</h1>
            <div className="text-sm text-gray-500">
              可转债交易管理平台
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow">
          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} />
          <div className="p-6">
            {renderContent()}
          </div>
        </div>
      </main>
    </div>
  );
} 