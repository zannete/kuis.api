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


class UpdateListener(object):

  def save_image(self,bucket,folder,image_data):
      image_data   = image_data.split("data:image/jpeg;base64,")[1]
      n_image_data = "{}.jpg".format(hashlib.sha256(image_data.encode("utf-8")).hexdigest())
      f_image_data = open(os.path.join(os.getcwd(), "tmpImage", n_image_data), "wb")
      f_image_data.write(base64.decodestring(image_data.encode("utf-8")))
      f_image_data.close()

      b_image_data = bucket.blob("{}/{}".format(folder, n_image_data))
      b_image_data.upload_from_file(open(os.path.join(os.getcwd(), "tmpImage", n_image_data), "rb"), content_type="image/jpeg")
      b_image_data.make_public()

      os.remove(os.path.join(os.getcwd(), "tmpImage", n_image_data))
      return b_image_data.public_url

  def on_post(self, req, res, kuis_id):

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

    kuis_ref = db.reference("/jawaban/kuis/{}".format(kuis_id))

    cek = input("cek Id: ")

    if cek in kuis_ref.child(kuis_id).get().values():
      update_judul = input("Masukkan Judul: ")
      kuis_ref.set({"judul":update_judul})
      url_cover_image = self.save_image(bucket, "coverImage", cover_image)
      kuis_ref.set({"coverImage":url_cover_image})
      update_profile_x = input("Masukkan Profile X: ")
      kuis_ref.child("profileX").set({"profileX":update_profile_x})
      update_profile_y = input("Masukkan Profile Y: ")
      kuis_ref.child("profileY").set({"profileY":update_profile_y})
      update_profile_width = input("Masukkan Profile width: ")
      kuis_ref.child("profileWidth").set({"profileWidth":update_profile_width})
      update_profile_height = input("Masukkan Profile height: ")
      kuis_ref.child("profileHeight").set({"profileHeight":update_profile_height})
      update_list_jawaban = input("update_list_jawaban: ")
      url_list_jawaban = []
      for jawaban in update_list_jawaban:
          url_jawaban = self.save_image(bucket, "jawabanImage", jawaban)
          url_list_jawaban.append(url_jawaban)
      kuis_ref.child("listJawaban").set({"listJawaban":url_list_jawaban})

      req.context["result"] = {"status": {"code": 200, "message": "success"}}
    if __name__ == "__main__":
        save_image(self, 1, 1, "image_data")
        on_post(self, 1, 200, 1)
