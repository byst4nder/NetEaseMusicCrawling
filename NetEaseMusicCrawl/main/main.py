from flask import Flask
from flask import request
import json
import netease
app = Flask(__name__)


@app.route('/getRtComments')
def getRtComment():
    keyword = request.args.get("kw")
    song_id = netease.search_keyword(str(keyword))
    data = netease.getRTComments(song_id)
    return json.dumps(data)

@app.route('/getHotComments')
def getHotComment():
    keyword = request.args.get("kw")
    song_id = netease.search_keyword(str(keyword))
    data = netease.getHotComments(song_id)
    return json.dumps(data)
if __name__ == 'main':
    app.run()

