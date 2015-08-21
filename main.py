
from __future__ import print_function
from flask import Flask, request, render_template

default_params = {'by': None,
                  'message': None,
                  'title': None,
                  'title_size': 'big',
                  'brand_message': "Turn many links into one link right from your browser's address bar."}

app = Flask(__name__)

class Link:
    def __init__(self, path, title=None, note=None):
        if title: 
            self.title = title
        else:
            self.title = path
        if '://' not in path[:10]:
            path = 'http://%s' % path
        self.href = path
        self.note = ''

# Consider:
# - we can include a self-referential link (localhost:8888/anotherlink.com)
# - we can title the links (maybe)?
# - So: if the format is set up the right way it could be possible to encode 
#   an entire choose-your-own-adventure game into one big URL string...?

# "Catch-all URL": http://flask.pocoo.org/snippets/57/
@app.route('/', defaults={'submitted_text': ''})
@app.route('/<path:submitted_text>')
def catch_all(submitted_text):
    # '/static/' urls are sent to file system by default

    if submitted_text.lower() in ['', 'index.html', 'index.htm']:
        return "Front page here"

    if submitted_text.lower() in ['about', 'about/', 'about.html']:
        return "About page here"

    if submitted_text.lower() in ['usage', 'usage/', 'usage.html']:
        return "Usage page here"

    else:
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

            title = s
            if len(title) > 77:
                title = title[:77] + '...'

            lnk = Link(path=s, title=title)
            links.append(lnk)

        # send Link list to jinja template

        return render_template('main.html', links=links, 
                                            by=params['by'],
                                            message=params['message'],
                                            title=params['title'],
                                            brand_message = params['brand_message'])

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)