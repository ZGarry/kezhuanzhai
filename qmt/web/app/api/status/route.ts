import { NextResponse } from 'next/server';

export async function GET() {
  // TODO: 实现实际的状态获取逻辑
  return NextResponse.json({
    isRunning: true,
    lastUpdate: new Date().toLocaleString(),
    tradingDay: true,
    memoryUsage: 45.6,
    cpuUsage: 12.3
  });
} 