from flask import Flask, request
import api

app = Flask(__name__)

@app.route('/')
def index():
    return "<h2>Index</h2>"

@app.route("/api", methods=['POST'])
def _api():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        cmd = data['cmd']
        if cmd == 'search':
            param = data['param']
            return api.search(param)
        if cmd == 'chapurl':
            param = data['param']
            return api.chap_urls(param)
        if cmd == 'chapimgs':
            param = data['param']
            return api.chap_imgs(param)
        if cmd == 'chapter':
            param = data['param']
            return api.chapter(param)
        if cmd == 'status':
            param = data['param']
            return api.status(param)
    else:
        return 'Content-Type not supported!'

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4444)
