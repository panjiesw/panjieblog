from pylons import tmpl_context
from tg.decorators import without_trailing_slash

__author__ = 'panjiesw'

from tg import expose, redirect
from panjieblog.crud.controller import CrudRestController
from panjieblog.widgets.form import CustomForm, CustomAddRecordForm
from tgext.crud.decorators import registered_validate
from config import AdminConfig, CrudRestControllerConfig
from sprox.fillerbase import EditFormFiller
from sprox.formbase import FilteringSchema
from formencode.validators import FieldsMatch
from tw2.forms import TextField, PasswordField, TextArea, SingleSelectField
from tgext.crud.utils import SortableTableBase as TableBase
from panjieblog import model

from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm, EditableForm
from sprox.widgets.tw2widgets.widgets import PropertySingleSelectField

from sprox.fillerbase import RecordFiller, AddFormFiller

class UserControllerConfig(CrudRestControllerConfig):
	def _do_init_with_translations(self, translations):
		user_id_field      = translations.get('user_id',       'user_id')
		user_name_field    = translations.get('user_name',     'user_name')
		email_field        = translations.get('email_address', 'email_address')
		password_field     = translations.get('password',      'password')
		display_name_field = translations.get('display_name',  'display_name')
		group_name_field     = translations.get('group_name', 'group_name')

		if not getattr(self, 'table_type', None):
			class Table(TableBase):
				__entity__ = self.model
				__omit_fields__ = [user_id_field, '_groups', '_password', password_field]
				__url__ = '../users.json'
			self.table_type = Table

		if not getattr(self, 'table_filler_type', None):
			class MyTableFiller(TableFiller):
				__entity__ = self.model
				__omit_fields__ = ['_password', password_field]
				def __actions__(self, obj):
					primary_fields = self.__provider__.get_primary_fields(self.__entity__)
					pklist = 'users/'+'/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
					value = '<a id="btn_edit" class="btn btn-warning" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                   '<form style="display:inline; margin-left:10px;" method="POST" action="'+pklist+'">'\
                   '<input type="hidden" name="_method" value="DELETE" />'\
                   '<input class="btn btn-danger" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" />'\
                   '</form>'
					return value
			self.table_filler_type = MyTableFiller

		if hasattr(TextField, 'req'):
			edit_form_validator = FieldsMatch('password', 'verify_password',
				messages={'invalidNoMatch': 'Passwords do not match'})
		else:
			edit_form_validator =  FilteringSchema(chained_validators=[FieldsMatch('password',
				'verify_password',
				messages={'invalidNoMatch':
					          'Passwords do not match'})])

		if not getattr(self, 'edit_form_type', None):
			class EditForm(CustomForm):
				__entity__ = self.model
				__require_fields__     = [user_name_field, email_field]
				__omit_fields__        = ['created', '_password', '_groups']
				__hidden_fields__      = [user_id_field]
				__field_order__        = [user_id_field, user_name_field, email_field, display_name_field, 'password', 'verify_password', 'groups']
				password = PasswordField('password', value='')
				verify_password = PasswordField('verify_password')
				__base_validator__ = edit_form_validator

			if email_field is not None:
				setattr(EditForm, email_field, TextField)
			if display_name_field is not None:
				setattr(EditForm, display_name_field, TextField)
			self.edit_form_type = EditForm

		if not getattr(self, 'edit_filler_type', None):
			class UserEditFormFiller(EditFormFiller):
				__entity__ = self.model
				def get_value(self, *args, **kw):
					v = super(UserEditFormFiller, self).get_value(*args, **kw)
					del v['password']
					return v

			self.edit_filler_type = UserEditFormFiller

		if not getattr(self, 'new_form_type', None):
			class NewForm(CustomAddRecordForm):
				__entity__ = self.model
				__require_fields__     = [user_name_field, email_field, password_field]
				__omit_fields__        = ['created', '_password', '_groups']
				__hidden_fields__      = [user_id_field]
				__field_order__        = [user_name_field, email_field, password_field, display_name_field, group_name_field]

			if email_field is not None:
				setattr(NewForm, email_field, TextField)
			if display_name_field is not None:
				setattr(NewForm, display_name_field, TextField)
			self.new_form_type = NewForm

	class defaultCrudRestController(CrudRestController):

		@expose('/crud/edit.html')
		def edit(self, *args, **kw):
			tmpl_context.widget = self.edit_form
			pks = self.provider.get_primary_fields(self.model)
			if len(args) > 0:
				kw = {}
				for i, pk in  enumerate(pks):
					kw[pk] = args[i]
			value = self.edit_filler.get_value(kw)
			value['_method'] = 'PUT'
			#		return value
			return dict(value=value, model=self.model.__name__, pk_count=len(pks))

		@expose()
		@registered_validate(error_handler=edit)
		def put(self, *args, **kw):
			"""update"""
			if 'password' in kw and not kw['password']:
				del kw['password']

			pks = self.provider.get_primary_fields(self.model)
			for i, pk in enumerate(pks):
				if pk not in kw and i < len(args):
					kw[pk] = args[i]

			self.provider.update(self.model, params=kw)
			return "success"



