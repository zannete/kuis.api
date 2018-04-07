import os
import time

import falcon
import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

class DisplayListener:
  def on_get(self, req, res, kuis_id, user_id):
    if not "facebookexternalhit/1.1" in req.user_agent:
      raise falcon.HTTPMovedPermanently("https://kuis.zannete.com/kuis/{}".format(kuis_id))
    
  def on_get(self, req, res, kuis_id, user_id):      
    try:
      cred         = credentials.Certificate(os.path.join(os.getcwd(), "serviceAccountKey.json"))
      firebase_app = firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://kuis-zannete.firebaseio.com/'
      }) 
    except ValueError:
      print("Firebase has been initialized")
    
    jawaban_ref = db.reference("/jawaban/{}/{}".format(kuis_id, user_id))
    url_jawaban = jawaban_ref.get()

    kuis_ref   = db.reference("/kuis/{}".format(kuis_id))
    judul_kuis = kuis_ref.child("judul").get()

    res.body = """
    <html>
      <head>
        <meta property="og:url" content="https://api.zannete.com/display/{kuis_id}/{user_id}" />
        <meta property="og:type" content="article" />
        <meta property="og:title" content="{judul}" />
        <meta property="og:description" content="Ayo bermain kuis di Zannete. Kunjungi websitenya, mainkan kuisnya, bagikan dengan teman Anda." />
        <meta property="og:image" content="{url_image}" />
        <meta property="og:image:width" content="1200"/>
        <meta property="og:image:height" content="800"/>
      </head>
    </html>
    """.format(
      kuis_id=kuis_id,
      user_id=user_id,
      judul=judul_kuis,
      url_image=url_jawaban
    )
