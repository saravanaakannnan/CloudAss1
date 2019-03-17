import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)

class GPUINFO(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
		url = ''
		url_string = ''
		welcome = 'Welcome back'

		# pull the current user from the request
		user = users.get_current_user()

		if user:
			url = users.create_logout_url("/")
			url_string = 'logout'

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'

		name = self.request.get('name')
		mygpu_key = ndb.Key('MyGpu',name)
		mygpu = mygpu_key.get()

		if mygpu is None:
			self.redirect("/")

		template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
			'gpu_array' : MyGpu.query().fetch(),
			'mygpu' : mygpu
		}

        # pull the template file and ask jinja to render
        # it with the given template values
		template = JINJA_ENVIRONMENT.get_template('GPUinfo.html')
		self.response.write(template.render(template_values))


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'

		# URL that will contain a login or logout link
		# and also a string to represent this
		url = ''
		url_string = ''
		welcome = 'Welcome back'

		# pull the current user from the request
		user = users.get_current_user()

		if not user:
			return self.redirect("/")

		if self.request.get("cancel"):
			return self.redirect("/")

		name = self.request.get('name')

		mygpu_key = ndb.Key('MyGpu',name)
		mygpu = mygpu_key.get()
		mygpu.geometry_shader = self.request.get('geometry_shader') == "on"
		mygpu.tesselation_shader = self.request.get('tesselation_shader') == "on"
		mygpu.shaderInt16 = self.request.get('shaderInt16') == "on"
		mygpu.sparse_binding = self.request.get('sparse_binding') == "on"
		mygpu.texture_compressionETC2 = self.request.get('texture_compressionETC2') == "on"
		mygpu.vertex_pipeline_stores = self.request.get('vertex_pipeline_stores') == "on"


		mygpu.put()

		self.redirect("/")