class GroupControllerConfig(CrudRestControllerConfig):
	def _do_init_with_translations(self, translations):
		group_id_field       = translations.get('group_id', 'group_id')
		group_name_field     = translations.get('group_name', 'group_name')

		class GroupTable(TableBase):
			__model__ = self.model
			__limit_fields__ = [group_name_field, 'permissions']
			__url__ = '../groups.json'
		self.table_type = GroupTable

		class GroupTableFiller(TableFiller):
			__model__ = self.model
			__limit_fields__ = [group_id_field, group_name_field, 'permissions']
			def __actions__(self, obj):
				primary_fields = self.__provider__.get_primary_fields(self.__entity__)
				pklist = 'groups/'+'/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
				value = '<a id="btn_edit" class="btn btn-warning" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
               '<form style="display:inline; margin-left:10px;" method="POST" action="'+pklist+'">'\
				 '<input type="hidden" name="_method" value="DELETE" />'\
				 '<input class="btn btn-danger" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" />'\
				 '</form>'
				return value
		self.table_filler_type = GroupTableFiller

		class GroupNewForm(CustomAddRecordForm):
			__model__ = self.model
			__limit_fields__ = [group_name_field, 'permissions']
			__field_order__ = [group_name_field, 'permissions']
		self.new_form_type = GroupNewForm

		class GroupEditForm(CustomForm):
			__model__ = self.model
			__limit_fields__ = [group_id_field, group_name_field, 'permissions']
			__field_order__ = [group_id_field, group_name_field, 'permissions']
		self.edit_form_type = GroupEditForm

class PermissionControllerConfig(CrudRestControllerConfig):
	def _do_init_with_translations(self, translations):
		permission_id_field              = translations.get('permission_id', 'permission_id')
		permission_name_field            = translations.get('permission_name', 'permission_name')
		permission_description_field     = translations.get('permission_description', 'description')

		class PermissionTable(TableBase):
			__model__ = self.model
			__limit_fields__ = [permission_name_field, permission_description_field, 'groups']
			__url__ = '../permissions.json'
		self.table_type = PermissionTable

		class PermissionTableFiller(TableFiller):
			__model__ = self.model
			__limit_fields__ = [permission_id_field, permission_name_field, permission_description_field, 'groups']
			def __actions__(self, obj):
				primary_fields = self.__provider__.get_primary_fields(self.__entity__)
				pklist = 'permissions/'+'/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
				value = '<a id="btn_edit" class="btn btn-warning" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
               '<form style="display:inline; margin-left:10px;" method="POST" action="'+pklist+'">'\
               '<input type="hidden" name="_method" value="DELETE" />'\
               '<input class="btn btn-danger" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" />'\
               '</form>'
				return value
		self.table_filler_type = PermissionTableFiller

		class PermissionNewForm(CustomAddRecordForm):
			__model__ = self.model
			__limit_fields__ = [permission_name_field, permission_description_field, 'groups']
		self.new_form_type = PermissionNewForm

		class PermissionEditForm(CustomForm):
			__model__ = self.model
			__limit_fields__ = [permission_name_field, permission_description_field,'groups']
		self.edit_form_type = PermissionEditForm

		class PermissionEditFiller(RecordFiller):
			__model__ = self.model
		self.edit_filler_type = PermissionEditFiller



