# -*- coding: utf-8 -*-
#quckstarted Options:
#
# sqlalchemy: False
# auth:       ming
# mako:       None
#
#

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs=['WebTest >= 1.2.3',
               'nose',
               'coverage',
               'wsgiref',
               'repoze.who-testutil >= 1.0.1',
               ]
install_requires=[
    "TurboGears2 >= 2.2.0rc1",
    "Jinja2",
    "tgming",
    "repoze.what >= 1.0.8",
    "repoze.who-friendlyform >= 1.0.4",
    "repoze.who==1.0.19",
    "tgext.admin >= 0.3.11",
    "tw2.forms",
    "sprox >= 0.7dev",
    ]

setup(
    name='panjieblog',
    version='0.1',
    description='',
    author='',
    author_email='',
    #url='',
    setup_requires=["PasteScript >= 1.7", "sprox", "utils", "webhelpers", "ming"],
    paster_plugins=['PasteScript', 'Pylons', 'TurboGears2'],
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'panjieblog': ['i18n/*/LC_MESSAGES/*.mo',
                                 'templates/*/*',
                                 'public/*/*']},
    message_extractors={'panjieblog': [
            ('**.py', 'python', None),
            ('templates/**.html', 'genshi', None),
            ('public/**', 'ignore', None)]},

    entry_points="""
    [paste.app_factory]
    main = panjieblog.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    dependency_links=[
        "http://tg.gy/beta"
        ],
    zip_safe=False
)
