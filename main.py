"""A web app that takes a domain and creates a bucket for that user in their GCS."""

import logging
import json
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import oauth
from google.appengine.api import app_identity
from google.appengine.api import urlfetch

my_default_retry_params = gcs.RetryParams(
    initial_delay=0.2,
    max_delay=5.0,
    backoff_factor=2,
    max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


class MainPage(webapp2.RequestHandler):

  def get(self):
    user = oauth.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

# Things to look at:
# https://github.com/GoogleCloudPlatform/storage-appengine-photos-python/blob/master/home.py
# https://developers.google.com/appengine/docs/python/googlecloudstorageclient/
# https://github.com/GoogleCloudPlatform/storage-file-transfer-json-python/blob/master/chunked_transfer.py
# https://github.com/GoogleCloudPlatform/storage-oauth2-tool-python/blob/master/gs-oauth.py
# https://developers.google.com/appengine/docs/python/appidentity/
