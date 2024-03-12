#!/usr/bin/env python

from distutils.core import setup
import jsonpath as module

name = module.__name__
version = module.__version__
url_base = "http://www.ultimate.com/phil/python/"
url = url_base + '#' + name
download_url = "%sdownload/%s-%s.tar.gz" % (url_base, name, version)
# extract description and long_description from module __doc__ string
lines = module.__doc__.split("\n")
while len(lines) > 0 and lines[0] == '':
    lines.pop(0)
empty = lines.index('')
descr = '\n'.join(lines[:empty])
long_descr = '\n'.join(lines[empty+1:])

setup(name=name,
      version=version,
      description=descr,
      # ReStructuredText: http://docutils.sourceforge.net/rst.html
      long_description=long_descr,
      author="Phil Budne",
      author_email="phil@ultimate.com",
      url=url,
      download_url=download_url,
      py_modules=['jsonpath'],
      classifiers=[
        # http://pypi.python.org/pypi?:action=list_classifiers
        #'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # Want: 'Topic :: Text Processing :: Markup :: JSON'
        'Topic :: Text Processing :: Markup',
        ],
      license="MIT",
      platforms = ['Any']
      )
