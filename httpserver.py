# -------------------------------------------------------------------------------
# Name:        httpserver
# Purpose:
#
# Author:      apav
#
# Created:     18.02.2014
# Copyright:   (c) apav 2014
# -------------------------------------------------------------------------------

from socketserver import BaseServer, ThreadingMixIn
import xml.etree.ElementTree as etree
import socket
import ssl
from cgi import parse_header
from http.server import *
import threading
import settings
import logging
import log
import time
import protocol

logger = 0


# class for multithreading and Secure HTTP Server
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def __init__(self, address, handler):
        global logger
        try:
            BaseServer.__init__(self, address, handler)
            self.socket = ssl.SSLSocket(
                sock=socket.socket(self.address_family, self.socket_type),
                ssl_version=ssl.PROTOCOL_TLSv1,
                certfile=settings.ServerParams["Certificate"],
                server_side=True)
            self.server_bind()
            self.server_activate()
            #   create http logger
            logger = logging.getLogger('HTTP')
            logger.setLevel(settings.SystemParams["LogLevel"])
            logger.addHandler(log.ch)

            logger.info('HTTPS server started. Press ^C to stop')
        except Exception as err:
            Logger.error('Error during HTTPS server starting')

    def shutdown(self):
        HTTPServer.shutdown(self)
        logger.info('HTTPS server stoped')


class MyHandler(BaseHTTPRequestHandler):
    def do_QUIT(self):
        self.send_response(200)
        self.end_headers()
        self.server.stop = True
        return

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        return

    def do_GET(self):
        global logger
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            localtime = time.localtime()
            timeString = time.strftime("%d.%m.%Y %H:%M:%S", localtime)
            # Check db connection
            settings.database.checkconnection()
            answer = '<?xml version="1.0" encoding="utf-8"?> \
                     <Response datetime="%s"> \
                     <ResultCode>ERROR</ResultCode> \
                      <ErrorString errorCode="%d">%s</ErrorString> \
                     </Response>' % (timeString, -1, settings.database.geterrordescription(-1))
            self.wfile.write(answer.encode("utf-8"))
            # message =  threading.currentThread().getName()
            # print (message)
            logger.error('GET request recieved')
        except IOError as err:
            logger.error(str(err))
            self.send_error(404, str(err))
        return

    def do_POST(self):
        global logger
        #        message =  threading.currentThread().getName()
        #        print (message)
        try:
            ctype, pdict = parse_header(self.headers['content-type'])
            # logger.debug(self.headers)
        except IOError as err:
            logger.error(str(err))
            self.send_error(404, str(err))
        if ctype == 'text/xml':
            try:
                length = int(self.headers['content-length'])
                data = self.rfile.read(length).decode("utf-8")
                sender = self.client_address[0] + ':' + str(self.client_address[1])
                logger.info(sender + ' - Recieved XML: ' + data)
                parse_answer = settings.protocol.parse(data, sender)
                if parse_answer[0] == 0:
                    res = 'OK'
                    answer = parse_answer[1]
                else:
                    res = 'ERROR'
                    localtime = time.localtime()
                    timeString = time.strftime("%d.%m.%Y %H:%M:%S", localtime)
                    answer = '<?xml version="1.0" encoding="utf-8"?>' \
                             '<Response datetime="%s">' \
                             '<ResultCode>%s</ResultCode>' \
                             '<ErrorString errorCode="%s">%s</ErrorString>' \
                             '</Response>' % (timeString, res, str(parse_answer[0]), parse_answer[1])
                self.send_response(200)
                self.send_header("Content-type", "text/xml")
                self.end_headers()
                logger.info(sender + ' - Sended XML: ' + answer)
                self.wfile.write(answer.encode("utf-8"))
            except IOError as err:
                logger.error(str(err))
                self.send_error(404, str(err))
        else:
            try:
                localtime = time.localtime()
                timeString = time.strftime("%d.%m.%Y %H:%M:%S", localtime)
                self.send_response(200)
                self.send_header("Content-type", "text/xml")
                self.end_headers()
                answer = '<?xml version="1.0" encoding="utf-8"?> \
                     <Response datetime="%s"> \
                     <ResultCode>ERROR</ResultCode> \
                      <ErrorString errorCode="-2">%s</ErrorString> \
                     </Response>' % (timeString, settings.database.geterrordescription(-2))
                self.wfile.write(answer.encode("utf-8"))
                logger.error('Wrong content-type header')
            except IOError as err:
                logger.error(str(err))
                self.send_error(404, str(err))
        return
