# -*- coding: utf-8 -*-
"""Setup the panjieblog application"""

import logging
from tg import config
from panjieblog import model

def bootstrap(command, conf, vars):
    """Place any commands to setup panjieblog here"""

    # <websetup.bootstrap.before.auth
    g = model.Group()
    g.group_name = u'managers'
    g.display_name = u'Managers Group'

    p = model.Permission()
    p.permission_name = u'manage'
    p.description = u'This permission give an administrative right to the bearer'
    p.groups = [g]

    u = model.User()
    u.user_name = u'manager'
    u.display_name = u'Example manager'
    u.email_address = u'manager@somedomain.com'
    u.groups = [g]
    u.password = u'managepass'

    u1 = model.User()
    u1.user_name = u'editor'
    u1.display_name = u'Example editor'
    u1.email_address = u'editor@somedomain.com'
    u1.password = u'editpass'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
