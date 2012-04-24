# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in panjieblog.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig

import panjieblog
from panjieblog import model
from panjieblog.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []
base_config.prefer_toscawidgets2 = True

base_config.package = panjieblog

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer = 'jinja'
base_config.renderers.append('jinja')
base_config.renderers.append('mako')
base_config.jinja_extensions = ['jinja2.ext.with_']
#base_config.use_dotted_templatenames = False
#Configure the base Ming Setup
base_config.use_ming = True
base_config.use_sqlalchemy=False
base_config.use_transaction_manager=False
# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP 
base_config.sa_auth.cookie_secret = "ChangeME" 

base_config.auth_backend = 'ming'

# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.User

# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# override this if you are using a different charset for the login form
base_config.sa_auth.charset = 'utf-8'

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'
