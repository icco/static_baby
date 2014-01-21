"""A web app that takes a domain and creates a bucket for that user in their GCS."""

import logging
import json
import os
import cloudstorage as gcs
import webapp2
from webapp2_extras import jinja2

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator

import settings

decorator = OAuth2Decorator(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    scope=settings.SCOPE)
service = build('storage', 'v1beta2')

my_default_retry_params = gcs.RetryParams(
    initial_delay=0.2,
    max_delay=5.0,
    backoff_factor=2,
    max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


class MainPage(webapp2.RequestHandler):

  def render_response(self, template, **context):
    renderer = jinja2.get_jinja2(app=self.app)
    rendered_value = renderer.render_template(template, **context)
    self.response.write(rendered_value)

  @decorator.oauth_aware
  def get(self):
    if decorator.has_credentials():
      result = service.buckets().list().execute(http=decorator.http())
      buckets = result.get('items', [])
      self.render_response('index.html', buckets=buckets)
    else:
      url = decorator.authorize_url()
      self.render_response('index.html', buckets=[], authorize_url=url)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    (decorator.callback_path, decorator.callback_handler()),
    ], debug=True)

# Things to look at:
# https://github.com/GoogleCloudPlatform/storage-appengine-photos-python/blob/master/home.py
# https://developers.google.com/appengine/docs/python/googlecloudstorageclient/
# https://github.com/GoogleCloudPlatform/storage-file-transfer-json-python/blob/master/chunked_transfer.py
# https://github.com/GoogleCloudPlatform/storage-oauth2-tool-python/blob/master/gs-oauth.py
# https://developers.google.com/appengine/docs/python/appidentity/
