# -*- coding: utf-8 -*-
"""The application's model objects"""

import ming.odm
from session import mainsession, DBSession

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    mainsession.bind = engine
    ming.odm.Mapper.compile_all()

    for mapper in ming.orm.Mapper.all_mappers():
        mainsession.ensure_indexes(mapper.collection)

# Import your model modules here.
from panjieblog.model.auth import User, Group, Permission
