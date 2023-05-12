import os

bind = 'localhost:10022'
workers = 2
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
secure_scheme_headers = {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
forwarded_allow_ips = '*'

