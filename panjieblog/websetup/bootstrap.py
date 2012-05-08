# -*- coding: utf-8 -*-
"""Setup the panjieblog application"""

import logging
from tg import config
from panjieblog import model

def bootstrap(command, conf, vars):
    """Place any commands to setup panjieblog here"""

    # <websetup.bootstrap.before.auth
    g = model.Group()
    g.group_name = u'admin'
    g.display_name = u'Admin Group'

    p = model.Permission()
    p.permission_name = u'manage'
    p.description = u'This permission give an administrative right to the bearer'
    p.groups = [g]

    u = model.User()
    u.user_name = u'panjiesw'
    u.display_name = u'Panjie SW'
    u.email_address = u'panjie@panjiesw.com'
    u.groups = [g]
    u.password = u'p4nji135wTG'

    pg = model.Page()
    pg.cat_name = u'life'
    pg.cat_display = u'Life'

    pg2 = model.Page()
    pg2.cat_name = u'python'
    pg2.cat_display = u'Python'

    a = model.Article()
    a.name = u'first-post'
    a.title = u'The First Blog Post'
    a.text = u'<h1>Hello World</h1><p>This is the first post from bootstrap.</p>'\
             u'<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
             u'Pellentesque congue massa in nulla convallis semper. Curabitur sollicitudin, ' \
             u'nulla quis dignissim fringilla, nunc dolor elementum nulla, ut malesuada est lacus ac mauris. ' \
             u'Fusce elementum egestas hendrerit. Integer eget leo quam, vitae consequat elit. ' \
             u'Vivamus pulvinar massa at ipsum bibendum ut hendrerit enim imperdiet. Duis libero tellus, ' \
             u'fringilla sed porta ut, varius quis est. Morbi convallis urna lacus, gravida interdum massa. ' \
             u'Morbi pellentesque libero vel velit rutrum eleifend. </p>'
    a.user = u'panjiesw'
    a.category = u'Life'

    model.DBSession.flush()
    model.DBSession.clear()

    # <websetup.bootstrap.after.auth>
