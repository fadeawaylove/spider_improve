import os

# 启动一个celery的worker工作进程
# -A 指定要运行的任务模块
# -l 执行log日志等级
# -P gevent表明使用gevent来运行任务
os.system("celery worker -A tasks -l info -P gevent")

