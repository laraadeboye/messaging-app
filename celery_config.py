from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

app.conf.update(
    result_backend='rpc://',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
