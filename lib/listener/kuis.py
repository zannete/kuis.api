import os

import falcon
import firebase_admin

from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

class KuisListener:

    def on_post(self, req, res):
        doc            = req.context["doc"]
        judul          = doc["judul"]
        profile_x      = doc["profileX"]
        profile_y      = doc["profileY"]
        profile_width  = doc["profileWidth"]
        profile_height = doc["profileHeight"]

        try:
            cred         = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
            firebase_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://kuis-zannete.firebaseio.com/'
          })
        except ValueError:
            print("Firebase has been initialized")


        kuis_ref     = db.reference('/kuis')
        new_kuis_ref = kuis_ref.push()
        new_kuis_ref.set(doc)

        req.context["result"] = {"status": {"code": 200, "message": "success"}}
