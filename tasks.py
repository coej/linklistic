from celery import Celery
celery_app = Celery('example')

#import os
#app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
#                CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

@celery_app.task
def adder_func(x, y):
    import time
    time.sleep(5)
    return x + y