import urllib
import hashlib
import os

import falcon
import requests
import firebase_admin

from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db


class UpdateListener:

    def on_patch(self, req, res):

        doc            = req.context["doc"]
        judul          = doc["judul"]
        profile_x      = doc["profileX"]
        profile_y      = doc["profileY"]
        profile_width  = doc["profileWidth"]
        profile_height = doc["profileHeight"]
        cover_image    = doc["coverImage"]
        list_jawaban   = doc["listJawaban"]

        try:
            cred         = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
            firebase_app = firebase_admin.initialize_app(cred, {
                'storageBucket': 'kuis.zannete.com',
                'databaseURL': 'https://kuis-zannete.firebaseio.com/'
            })
        except ValueError:
            print("Firebase has been initialized")
        bucket = storage.bucket()

        kuis_ref = db.reference("/kuis")

        kuis_ref.set({"judul":judul})
        kuis_ref.child("profileX").set({"profileX":profile_x})
        kuis_ref.child("profileY").set({"profileY":profile_y})
        kuis_ref.child("profileWidth").set({"profileWidth":profile_width})
        kuis_ref.child("profileHeight").set({"profileHeight":profile_height})
        kuis_ref.child("listJawaban").set({"listJawaban":url_list_jawaban})

        req.context["result"] = {"status": {"code": 200, "message": "success"}}
