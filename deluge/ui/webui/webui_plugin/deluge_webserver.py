#
# webserver_framework.py
#
# Copyright (C) Martijn Voncken 2007 <mvoncken@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, write to:
#     The Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor
#     Boston, MA  02110-1301, USA.
#
#  In addition, as a special exception, the copyright holders give
#  permission to link the code of portions of this program with the OpenSSL
#  library.
#  You must obey the GNU General Public License in all respects for all of
#  the code used other than OpenSSL. If you modify file(s) with this
#  exception, you may extend this exception to your version of the file(s),
#  but you are not obligated to do so. If you do not wish to do so, delete
#  this exception statement from your version. If you delete this exception
#  statement from all source files in the program, then also delete it here.


from webserver_common import ws

from lib.webpy022.request import webpyfunc
from lib.webpy022 import webapi
from lib.gtk_cherrypy_wsgiserver import CherryPyWSGIServer
import lib.webpy022 as web
import os

def create_webserver(urls, methods, middleware):
    func = webapi.wsgifunc(webpyfunc(urls, methods, False), *middleware)
    server_address=("0.0.0.0", int(ws.config.get('port')))

    server = CherryPyWSGIServer(server_address, func, server_name="localhost")
    if ws.config.get('use_https'):
        server.ssl_certificate = os.path.join(ws.webui_path,'ssl/deluge.pem')
        server.ssl_private_key = os.path.join(ws.webui_path,'ssl/deluge.key')

    print "http://%s:%d/" % server_address
    return server

def WebServer(debug = False):
    if debug:
        middleware = [web.reloader]
    else:
        middleware = []

    import pages
    return create_webserver(pages.urls, pages.page_classes, middleware)

def run(debug = False):
    server = WebServer(debug)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
