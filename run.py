import falcon

from falcon_cors import CORS

from lib.middleware.json_translator import JSONTranslator
from lib.middleware.require_json import RequireJSON
from lib.listener.play import PlayListener
from lib.listener.kuis import KuisListener
from lib.listener.display import DisplayListener
from lib.listener.update import UpdateListener

cors = CORS(allow_all_origins=True, allow_all_headers=True, allow_all_methods=True)
app  = falcon.API(middleware=[
  RequireJSON(),
  JSONTranslator(),
  cors.middleware
])

app.add_route("/kuis", KuisListener())
app.add_route("/play/{kuis_id}", PlayListener())
app.add_route("/display/{kuis_id}/{user_id}", DisplayListener())
app.add_route("/jawaban/kuis/{kuis_id}", UpdateListener())
