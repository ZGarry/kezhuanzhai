export default function Documentation() {
  return (
    <div className="prose max-w-none">
      <h2 className="text-xl font-semibold mb-6">系统文档</h2>
      
      <div className="space-y-8">
        <section>
          <h3 className="text-lg font-medium text-gray-900">功能特性</h3>
          <ul className="mt-4 space-y-2 text-gray-600">
            <li className="flex items-center">
              <span className="w-4 h-4 mr-2 text-green-500">✓</span>
              自动化双低策略执行
            </li>
            <li className="flex items-center">
              <span className="w-4 h-4 mr-2 text-green-500">✓</span>
              剩余资金逆回购操作
            </li>
            <li className="flex items-center">
              <span className="w-4 h-4 mr-2 text-green-500">✓</span>
              实时持仓监控
            </li>
            <li className="flex items-center">
              <span className="w-4 h-4 mr-2 text-green-500">✓</span>
              自动化数据采集
            </li>
            <li className="flex items-center">
              <span className="w-4 h-4 mr-2 text-green-500">✓</span>
              钉钉消息通知
            </li>
          </ul>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-900">数据来源</h3>
          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium">集思录</h4>
              <p className="text-sm text-gray-600 mt-1">可转债基础数据、换手率等</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium">迅投QMT</h4>
              <p className="text-sm text-gray-600 mt-1">交易接口、账户信息</p>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-medium">akshare</h4>
              <p className="text-sm text-gray-600 mt-1">交易日历等基础数据</p>
            </div>
          </div>
        </section>

        <section>
          <h3 className="text-lg font-medium text-gray-900">开发进度</h3>
          <div className="mt-4 space-y-4">
            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">V0版本</span>
                <span className="text-sm text-gray-500">20%</span>
              </div>
              <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '20%' }}></div>
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-900">V1版本</span>
                <span className="text-sm text-gray-500">40%</span>
              </div>
              <div className="mt-1 w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: '40%' }}></div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
} 