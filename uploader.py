import logging
from google.appengine.ext import db, blobstore, webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images

def find_image_by_name(handle):
    result = db.GqlQuery("SELECT * FROM TestImage WHERE name = :1 LIMIT 1",
        handle).fetch(1)
    if (len(result) > 0):
        return result[0]
    else:
        return None

class TestImage(db.Model):
    name = db.StringProperty(required=True)
    blob_key = blobstore.BlobReferenceProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)

class TestImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(blobstore.create_upload_url('/image/submit'))

    def post(self):
        name = self.request.get("name")
        blob_info = self.get_uploads()[0]
        image = TestImage(name=name, blob_key=blob_info.key())
        image.put()
        logging.info("Uploaded image named %s" % name)
        logging.info("Uploaded data %s" % self.request.__dict__)
        self.redirect("/image/%s.png" % name)



class TestOneStepImageUploadHandler(webapp.RequestHandler):

    def post(self):    
        
        name = self.request.get("name")
        img = request.get("image")
        
        image = TestImage(name=name, blob_key=blob_info.key())
        image.put()



        img.put()
        if (self.request.get("return")):
            # this was submitted by a form
            self.redirect(self.request.get("return"))
        else:
            # this was submitted by an API client

            response = { 'handle': img.handle, 'created_at': img.created_at.isoformat() }
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps(response))

class TestImageServer(webapp.RequestHandler):

    def get(self, name):
        image = find_image_by_name(name)
        logging.info("Got image %s for name %s" % (image, name))
        if image:
            image_url = images.get_serving_url(str(image.blob_key.key()))
            self.redirect(image_url, permanent=True)
        else:
            self.redirect("/static/broken.png")

if __name__ == "__main__":
    application = webapp.WSGIApplication(
        [
            ('/image/([^/]+)\.png', TestImageServer),
            ('/image/submit', TestImageUploadHandler),
         ], debug=True)
    run_wsgi_app(application)
                          