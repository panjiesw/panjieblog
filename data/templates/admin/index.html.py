# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1335260086.620208
_enable_loop = True
_template_filename = '/home/panjiesw/TurboEnv/panjieblog/panjieblog/templates/admin/index.html'
_template_uri = '/admin/index.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"{% extends 'admin/master.html' %}")
        return ''
    finally:
        context.caller_stack._pop_frame()


