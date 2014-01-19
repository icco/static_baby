"""A web app that takes a domain and creates a bucket for that user in their GCS."""

from google.appengine.api import users

import os
import cloudstorage as gcs
import webapp2

my_default_retry_params = gcs.RetryParams(
    initial_delay=0.2,
    max_delay=5.0,
    backoff_factor=2,
    max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)


class MainPage(webapp2.RequestHandler):

  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
