# utils_zihang

工具方法

## 安装

```bash
pip install utils_zihang
```

## 使用示例

```
from utils_zihang.log import setup_logger

# 示例：指定自定义日志路径

custom_log_dir = "/Users/luzihang/Desktop/LocalProjectHome/utils_zihang/log"
log = setup_logger(app_name="my_app", env="DEV", log_dir=custom_log_dir)
log.info("这是一条信息日志")

import uuid
trace_id = str(uuid.uuid4())
log.bind(trace=trace_id).info("这是一条带有trace的信息日志")
log.bind(trace=trace_id, analysis=True).info("这是一条带有trace和analysis的信息日志")
log.bind(analysis=True).info("这是一条带有analysis的信息日志")
```



