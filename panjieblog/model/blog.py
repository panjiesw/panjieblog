__author__ = 'panjiesw'


import os
from datetime import datetime
import sys
try:
	from hashlib import sha256
except ImportError:
	sys.exit('ImportError: No module named hashlib\n'
	         'If you are on python2.4 this library is not part of python. '
	         'Please install it. Example: easy_install hashlib')

#__all__ = ['User', 'Group', 'Permission']

from ming import schema as s
from ming.odm import FieldProperty, ForeignIdProperty, RelationProperty
from ming.odm import Mapper
from ming.odm.declarative import MappedClass
from tgming import SynonymProperty, ProgrammaticRelationProperty
import os
from session import DBSession

from auth import User

class Article(MappedClass):
	class __mongometa__:
		session = DBSession
		name = 'article'
		unique_indexes = [('slug',),]
		indexes = [('created_on'),('title'),('tags')]

	_id = FieldProperty(s.ObjectId)
	_category = FieldProperty(s.String)
	_user = FieldProperty(s.String)
	created_on = FieldProperty(s.DateTime,if_missing=datetime.now)
	name = FieldProperty(s.String)
	title = FieldProperty(s.String)
	text = FieldProperty(s.String)
	tags = FieldProperty(s.Array(str))

	def _get_category(self):
		return Page.query.get(cat_name=self._category)
	def _set_category(self,cat):
		self._category = cat
	category = ProgrammaticRelationProperty(Page,_get_category,_set_category)

	def _get_user(self):
		return User.query.get(user_name=self._user)
	def _set_user(self, user):
		self._user = user
	user = ProgrammaticRelationProperty(User, _get_user, _set_user)

	@classmethod
	def by_year(cls, year, dt=datetime.now()):
		act_date = datetime(int(year),1,1)
		fin_date = datetime(int(year)+1,1,1)
		return cls.query.find(
				{
					"$and" : [
								{'created_on':{"$gte":act_date, "$lt":fin_date}},
								{'created_on':{"$lte":dt}}
							]
				}
		).sort({'created_on':-1}).all()

	@classmethod
	def by_year_month(cls, year, month, dt=datetime.now()):
		act_date = datetime(int(year),int(month),1)
		fin_date = datetime(int(year),int(month)+1,1)
		return cls.query.find(
				{
					"$and" : [
								{'created_on':{"$gte":act_date, "$lt":fin_date}},
								{'created_on':{"$lte":dt}}
							]
			}
		).sort({'created_on':-1}).all()

	@classmethod
	def all_posts(cls, dt=datetime.now()):
		return cls.query.find({'created_on':{"$lte":dt}}).sort({'created_on':-1}).limit(5)



class Page(MappedClass):
	class __mongometa__:
		session = DBSession
		name = 'page'
		unique_indexes = [('_cat_name',),]

	_id = FieldProperty(s.ObjectId)
	cat_name = FieldProperty(s.String)
	cat_display = FieldProperty(s.String)

	@property
	def posts(self, dt=datetime.now()):
		return Article.query.find(
				{
				'_category': {"$in": self.cat_name},
				'created_on':{"$lte":dt}
			}
		).sort({'created_on':-1}).limit(5)

	@classmethod
	def categories(cls):
		query = cls.query.find().all()
		cats = {'name': [], 'display': []}
		for que in query :
			if que.cat_name not in cats['name'] :
				cats['name'].append(que.cat_name)
				cats['display'].append(que.cat_display)
		return cats


