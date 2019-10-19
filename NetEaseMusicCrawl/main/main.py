from flask import Flask
from flask import request
import json
import netease
app = Flask(__name__)


@app.route('/')
def getcomment():
    keyword = request.args.get("kw")
    song_id = netease.search_keyword(str(keyword))
    data = netease.details(song_id)
    return json.dumps(data)


if __name__ == 'main':
    app.run()

