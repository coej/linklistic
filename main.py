
from __future__ import print_function
from flask import Flask, request, render_template, jsonify

from tasks import *

# rendered below closing HTML tag!

# "In Python 2, if you want to uniformly receive all your database input in 
# Unicode, you can register the related typecasters globally as soon as Psycopg is imported:"

# heroku postgres boilerplate
# the environment variable DATABASE_URL has to be set manually on Heroku 
# (e.g., on the app settings page)
# set with: 
# confirm with: heroku config:get DATABASE_URL --app linklistic

# install RabbitMq (binary, apt-get) and Celery (pip) to set up asynchronous background jobs (getting title, getting thumbnail maybe)
# RABBITMQ_BIGWIG_TX_URL etc. were set automatically by the heroku addon install process.

# heroku domains:add www.linklistic.com -a linklistic  (won't point to www.* if not explicitly added)

default_params = {'by': None,
                  'message': None,
                  'title': None,
                  'title_size': 'big',
                  'brand_message': '' #"Turn many links into one link right from your address bar."
                  }

app = Flask(__name__)

class Link:
    def __init__(self, path, title=None, note=None, thumbnail=None):

        def assume_protocol(path):
            if '://' not in path[:10]:
                path = 'http://%s' % path
            return path

        self.href = assume_protocol(path)
        self.note = note
        if title:
            self.title = title
        else:
            self.title = path

    def write(connection):
        pass

# Consider:
# - we can include a self-referential link (localhost:8888/anotherlink.com)
# - we can title the links (maybe)?
# - So: if the format is set up the right way it could be possible to encode 
#   an entire choose-your-own-adventure game into one big URL string...?



## binary insertion (bytea type):
# mypic = open('picture.png', 'rb').read()
# curs.execute("insert into blobs (file) values (%s)", (psycopg2.Binary(mypic),))

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



@app.route('/ajax')
def ajax_test():
    return render_template('ajax_demo.html')
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result = a + b)




@app.route('/')
def site_root():
    return "Front page here"

@app.route('/celery')
def celery_test():
    #from tasks import adder_func
    result = adder_func.delay(3, 4)
    return str(result.status)

@app.route('/database')
def database():
    # SQL_lists = etc. (get title/message/note/etc. information)
    params = default_params.copy() # placeholder values
    submitted_text = '' #placeholder

    SQL_links = "SELECT * FROM Link"
    with conn:
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(SQL_links)
            links = [Link(path=r[1], title=r[2], note=r[3])
                            for r in cursor]

    for link in links:
        print(link.href, link.note)

    return render_template('main.html', links=[str(tup) for tup in enumerate(links)],
                                        by=params['by'],
                                        message=params['message'],
                                        title=params['title'],
                                        brand_message = params['brand_message'],
                                        full_query = submitted_text)
    return str(records)




# "Catch-all URL": http://flask.pocoo.org/snippets/57/
@app.route('/<path:submitted_text>')
def catch_all(submitted_text):
    # '/static/' urls are sent to file system by default

    if submitted_text.lower() in ['about', 'about/', 'about.html']:
        return "About page here"

    if submitted_text.lower() in ['usage', 'usage/', 'usage.html']:
        return "Usage page here"

    links = []
    params = default_params.copy()

    # users must use two semicolons for each semicolon that's in an actual URL to be linked
    strings = submitted_text.replace(';;', 'ESCAPED_SEMICOLON_STANDIN')  
    #we'll need more general-purpose escaping to avoid HTML issues with angle brackets etc.

    strings = strings.split(';')
    for s in strings:

        # functionality for adding commands into the 
        # link list string ("listname:My Bookmarks;http://...")
        
        check_commands = s.split('=')  #, maxsplit=1) py 3 only
        if len(check_commands)>=2:
            key = check_commands[0]
            value = '='.join(check_commands[1:])
            params[key] = value
            continue

        s = s.replace('ESCAPED_SEMICOLON_STANDIN', ';')

        #title = s
        #if len(title) > 77:
        #    title = title[:77] + '...'

        link = Link(path=s)
        links.append(link)

    for link in links:
        commit_raw_link.delay(link.href)


    return render_template('main.html', links=links,
                                        by=params['by'],
                                        message=params['message'],
                                        title=params['title'],
                                        brand_message = params['brand_message'],
                                        full_query = submitted_text)


if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)