__author__ = 'panjiesw'

from sprox.formbase import FormBase
import tw2.core as twc
from tw2.forms.widgets import Form, BaseLayout
from sprox.widgets.tw2widgets.widgets import SproxMethodPutHiddenField
from formencode.validators import String

class CustomFormLayout(BaseLayout):
	template = "panjieblog.widgets.templates.custom_layout"

class CustomFormWidget(Form):
	template = "panjieblog.widgets.templates.custom_form"
	child = twc.Variable(default=CustomFormLayout)
	children = twc.Required

class CustomForm(FormBase):
	__base_widget_type__ = CustomFormWidget
	def _do_get_disabled_fields(self):
		fields = self.__disable_fields__[:]
		fields.append(self.__provider__.get_primary_field(self.__entity__))
		return fields

	def _do_get_fields(self):
		"""Override this function to define what fields are available to the widget.

	"""
		fields = super(CustomForm, self)._do_get_fields()
		primary_field = self.__provider__.get_primary_field(self.__entity__)
		if primary_field not in fields:
			fields.append(primary_field)

		if '_method' not in fields:
			fields.append('_method')

		return fields

	def _do_get_field_widgets(self, fields):
		widgets = super(CustomForm, self)._do_get_field_widgets(fields)
		widgets['_method'] = SproxMethodPutHiddenField(id='sprox_method', validator=String(if_missing=None))
		return widgets

	__check_if_unique__ = False


class CustomAddRercordForm(FormBase):
	__base_widget_type__ = CustomFormWidget
	def _do_init_attrs(self):
		super(CustomAddRercordForm, self)._do_init_attrs()

		if not self.__omit_fields__:
			pkey = self.__provider__.get_primary_field(self.__entity__)
			self.__omit_fields__.append(pkey)

	def _do_get_disabled_fields(self):
		fields = self.__disable_fields__[:]
		fields.append(self.__provider__.get_primary_field(self.__entity__))
		return fields