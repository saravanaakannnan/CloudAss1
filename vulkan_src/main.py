import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from add import Add
from editGPU import EDITGPU
from GPUinfo import GPUINFO
from mygpu import MyGpu
from CompareGPU import COMPAREGPU
from FeatureSearch import FEATURESEARCH
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        f_geometryShader = "False"
        f_tesselationShader = "False"
        f_shaderInt16 = "False"
        f_sparseBinding = "False"
        f_textureCompressionETC2 = "False"
        f_vertexPipelineStoresAndAtomics = "False"
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        f_geometry_shader = self.request.get("filter_geometry_shader") == "on"
        f_tesselation_shader = self.request.get("filter_tesselation_shader") == "on"
        f_shaderInt16 = self.request.get("filter_shaderInt16") == "on"
        f_sparse_binding = self.request.get("filter_sparse_binding") == "on"
        f_texture_compressionETC2 = self.request.get("filter_texture_compressionETC2") == "on"
        f_vertex_pipeline_stores = self.request.get("filter_vertex_pipeline_stores") == "on"

        user_array = MyGpu.query()

        if f_geometry_shader:
            user_array = user_array.filter(MyUser.geometry_shader  == True)

        if f_tesselation_shader:
            user_array = user_array.filter(MyUser.tesselation_shader == True)

        if f_shaderInt16:
            user_array = user_array.filter(MyUser.shaderInt16 == True)

        if f_sparse_binding:
            user_array = user_array.filter(MyUser.sparse_binding == True)

        if f_texture_compressionETC2 :
            user_array = user_array.filter(MyUser.texture_compressionETC2 == True)

        if f_vertex_pipeline_stores:
            user_array = user_array.filter(MyUser.vertex_pipeline_stores == True)

        #if f_atomics:
            #user_array = user_array.filter(MyUser.atomics == True)
        #user_array = user_array.fetch()

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'user_array' : user_array,

            }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        #url = ''
        #url_string = ''
        #welcome = 'Welcome back'

        user = users.get_current_user()

        if not user:
            return self.redirect("/")

        name = self.request.get('users_name')

        mygpu_key = ndb.Key('MyGpu', name)
        mygpu = mygpu_key.get()

        if myuser:
            return self.redirect("/")


app = webapp2.WSGIApplication([
('/', MainPage),
('/add', Add),
('/GPUinfo', GPUINFO),
('/editGPU', EDITGPU),
('/CompareGPU', COMPAREGPU),
('/FeatureSearch',FEATURESEARCH)
], debug=True)
