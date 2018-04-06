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
from PIL import Image
from resizeimage import resizeimage

# ACCESS_TOKEN = "EAAWmo0Rm7kIBAGvSGxQ6pKzWocXlUZCANiZBO4aMfSJAyiJiU1js9F6zJNpIIpwDrQ1M8sFEYf3NsZCea6QeiAWTFZArVLjaG9WN0B2OugfMnZAlMm9jtnItY8GO3kuNRp2a3OiOuV1ytZBkMGwpH53q1c9pfAEQMZAC3q8VkAiiiB4UICw2Yz380wZBCCXbvB0ZD"
# USER_ID      = "c7zM4CsSjMhpMZFaR0kq7NQDW483"
# EMAIL        = "franssiswanto@gmail.com"

class PlayListener:

    def update_profile_picture_database(self, user_id, email, url_profile_picture):
        # Double check apakah profile picture pernah disave sebelumnya
        # Jika pernah maka tambah profile picture, jika belum ya tambah biasa aja si
        user_ref  = db.reference("/user/{}".format(user_id))
        user_data = user_ref.get()
        if user_data is None:
            user_ref.set({
                "email": email
          })

        
    def on_post(self, req, res, kuis_id):
        doc          = req.context["doc"]
        access_token = doc["accessToken"]
        user_id      = doc["userId"]
        email        = doc["email"]
    
        try:
            cred         = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
            firebase_app = firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://kuis-zannete.firebaseio.com/'
            })
        except ValueError:
            print("Firebase has been initialized")

        jawaban_ref      = db.reference("/jawaban")
        existing_jawaban = jawaban_ref.child(kuis_id).child(user_id).get()
        reprocess        = True if existing_jawaban is None else False
        print("Re-Processing: {}".format(reprocess))
        if reprocess:
            kuis_ref             = db.reference("/kuis/{}".format(kuis_id))
            profile_x            = int(kuis_ref.child("profileX").get())
            profile_y            = int(kuis_ref.child("profileY").get())
            profile_width        = int(kuis_ref.child("profileWidth").get())
            profile_height       = int(kuis_ref.child("profileHeight").get())

