import urllib
import hashlib
import os
import random

import falcon
import requests
import firebase_admin

from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db


class UpdateListener:

    def on_patch(self, req, res, kuis_id):

        doc            = req.context["doc"]
        judul          = doc["judul"]
        profile_x      = doc["profileX"]
        profile_y      = doc["profileY"]
        profile_width  = doc["profileWidth"]
        profile_height = doc["profileHeight"]

        try:
            cred         = credentials.Certificate(os.path.join(os.getcwd(), "service.json"))
            firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://coba-d5c28.firebaseio.com//'
            })
        except ValueError:
            print("Firebase has been initialized")

        kuis_ref = db.reference("/kuis/{}".format(kuis_id))

        kuis_ref.set({"judul":judul})
        kuis_ref.child("profileX").set({"profileX":profile_x})
        kuis_ref.child("profileY").set({"profileY":profile_y}) kuis_ref.child("profileWidth").set({"profileWidth":profile_width}) kuis_ref.child("profileHeight").set({"profileHeight":profile_height})

        req.context["result"] = {"status": {"code": 200, "message": "success"}}
