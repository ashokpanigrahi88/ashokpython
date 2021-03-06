# -*- coding: utf-8 -*-
"""Release data for the  OratechDatahub project."""

#-----------------------------------------------------------------------------
#  Copyright (c) 2021,  OratechDatahub Development Team.
#
#  The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

# Name of the package for release purposes.  This is the name which labels
# the tarballs and RPMs made by distutils, so it's best to lowercase it.
name = 'oratechetl'

#  OratechDatahub version information.  An empty _version_extra corresponds to a full
# release.  'dev' as a _version_extra string means this is a development
# version
_version_major = 1
_version_minor = 0
_version_patch = 0
_version_extra = '.dev'
# _version_extra = 'b1'
#_version_extra = ''  # Uncomment this for full releases

# Construct full version string from these.
_ver = [_version_major, _version_minor, _version_patch]

__version__ = '.'.join(map(str, _ver))
if _version_extra:
    __version__ = __version__  + _version_extra

version = __version__  # backwards compatibility name
version_info = (_version_major, _version_minor, _version_patch, _version_extra)


description = " OratechDatahub: Oratech Datahub ETL Utility"

long_description = \
"""
 OratechDatahub provides a rich toolkit to help you make the most out of using Python
"""

license = 'Oratech'

authors = {'Panigrahi' : ('Ashok Panigrahi','ashok.panigrahi@oratechsolutions.biz'),
           }

author = 'The OratechDatahub Development Team'

author_email = 'oratechdatahub-dev@python.org'

url = 'http://www.oratechsolutions.biz'


platforms = ['Linux','Mac OSX','Windows']

keywords = ['Interactive','Interpreter','Shell', 'Embedding']

classifiers = [
    'Framework ::  oratechetl',
    'Intended Audience :: Retailers',
    'Intended Audience :: Warehouse Business',
    'License :: OSI Approved :: OratechLicense',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: System :: Shells'
    ]
