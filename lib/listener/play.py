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
  def save_profile_picture_to_storage(self, bucket, access_token, user_id):
    profile_picture_url = "https://graph.facebook.com/v2.5/me/picture?width=1080&access_token={}".format(access_token)
    n_profile_picture   = "{}.jpg".format(hashlib.sha256(profile_picture_url.encode("utf-8")).hexdigest())
    urllib.request.urlretrieve(profile_picture_url, os.path.join(os.getcwd(), "tmpImage", n_profile_picture))
    
    print("Saving to GStorage: {}".format(n_profile_picture))
    b_profile_picture = bucket.blob("{}/{}".format("pengguna", n_profile_picture))
    b_profile_picture.upload_from_file(open(os.path.join(os.getcwd(), "tmpImage", n_profile_picture), "rb"), content_type="image/jpeg")
    b_profile_picture.make_public()
    
    return (b_profile_picture.public_url, n_profile_picture)
  
  def update_profile_picture_database(self, user_id, email, url_profile_picture):
    # Double check apakah profile picture pernah disave sebelumnya
    # Jika pernah maka tambah profile picture, jika belum ya tambah biasa aja si
    user_ref  = db.reference("/user/{}".format(user_id))
    user_data = user_ref.get()
    if user_data is None:
      user_ref.set({
        "email": email
      })
    
    profile_picture_ref  = user_ref.child("profilePicture")
    profile_picture_data = profile_picture_ref.get()
    profile_picture_data = {} if profile_picture_data is None else profile_picture_data
    duplicate            = False
    for key, value in profile_picture_data.items():
      if value == url_profile_picture:
        duplicate = True
    if not duplicate:
      print("New profile picture added!")
      new_profile_picture_ref = profile_picture_ref.push()
      new_profile_picture_ref.set(url_profile_picture)
  
  def on_post(self, req, res, kuis_id):
    doc          = req.context["doc"]
    access_token = doc["accessToken"]
    user_id      = doc["userId"]
    email        = doc["email"]
    
    try:
      cred         = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
      firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'kuis.zannete.com',
        'databaseURL': 'https://kuis-zannete.firebaseio.com/'
      })
    except ValueError:
      print("Firebase has been initialized")
    bucket = storage.bucket()
    
    bucket                                 = storage.bucket()
    url_profile_picture, n_profile_picture = self.save_profile_picture_to_storage(bucket, access_token, user_id)
    self.update_profile_picture_database(user_id, email, url_profile_picture)

    jawaban_ref      = db.reference("/jawaban")
    existing_jawaban = jawaban_ref.child(kuis_id).child(user_id).get()
    reprocess        = True if existing_jawaban is None else False
    print("Re-Processing: {}".format(reprocess))
    if reprocess:
      kuis_ref             = db.reference("/kuis/{}".format(kuis_id))
      list_jawaban         = kuis_ref.child("listJawaban").get()
      profile_x            = int(kuis_ref.child("profileX").get())
      profile_y            = int(kuis_ref.child("profileY").get())
      profile_width        = int(kuis_ref.child("profileWidth").get())
      profile_height       = int(kuis_ref.child("profileHeight").get())
      url_terpilih_jawaban = list_jawaban[random.randrange(0, len(list_jawaban))]
      n_terpilih_jawaban   = "{}{}".format(user_id, url_terpilih_jawaban)
      n_terpilih_jawaban   = "{}.jpg".format(hashlib.sha256(n_terpilih_jawaban.encode("utf-8")).hexdigest())
      urllib.request.urlretrieve(url_terpilih_jawaban, os.path.join(os.getcwd(), "tmpImage", n_terpilih_jawaban))
      
      i_profile_picture  = Image.open(open(os.path.join(os.getcwd(), "tmpImage", n_profile_picture), "rb"))
      i_profile_picture  = resizeimage.resize_cover(i_profile_picture, [profile_width, profile_height])
      i_terpilih_jawaban = Image.open(open(os.path.join(os.getcwd(), "tmpImage", n_terpilih_jawaban), "rb"))
      i_terpilih_jawaban.paste(i_profile_picture, (profile_x, profile_y, profile_x + profile_width, profile_y + profile_height))
      i_terpilih_jawaban.save(os.path.join(os.getcwd(), "tmpImage", n_terpilih_jawaban))
      
      b_terpilih_jawaban = bucket.blob("{}/{}".format("jawaban", n_terpilih_jawaban))
      b_terpilih_jawaban.upload_from_file(open(os.path.join(os.getcwd(), "tmpImage", n_terpilih_jawaban), "rb"), content_type="image/jpeg")
      b_terpilih_jawaban.make_public()
      url_terpilih_jawaban = b_terpilih_jawaban.public_url
      
      jawaban_ref = db.reference("/jawaban")
      jawaban_ref.child(kuis_id).child(user_id).set(url_terpilih_jawaban)
      os.remove(os.path.join(os.getcwd(), "tmpImage", n_terpilih_jawaban))
    os.remove(os.path.join(os.getcwd(), "tmpImage", n_profile_picture))
