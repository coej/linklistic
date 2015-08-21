

from flask import Flask, request, render_template, send_from_directory


app = Flask(__name__)

class Link:
    def __init__(self, path, title):
        if '://' not in path[:10]:
            path = 'http://%s' % path
        self.href = path
        self.title = title


# "Catch-all URL": http://flask.pocoo.org/snippets/57/
@app.route('/', defaults={'submitted_text': ''})
@app.route('/<path:submitted_text>')
def catch_all(submitted_text):

    #if submitted_text.lower()[:8] == 'st_test/':
    #    return './static/' + submitted_text[8:]

    #if submitted_text.lower()[:7] == 'static/':
    #    static_path = submitted_text[7:]
    #    print('fff')
    #    if static_path in ['css/bootstrap.min.css',
    #                       'css/grid.css',
    #                       'css/starter-template.css',
    #                       'img/favicon.ico',
    #                       'js/bootstrap.min.js',
    #                       'js/ie10-viewport-bug-workaround.js',
    #                       'js/jquery.min.js']:
    #    #    return send_from_directory('./static', static_path)
    #    #elif not static_path:
    #    #    return "blank path"
    #    #else:
    #        return "static path not found: " % static_path


    if submitted_text.lower() in ['', 'index.html', 'index.htm']:
        return "Front page here"

    if submitted_text.lower() in ['about', 'about/', 'about.html']:
        return "About page here"

    if submitted_text.lower() in ['usage', 'usage/', 'usage.html']:
        return "Usage page here"

    else:
        links = []

        strings = submitted_text.replace(';;', 'ESCAPED_SEMICOLON_STANDIN')  
        #we'll need more general-purpose escaping to avoid HTML issues with angle brackets etc.

        strings = strings.split(';')
        for s in strings:
            s = s.replace('ESCAPED_SEMICOLON_STANDIN', ';')

            lnk = Link(s, 'some title')
            links.append(lnk)

        # send strings list to jinja template
        return render_template('main.html', links=links)
        #return str(
        #    '<br>'.join(build_output_temp)
        #)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888, debug=True)

