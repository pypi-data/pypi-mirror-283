__title__ = 'ZRU Python'
__version__ = '1.0.0'
__author__ = 'ZRU'
__license__ = 'BSD 2-Clause'
__copyright__ = 'Copyright 2024 ZRU'

# Version synonym
VERSION = __version__

# Header encoding (see RFC5987)
HTTP_HEADER_ENCODING = 'iso-8859-1'

# Default datetime input and output formats
ISO_8601 = 'iso-8601'


from .zru import ZRUClient
