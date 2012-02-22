# Copyright (C) 2010-2011 Large Blue
#               Fergus Doyle: fergus.doyle@largeblue.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License Version 2 as published
# by the Free Software Foundation.  You may not use, modify or distribute
# this program under any other version of the GNU General Public License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os
import re
from webob import Request, Response
from chameleon.zpt.loader import TemplateLoader

DEFAULT_COOKIE_LIFETIME = 10 * 365 * 24 * 60 * 60 # 10 years

class GatewayMiddleware(object):
    def __init__(self,
                 app,
                 global_conf,
                 password,
                 cookie_name,
                 cookie_value,
                 domain = '',
                 lifetime = DEFAULT_COOKIE_LIFETIME,
                 # - exclude these URLs from gateway
                 exclude = '\.(js|css|png|gif|jpg|jpeg|ico)/?$',
                 # - exclude requests with these headers from gateway
                 skip_with_header = ''
                 ):
        """ example paste.deploy config:

            [filter:gateway]
            use = egg:openideo#gateway
            password = T0pS3cRet
            cookie_name = oreo
            cookie_value = yummy
            exclude = /static
            skip_with_header = HTTP_USER_AGENT:(funkload|ApacheBench)
                               REMOTE_HOST:127.0.0.1
        """
        self.app = app
        self.password = password
        self.cookie_name = cookie_name
        self.cookie_value = cookie_value
        self.domain = domain
        self.lifetime = lifetime
        self.exclude = re.compile(exclude, re.I) if exclude else None
        self.skip_list = []
        if skip_with_header:
            hdr_pattern_list = [ kv.split(':') for kv in skip_with_header.split() ]
            self.skip_list = [ (header, re.compile(pattern, re.I)) for header, pattern in hdr_pattern_list ]
        self.loader = TemplateLoader(os.path.dirname(__file__))

    def __call__(self, environ, start_response):
        request = Request(environ)

        if request.cookies.get(self.cookie_name, None) == self.cookie_value:
            return self.app(environ, start_response)

        if self.exclude and re.search(self.exclude, request.path_info):
            return self.app(environ, start_response)

        for header, pattern in self.skip_list:
            value = environ.get(header)
            if value and re.search(pattern, value):
                return self.app(environ, start_response)

        password = request.params.get('password', None)

        if password == self.password:
            res = request.get_response(self.app)
            domain = self.domain if self.domain else request.host
            res.set_cookie(self.cookie_name, self.cookie_value,
                            max_age=self.lifetime, path='/', domain=domain)
            return res(environ, start_response)
        else:
            template = self.loader.load('form.pt')
            res = Response(content_type='text/html', charset='utf8', body=template.render())
            return res(environ, start_response)
