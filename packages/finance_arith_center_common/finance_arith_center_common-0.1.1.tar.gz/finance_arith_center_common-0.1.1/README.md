# 工程架构 

finance_arith_center/
│
├── config/                    # 配置文件
│   ├── config.ini             # 配置项，如API密钥、数据库连接等
│   └── ...
├── common/
│   ├── catche/               # 原始数据，如CSV、数据库转储等
│   ├── processed/            # 清洗和处理后的数据
│   └── database/             # 数据库文件，如SQLite数据库
│   └── hdfs5                 # 数据库文件，如hdf5数据库
│
├── engines/                  # 引擎
│   ├── __init__.py            #计算引擎-- 
│   ├── engine_dask.py         # 计算引擎实现
|   ├── engine_gpu.py          # 计算引擎实现
|   ├── engine_c++.py          # 计算引擎实现
|   ├── engine_rust.py         # 计算引擎实现
|   ├── engine_bt.py           # 计算引擎实现
├── strategy/                 # 交易策略
│   ├── __init__.py
│   ├── strategy1.py          # 策略1的实现
│   ├── strategy2.py          # 策略2的实现
│   └── ...
│
├── research/                 # 策略研究和回测
│   ├── __init__.py
│   ├── backtest.py           # 回测框架
│   ├── analyzer.py           # 策略分析工具
│   └── ...
├── scheduler/  
│   ├── __init__.py             # 任务
│   ├── scheduler.py            # 任务配置  心跳轮训 
│   └── ...
│
├── utils/                     # 通用工具和辅助函数
│   ├── __init__.py
│   ├── data_handler.py       # 数据处理工具
│   ├── indicator.py          # 技术指标计算
│   ├── logger.py             # 日志记录工具
│   └── ...
│
├── logs/                      # 日志文件
│   └── ...
│
├── reports/                   # 报告和分析结果，如PDFs、Excel等
│   └── ...
│
├── tests/                     # 测试代码
│   ├── __init__.py
│   ├── test_strategy.py      # 策略测试
│   ├── test_api.py           # API测试
│   └── ...
│
├── main.py                    # 主执行文件，用于启动整个应用
├──.flake8                 # 格式化工具的配置
├──.pre-commit-config.yaml # 格式化工具的配置
├── gen_rpc.sh             # 通过proto文件生成Python gRPC调用代码的脚本
├── mypy.ini               # 格式化工具的配置
├── pyproject.toml         # Python项目配置文件

├── requirements-dev.txt   # 测试环境的依赖文件
├── requirements.txt       # 正式环境的依赖文件
└──


