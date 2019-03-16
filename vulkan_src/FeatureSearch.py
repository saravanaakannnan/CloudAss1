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

class FEATURESEARCH(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        f_geometry_shader = self.request.get("filter_geometry_shader") == "on"
        f_tesselation_shader = self.request.get("filter_tesselation_shader") == "on"
        f_shaderInt16 = self.request.get("filter_shaderInt16") == "on"
        f_sparse_binding = self.request.get("filter_sparse_binding") == "on"
        f_texture_compressionETC2 = self.request.get("filter_texture_compressionETC2") == "on"
        f_vertex_pipeline_stores = self.request.get("filter_vertex_pipeline_stores") == "on"

        user_array = MyGpu.query()

        if f_geometry_shader:
            user_array = user_array.filter(MyGpu.geometry_shader  == True)

        if f_tesselation_shader:
            user_array = user_array.filter(MyGpu.tesselation_shader == True)

        if f_shaderInt16:
            user_array = user_array.filter(MyGpu.shaderInt16 == True)

        if f_sparse_binding:
            user_array = user_array.filter(MyGpu.sparse_binding == True)

        if f_texture_compressionETC2 :
            user_array = user_array.filter(MyGpu.texture_compressionETC2 == True)

        if f_vertex_pipeline_stores:
            user_array = user_array.filter(MyGpu.vertex_pipeline_stores == True)


        user_array = user_array.fetch()

        template_values = {
            'user_array' : user_array,
            'f_geometry_shader' : f_geometry_shader,
            'f_tesselation_shader' : f_tesselation_shader,
            'f_shaderInt16' : f_shaderInt16,
            'f_sparse_binding' : f_sparse_binding,
            'f_texture_compressionETC2' : f_texture_compressionETC2,
            'f_vertex_pipeline_stores' : f_vertex_pipeline_stores,

            }
        template = JINJA_ENVIRONMENT.get_template('FeatureSearch.html')
        self.response.write(template.render(template_values))
