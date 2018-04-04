import os
import base64
import hashlib

import falcon
import firebase_admin

from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

class KuisListener:
  def save_image_to_firebase(self, bucket, folder, image_data):
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
  
  def on_post(self, req, res):
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
    
    url_cover_image = self.save_image_to_firebase(bucket, "coverImage", cover_image)
    doc.update({"coverImage": url_cover_image})
    
    url_list_jawaban = []
    for jawaban in list_jawaban:
      url_jawaban = self.save_image_to_firebase(bucket, "jawabanImage", jawaban)
      url_list_jawaban.append(url_jawaban)
    doc.update({"listJawaban": url_list_jawaban})
    
    kuis_ref     = db.reference('/kuis')
    new_kuis_ref = kuis_ref.push()
    new_kuis_ref.set(doc)
    
    req.context["result"] = {"status": {"code": 200, "message": "success"}}