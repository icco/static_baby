"""A web app that takes a domain and creates a bucket for that user in their GCS."""

import logging
import json
import os
import cloudstorage as gcs
import webapp2
from webapp2_extras import jinja2

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator
from google.appengine.api import users

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

class BasePage(webapp2.RequestHandler):
  """
  Render a template with local variables defined.

  Args:
    template: string. Template name.
    **context: Keywords to be bound as local variables in the template.
  """
  def render_response(self, template, **context):
    renderer = jinja2.get_jinja2(app=self.app)
    rendered_value = renderer.render_template(template, **context)
    self.response.write(rendered_value)


class MainPage(BasePage):

  @decorator.oauth_aware
  def get(self):
    user = users.get_current_user()
    if user and decorator.has_credentials():
      # TODO: Figure out how to get a project list for a user.

      result = service.buckets().list(project).execute(http=decorator.http())
      buckets = result.get('items', [])
      self.render_response('index.html', buckets=buckets)
    else:
      if user:
        self.redirect('/authorize')
      else:
        self.redirect('/login')


class AuthorizePage(BasePage):

  @decorator.oauth_aware
  def get(self):
    user = users.get_current_user()
    if user and decorator.has_credentials():
      self.redirect('/')
    else:
      if user:
        url = decorator.authorize_url()
        self.render_response('authorize.html', authorize_url=url)
      else:
        self.redirect('/login')


class LoginPage(BasePage):

  def get(self):
    user = users.get_current_user()
    if user:
      self.redirect('/')
    else:
      url = users.create_login_url('/')
      self.render_response('login.html', login_url=url)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/authorize', AuthorizePage),
    (decorator.callback_path, decorator.callback_handler()),
    ], debug=True)

# Things to look at:
# https://github.com/GoogleCloudPlatform/storage-appengine-photos-python/blob/master/home.py
# https://developers.google.com/appengine/docs/python/googlecloudstorageclient/
# https://github.com/GoogleCloudPlatform/storage-file-transfer-json-python/blob/master/chunked_transfer.py
# https://github.com/GoogleCloudPlatform/storage-oauth2-tool-python/blob/master/gs-oauth.py
# https://developers.google.com/appengine/docs/python/appidentity/
# https://developers.google.com/api-client-library/python/guide/aaa_oauth
