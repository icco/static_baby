# static_baby

Problem: Hosting static sites on Google infrastructure is surprisingly hard.

## Features

 * git push to deploy
 * Auto page-speed analysis and optimizations
 * Easy domain name hookup
 * Built in caching and versioning

## Current Public Google Tools for Static Site Hosting

 * Google Drive
   - Will serve any folder in drive as a website
   - Doesn't support domains
     - http://productforums.google.com/forum/#!topic/drive/Rbk9jNi-9qk
 * Google Cloud Storage
   - Requires you to choose between EU and US hosting
   - Requires some configuration via XML
   - Supports CNAMEs
 * Google Sites
   - It sucks. You know this. I know this.
 * Google App Engine
   - SSL costs $39 a month (cheaper if you use SNI)
   - Requires a little bit of knowledge about App Engine's system to actually deploy
   - https://developers.google.com/appengine/docs/python/gettingstartedpython27/staticfiles
   - Has Git Push to Deploy
