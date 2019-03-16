import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from mygpu import MyGpu
from datetime import datetime
import commands
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
class Add(webapp2.RequestHandler):
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
# pull the current user from the request

        user = users.get_current_user()

        f_geometry_shader = self.request.get("filter_geometry_shader") == "on"
        f_tesselation_shader = self.request.get("filter_tesselation_shader") == "on"
        f_shaderInt16 = self.request.get("filter_shaderInt16") == "on"
        f_sparse_binding = self.request.get("filter_sparse_binding") == "on"
        f_texture_compressionETC2 = self.request.get("filter_texture_compressionETC2") == "on"
        f_vertex_pipeline_stores = self.request.get("filter_vertex_pipeline_stores") == "on"
        error = 'The GPU name already exists'

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

        user_array = user_array.fetch()

        template_values = {

            'user_array' : user_array,
            'f_geometry_shader' : f_geometry_shader,
            'f_tesselation_shader' : f_tesselation_shader,
            'f_shaderInt16' : f_shaderInt16,
            'f_sparse_binding' : f_sparse_binding,
            'f_texture_compressionETC2' : f_texture_compressionETC2,
            'f_vertex_pipeline_stores' : f_vertex_pipeline_stores,
            'error' : error
            }
        template = JINJA_ENVIRONMENT.get_template('add.html')
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

        if name == mygpu:
            
            return self.response.write("Same name exists")
        else:
            return self.response.write("")

        if mygpu:
            return self.redirect('/')
        mygpu = MyGpu(id = name)
        mygpu.manufacturer = str(self.request.get('users_manufacturer'))
        mygpu.date_issued = datetime.strptime(self.request.get("users_date_issued"),'%Y-%m-%d')
        mygpu.geometry_shader = self.request.get('users_geometry_shader') == "on"
        mygpu.tesselation_shader = self.request.get('users_tesselation_shader') == "on"
        mygpu.shaderInt16 = self.request.get('users_shaderInt16') == "on"
        mygpu.sparse_binding = self.request.get('users_sparse_binding') == "on"
        mygpu.texture_compressionETC2 = self.request.get('users_texture_compressionETC2') == "on"
        mygpu.vertex_pipeline_stores = self.request.get('users_vertex_pipeline_stores') == "on"

        mygpu.put()
        self.redirect('/')
