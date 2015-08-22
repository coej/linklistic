from celery import Celery

# Locally on windows:
# $ rabbitmqctl add_user chris password999
# $ rabbitmqctl add_vhost linklistic
# $ rabbitmqctl set_permissions -p linklistic chris ".*" ".*" ".*"

# so then we run THIS FILE, tasks.py, with:  ('tasks' below refers to this filename)
#celery -A tasks worker --loglevel=info

# presumably we'd want the name/pass to be an environment variable eventually
BROKER_URL = 'amqp://chris:password999@localhost:5672/linklistic'
CELERY_RESULT_BACKEND = 'amqp'
CELERYD_STATE_DB = "c:/db/celery/celery_worker_state" 
celery_app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=BROKER_URL)

# do we put this here??
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
import os
import urlparse
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

from psycopg2.extras import DictCursor
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port)


@celery_app.task
def adder_func(x, y):
    import time
    time.sleep(5)
    print (x + y)
#run as adder_func.delay(1,2)  # "delay" queues it instead of running immediately

@celery_app.task
def commit_raw_link(href):
    import psycopg2

    SQL = '''
        INSERT INTO Link (href, title, note) 
        SELECT LOWER(%s), %s, %s
        WHERE NOT EXISTS (
            select * from Link where LOWER(href) = LOWER(%s)
        );
    '''
    format_items = (href, None, None, href)

    print (SQL % format_items)

    with conn.cursor() as cur:
        cur.execute(SQL, format_items)
        try:
            result = cur.fetchall()
            print(str(result))
        except:
            pass
        conn.commit()
    


@celery_app.task
def save_page_title(href):
    import requests
    from bs4 import BeautifulSoup
    import psycopg2
    cur = conn.cursor()
    cur.execute('select * from Link')
    conn.commit()


@celery_app.task
def read_me(href):
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('select * from Link')
    try: 
        x = cur.fetchone()
        print(str(x))
    except:
        print("couldn't fetchone()")
