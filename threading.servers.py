from http.server import *
import logging
import json
import threading
import datetime
import socketserver
import time
import ssl

logger = 0
now = datetime.datetime.now()


class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass


class calendarHttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        global logger
        logger.info('GET from 8000 port recieved')
        self.send_response(200)
        self.send_header('content-type', 'text/html;charset=utf-8')
        self.end_headers()
        answer = '<form name="inp" method="post"><p>Port 8000, method:</p><p><input maxlength="25" size="40" value="GET"></p></form>'
        self.wfile.write(answer.encode('utf-8'))
        time.sleep(15)
        print("sleep ended")

    def do_POST(self):
        global logger
        logger.info('POST from 8000 port recieved')
        self.send_response(200)
        self.send_header("content-type", "application/json;charset=utf-8")
        self.end_headers()
        length = int(self.headers['content-length'])
        # data = self.rfile.read(length).decode("utf-8")
        sender = self.client_address[0] + ':' + str(self.client_address[1])
        # logger.info(sender + ' - Recieved data: ' + data)
        filename = 'calendar.json'
        try:  # if everything ok...
            with open(filename) as data_file:  # we parse raw data into json structure
                data = json.load(data_file)  # read initial value from parsed data

            y = now.year  # take the sysdate
            m = now.month
            d = now.day

            # temporary variables for evaluation process
            JDNnum = int(eval(data['JDN']['JDNnum']))
            JDNc = int(eval(data['JDN']['JDNc']))
            JDNd = int(eval(data['JDN']['JDNd']))
            JDNe = int(eval(data['JDN']['JDNe']))
            JDNm = int(eval(data['JDN']['JDNm']))

            # dict. for sending answer
            answerdict = dict()
            NOW = dict()

            answerdict['NOW'] = NOW
            NOW['day'] = d
            NOW['month'] = m
            NOW['year'] = y

            answerdict['muslim'] = int(eval(data['muslim']))
            answerdict['mongol'] = int(eval(data['mongol']))
            answerdict['bengal'] = int(eval(data['bengal']))
            answerdict['thai'] = int(eval(data['thai']))

            nepal = dict()  # subdict for nepal
            answerdict['nepal'] = nepal
            nepal['day'] = int(eval(data['nepal']['day']))
            nepal['month'] = int(eval(data['nepal']['month']))
            nepal['year'] = int(eval(data['nepal']['year']))

            JDN = dict()  # subdict for JDN
            answerdict['JDN'] = JDN
            JDN['JDNday'] = int(eval(data['JDN']['JDNday']))
            JDN['JDNmonth'] = int(eval(data['JDN']['JDNmonth']))
            JDN['JDNyear'] = int(eval(data['JDN']['JDNyear']))

            answer = json.dumps(answerdict, sort_keys=False)  # put answerdict structure in a json format string

        except Exception as err:
            logger.exception(err)
            answer = str(err)
        self.wfile.write(answer.encode('utf-8'))
        logger.info('Calculated date in JSON format: ' + answer)


class funcHttpProcessor(BaseHTTPRequestHandler):
    def do_GET(self):
        global logger
        logger.info('GET from 8001 port received')
        self.send_response(200)
        self.send_header('content-type', 'text/html;charset=utf-8')
        self.end_headers()
        try:
            answer = '<html><body><h1>Port 8001, method GET</h1></body></html>'
        except Exception as err:
            logger.exception(err)
            answer = '<html><body><h1>Something wrong</h1></body></html>'
        self.wfile.write(answer.encode('utf-8'))

    def do_POST(self):
        global logger
        logger.info('POST from 8001 port recieved')
        self.send_response(200)
        self.send_header('content-type', 'application/json;charset=utf-8')
        self.end_headers()
        length = int(self.headers['content-length'])
        data = self.rfile.read(length).decode("utf-8")
        sender = self.client_address[0] + ':' + str(self.client_address[1])
        logger.info(sender + ' - Recieved data on 8001 port: ' + data)
        try:
            data = json.loads(data)
            x = float(data['value'])
            answer = str(eval(data['expr']))
            answer = '{"answer":%s}' % answer
        except Exception as err:
            logger.exception(err)
            answer = str(err)
        self.wfile.write(answer.encode('utf-8'))
        logger.info('Calculated answer in JSON format: ' + answer)


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=int):
    createlog()
    server_address = ('', port)
    httpd = ThreadedHTTPServer(server_address, handler_class)
    httpd.serve_forever()


def createlog():
    global logger

    ch = logging.FileHandler('logger.log')
    ch.setLevel(3)

    # create formatter
    formatter = logging.Formatter('[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    logger = logging.getLogger('HTTP')
    logger.setLevel(3)
    logger.addHandler(ch)
    logger.handlers = [logger.handlers[0], ]


calendar_server_thread = threading.Thread(target=run, args=(HTTPServer, calendarHttpProcessor, 8000))
calendar_server_thread.start()

func_server_thread = threading.Thread(target=run, args=(HTTPServer, funcHttpProcessor, 8001))
func_server_thread.start()

calendar_server_thread.join()
func_server_thread.join()
