# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_
from panjieblog import model
from repoze.what import predicates
from panjieblog.controllers.secure import SecureController
from panjieblog.admin.mongo import PJMongoAdminConfig
from panjieblog.admin.controller import AdminController
from datetime import datetime
#from tgext.admin.mongo import TGMongoAdminConfig
#from tgext.admin.controller import AdminController

from panjieblog.lib.base import BaseController
from panjieblog.controllers.error import ErrorController

__all__ = ['RootController']


class RootController(BaseController):
	"""
	The root controller for the panjieblog application.

	All the other controllers and WSGI applications should be mounted on this
	controller. For example::

		panel = ControlPanelController()
		another_app = AnotherWSGIApplication()

	Keep in mind that WSGI applications shouldn't be mounted directly: They
	must be wrapped around with :class:`tg.controllers.WSGIAppController`.

	"""
	secc = SecureController()
	admin = AdminController(model, None, config_type=PJMongoAdminConfig)

	error = ErrorController()
	@expose('index.html')
	def index(self, previous=None):
		"""Handle the front-page."""
		cat = model.Page.categories()
		allposts = None
		last_date_string = None
		if not previous:
			allposts = model.Article.all_posts()
		else:
			allposts = model.Article.all_posts(datetime.strptime(previous,"%Y-%m-%d"))
		if len(allposts) >= 5 :
			last_date_string = allposts[4].created_on.strftime("%Y-%m-%d")
		return dict(page='index', categories=cat, posts=allposts, next_ent=last_date_string)

	@expose('about.html')
	def about(self):
		"""Handle the 'about' page."""
		return dict(page='about')

	@expose('login.html')
	def login(self, came_from=lurl('/')):
		"""Start the user login."""
		login_counter = request.environ['repoze.who.logins']
		if login_counter > 0:
			flash(_('Wrong credentials'), 'warning')
		return dict(page='login', login_counter=str(login_counter),
					came_from=came_from)

	@expose()
	def post_login(self, came_from=lurl('/')):
		"""
		Redirect the user to the initially requested page on successful
		authentication or redirect her back to the login page if login failed.

		"""
		if not request.identity:
			login_counter = request.environ['repoze.who.logins'] + 1
			redirect('/login',
				params=dict(came_from=came_from, __logins=login_counter))
		userid = request.identity['repoze.who.userid']
		flash(_('Welcome back, %s!') % userid)
		redirect(came_from)

	@expose()
	def post_logout(self, came_from=lurl('/')):
		"""
		Redirect the user to the initially requested page on logout and say
		goodbye as well.

		"""
		flash(_('We hope to see you soon!'))
		redirect(came_from)


class BlogControllerEntry(object):
	def __init__(self, dt, name):
		self.entry = model.Article.query.get(created_on=dt, name=name)
		self.cat = model.Page.categories()

	@expose('post.html')
	def index(self):
		return dict(page='index', categories=self.cat, post=self.entry)


