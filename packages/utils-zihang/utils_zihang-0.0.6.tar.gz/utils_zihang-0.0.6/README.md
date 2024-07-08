### 项目用法说明

# utils_zihang

`utils_zihang` 是一个工具库，提供一系列常用的工具方法，包括日志记录功能。

## 安装

通过 `pip` 安装：

```bash
pip install utils_zihang
```

## 使用示例

### 日志工具

#### 手动指定日志目录

可以手动指定日志目录：

```python
import os
from utils_zihang.log import setup_logger

# 手动指定日志目录
custom_log_dir = "/path/to/your/custom/log/dir"
log = setup_logger(app_name="my_app", env="DEV", log_dir=custom_log_dir)
log.info("这是一条信息日志")

import uuid

trace_id = str(uuid.uuid4())
log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
log.bind(analysis=True).info("这是一条带有analysis的信息日志")
```

#### 根据环境变量设置日志目录

可以根据环境变量 `ENV` 设置日志目录，环境变量支持 `DEV`, `TEST`, `UAT`, `PROD`：

```python
import os
from utils_zihang.log import setup_logger

# 根据环境变量设置日志路径
env = os.getenv('ENV', 'DEV').upper()
log_dir = os.path.join('logs', env.lower())
os.makedirs(log_dir, exist_ok=True)

log = setup_logger(app_name="my_app", env=env, log_dir=log_dir)
log.info("这是一条信息日志")

import uuid

trace_id = str(uuid.uuid4())
log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
log.bind(analysis=True).info("这是一条带有analysis的信息日志")
```

#### 默认日志目录

在服务器上，默认的日志目录为 `/data/log`，如果不指定日志目录，则日志将保存在该目录下：

```python
import os
from utils_zihang.log import setup_logger

# 不指定日志目录，默认保存在 /data/log
log = setup_logger(app_name="my_app", env="PROD")
log.info("这是一条信息日志")

import uuid

trace_id = str(uuid.uuid4())
log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
log.bind(analysis=True).info("这是一条带有analysis的信息日志")
```

### 完整示例代码

在 `main.py` 中使用 `setup_logger` 函数来配置日志：

```python
import os
from utils_zihang.log import setup_logger

# 根据环境变量设置日志路径
env = os.getenv('ENV', 'DEV').upper()
log_dir = os.path.join('logs', env.lower())
os.makedirs(log_dir, exist_ok=True)

log = setup_logger(app_name="my_app", env=env, log_dir=log_dir)
log.info("这是一条信息日志")

import uuid

trace_id = str(uuid.uuid4())
log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
log.bind(analysis=True).info("这是一条带有analysis的信息日志")
```

## 其他工具

此空间预留用于将来添加其他工具的说明。

## `setup_logger` 函数说明

`setup_logger` 函数用于配置日志记录器，支持以下参数：

- `app_name`：应用名称，用于生成日志文件名。
- `env`：环境名称，如 `DEV`, `TEST`, `UAT`, `PROD`。
- `log_dir`：日志目录路径，默认根据环境变量设置。

日志文件：

- 普通日志：`<app_name>.log`
- 错误日志：`<app_name>-error.log`
- 分析日志：`<app_name>-analysis.log`