class ArticleControllerConfig(CrudRestControllerConfig):
	def _do_init_with_translations(self, translations):
		article_id_field = translations.get('article_id', 'article_id')
		article_name_field = translations.get('article_name', 'name')
		article_title_field = translations.get('article_title', 'title')
		article_text_field = translations.get('article_text', 'text')
		article_category_field = translations.get('article_category', 'category')

		class ArticleTable(TableBase):
			__model__ = self.model
			__omit_fields__ = ['_category',article_id_field,'_user',article_text_field]
			__url__ = '../articles.json'
		self.table_type = ArticleTable

		class ArticleTableFiller(TableFiller):
			__model__ = self.model
			__omit_fields__ = ['_category',article_id_field,'_user',article_text_field]
			def __actions__(self, obj):
				primary_fields = self.__provider__.get_primary_fields(self.__entity__)
				pklist = 'articles/'+'/'.join(map(lambda x: str(getattr(obj, x)), primary_fields))
				value = '<a id="btn_edit" class="btn btn-warning" href="'+pklist+'/edit" style="text-decoration:none">edit</a>'\
                         '<form style="display:inline; margin-left:10px;" method="POST" action="'+pklist+'">'\
                         '<input type="hidden" name="_method" value="DELETE" />'\
                         '<input class="btn btn-danger" onclick="return confirm(\'Are you sure?\');" value="delete" type="submit" />'\
                         '</form>'
				return value
		self.table_filler_type = ArticleTableFiller

		class ArticleEditForm(CustomForm):
			__model__ = self.model
			__require_fields__ = [article_name_field, article_title_field, article_text_field]
			__omit_fields__ = ['_user', 'created_on']
			__hidden_fields = [article_id_field]
			__field_order__ = [article_id_field, article_name_field, article_title_field, article_text_field]
		self.edit_form_type = ArticleEditForm

		class ArticleEditFormFiller(RecordFiller):
			__model__ = self.model
			def get_value(self, *args, **kw):
				v = super(ArticleEditFormFiller, self).get_value(*args, **kw)
				return v
		self.edit_filler_type = ArticleEditFormFiller

		class ArticleNewForm(CustomAddRecordForm):
			__model__ = self.model
			__omit_fields__ = ['_user', 'created_on', '_category']
			__hidden_fields = [article_id_field]
			__field_order__ = [article_id_field, article_name_field, article_title_field, 'category', article_text_field, 'tags', 'user']
		self.new_form_type = ArticleNewForm

	class defaultCrudRestController(CrudRestController):

		@without_trailing_slash
		@expose('/crud/new.html')
		def new(self, *args, **kw):
			"""Display a page to show a new record."""
			tmpl_context.widget = self.new_form
			return dict(value=kw, model=self.model.__name__)

		@expose()
		@registered_validate(error_handler=new)
		def post(self, *args, **kw):
			tgs = kw.get('tags',[])
			if not len(tgs):
				kw['tags'] = []
			else:
				_tgs = tgs.split(',')
				kw['tags'] = [_tgs_.strip() for _tgs_ in _tgs]
			self.provider.create(self.model, params=kw)
			return dict(value=kw)




class PJAdminConfig(AdminConfig):
	default_to_dojo = False

	user       = UserControllerConfig
	group      = GroupControllerConfig
	permission = PermissionControllerConfig


