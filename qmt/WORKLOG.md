# 开发日志

## 已完成功能

### V0版本-2024年11月之前-20%
- [x] 基础框架搭建
- [x] 集思录数据获取模块
- [x] 双低策略实现
- [x] 逆回购策略实现
- [x] 钉钉通知集成
- [x] 基础持仓管理
- [x] 定时任务框架
- [x] 交易日判断

### V1版本-2024年11月19日-25%
- [x] 换手率数据采集
- [x] 系统长期稳定执行
- [x] 集思录数据获取模块深入优化

### V1.5版本-2024年12月8日-支持多策略-30%
- [X] 获取过去五个工作日的换手率
- [X] 优化当前代码，主要是要加入策略模式，为未来代码进一步扩展做准备。还很多代码债务
- [X] 测试模式下验证手段
- [X] 使用换手率等动量因子
- [X] 暂时还没有方法可以获取历史数据，集思录只可以获取当日数据。每日收集数据即可
- [X] 开设多账户，on the way，资金调度公司计算
- [X] 每日最后买入逆回购
- [X] 可转债打新(to do, 待收集他人代码)
- [X] 支持复合策略

### V1.6版本-2024年12月14日-支持多策略-35%
- [X] 减少不必要的xiaohei输出，完善测试模式文案
- [] 探索电脑晚上关机问题。显卡风扇问题
- [X] 显示器息屏（提供了一套代码的解决方案）。电源情况检测。有一些总是唤醒的软件需要移除。电源问题解决了。
- [] 探索复合策略回测
- [] 开设多账户，使用lude，做资金周转
- [X] 研究lude文档。lude的软件也要玩明白（还有很多lude的有价值的内容我没有学走）。还没有针对性的调整账号。
- [X] 逆回购输出日志
- [X] 调整代码，但是暂时不先发布（先维持系统的运行，先不发布，这样系统就一直在运行。这个是停机发布问题）
- [X] 统一日志
- [X] 阅读他人文档


### V1.7版本-2024年12月14日-支持多策略-40%
- [X] 提供对应的网页，用于记录相关内容。先搭建出了网页的空壳子
- [X] 电源问题还是偶尔存在，电源设置总是容易被其他软件所篡改。先保留
- [] 现有模式下做优化
- [X] 个人网站的网络信息记录板块，收集别人有意义的东西;独立有一个页面进行承载，包括个人
- [] 保证委托一定完成
- [] 支持本地回测系统
