

from flask import Flask, request, render_template


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
        params = {'from': None,
                  'message': "Broken links? It's not our fault.",
                  'title': "Your links are listed below."}

        # users must use two semicolons for each semicolon that's in an actual URL to be linked
        strings = submitted_text.replace(';;', 'ESCAPED_SEMICOLON_STANDIN')  
        #we'll need more general-purpose escaping to avoid HTML issues with angle brackets etc.

        strings = strings.split(';')
        for s in strings:

            # functionality for adding commands into the 
            # link list string ("listname:My Bookmarks;http://...")
            
            check_commands = s.split('=', maxsplit=1)
            if len(check_commands)==2:
                key = check_commands[0]
                value = check_commands[1]
                params[key] = value

            s = s.replace('ESCAPED_SEMICOLON_STANDIN', ';')

            title = s
            if len(title) > 77:
                title = title[:77] + '...'

            lnk = Link(path=s, title=title)
            links.append(lnk)

        # send Link list to jinja template
        return render_template('main.html', links=links, 
                                            list_from=params['from'],
                                            message=params['message'],
                                            title=params['title'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)

