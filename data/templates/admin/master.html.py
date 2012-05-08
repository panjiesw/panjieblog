# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1335288925.204932
_enable_loop = True
_template_filename = '/home/panjiesw/TurboEnv/panjieblog/panjieblog/templates/admin/master.html'
_template_uri = '/admin/master.html'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = []


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<!DOCTYPE html>\n<html>\n    {% from \'admin/sidebar.html\' import sidebar with context %}\n    <head>\n        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"\n              content="{{ response.content_type }}; charset={{ response.charset }}"/>\n        <meta name="description" content="The Administration System and Interface of PanjieSW Blog"/>\n        <meta name="author" content="PanjieSW @panjiesw"/>\n        <title>PanjieSW Blog Admin Interface</title>\n        <link rel="stylesheet" type="text/css" media="screen" href="{{ tg.url(\'/css/bootstrap.min.css\') }}" />\n        <link rel="stylesheet" type="text/css" media="screen" href="{{ tg.url(\'/css/bootstrap-responsive.min.css\') }}" />\n        <style type="text/css">\n            body {\n                padding-top: 60px;\n                background-color: #d9d9d9;\n            }\n\n            .sidebar-nav {\n                padding: 9px 0;\n            }\n\n            .crd_table {\n                margin-top: 20px;\n            }\n        </style>\n    </head>\n    <body>\n        <div class="navbar navbar-fixed-top">\n            <div class="navbar-inner">\n                <div class="container-fluid">\n                    <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n                        <span class="icon-bar"></span>\n                        <span class="icon-bar"></span>\n                        <span class="icon-bar"></span>\n                    </a>\n                    <a class="brand" href="{{ tg.url(\'/\') }}">PanjieSW Blog</a>\n                    <div class="nav-collapse">\n                        <ul class="nav">\n                            <li class="active"><a href="{{ tg.url(\'/\') }}">Home</a></li>\n                        </ul>\n                        <ul class="nav pull-right">\n                            <li class="pull-right"><a href="{{ tg.url(\'/logout_handler\') }}">Logout</a></li>\n                        </ul>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <div class="container">\n            <div class="row-fluid">\n                <div class="span2">\n                    <div class="well sidebar-nav">\n                        {{ sidebar() }}\n                    </div>\n                </div>\n                <div class="span9">\n                    <div id="content_wrap" class="well">\n                        <h1>Hello World!!</h1>\n                        <p>This is the Administration System of PanjieSW Blog.</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n        <script type="text/javascript" src="{{ tg.url(\'/javascript/jquery-1.7.1.min.js\') }}" ></script>\n        <script type="text/javascript" src="{{ tg.url(\'/javascript/bootstrap.min.js\') }}" ></script>\n        <script type="text/javascript">\n            $(function(){\n                var last_active;\n                $(\'.sidelink\').click(function(event){\n                    var url = this.href;\n                    if (last_active)    last_active.removeClass("active");\n                    $.get(\n                            url,\n                            function (data) {\n                                $(\'#content_wrap\').html(data);\n                            }\n                    );\n                    $(this).parent().addClass("active");\n                    last_active = $(this).parent();\n                    return false;\n                });\n\n                $(\'.table thead tr th a\').live("click", function(event){\n                    var url = this.href;\n                    $.get(\n                            url,\n                            function (data) {\n                                $(\'#content_wrap\').html(data);\n                            }\n                    );\n                    return false;\n                });\n\n                $(\'#crd_edit\').live("click",function(event){\n                    var url = this.href;\n                    $.get(\n                            url,\n                            function(data) {\n                                console.log(data);\n                            }\n                    )\n                    return false;\n                });\n            })\n        </script>\n    </body>\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


