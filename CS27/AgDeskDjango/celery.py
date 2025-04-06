from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置默认的 Django settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgDeskDjango.settings')

app = Celery('AgDeskDjango')

# 从 Django 的 settings.py 中读取配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')