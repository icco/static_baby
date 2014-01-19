# static_baby

Problem: Hosting static sites on Google infrastructure is surprisingly hard.

## Features

 * git push to deploy
 * Auto page-speed analysis and optimizations
 * Easy domain name hookup
 * Built in caching and versioning

## Google Tools for Static Site Hosting

This does not include competitors or internal tools Google developers have access to.

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
   - Some people have built similar things already
     - http://drydrop.binaryage.com/

## Proposed Flow

 1. User logs into an app engine app.
 2. App asks the user to define a domain.
 3. After user puts in a domain, app returns settings for user to put in their DNS and a git repo to push to.
 4. User runs `git remote add google git://blahhhhhhh.git` to add Google as a push point for their static site.
 5. User runs `git push google master` to deploy
 6. User vists <http://www.example.com/> and sees their website up to date with the new push.
 7. User recieves an email with suggestions on how to improve their site with page-speed, and the changes the page speed system did automatically.

For returning users repeat steps five through seven.
