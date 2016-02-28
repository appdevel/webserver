from http.server import *
import logging
import json
import threading
import datetime

logger = 0
now = datetime.datetime.now()

class calendarHttpProcessor(BaseHTTPRequestHandler): 
    def do_GET(self):
        global logger
        logger.info('GET recieved')       
        self.send_response(200)
        self.send_header('content-type','text/html;charset=utf-8')
        self.end_headers()
        answer = '<html><body><h1>Data server is up!</h1></body></html>'
        self.wfile.write(answer.encode('utf-8'))    
    def do_POST(self):
        global logger
        logger.info('POST recieved')        
        self.send_response(200)
        self.send_header('content-type','application/json;charset=utf-8')
        self.end_headers()
        length = int(self.headers['content-length'])
        #data = self.rfile.read(length).decode("utf-8")
        sender = self.client_address[0] + ':' + str(self.client_address[1])
        #logger.info(sender + ' - Recieved data: ' + data) 
        filename = 'basic1.json'
        try:
            with open(filename) as data_file:               # we parse raw data into json structure
                data = json.load(data_file)                 # read initial value from parsed data    
            y = now.year                                    # take the sysdate
            m = now.month
            d = now.day       
            answer = (eval(data['muslim']))                    # calculate expression and transform result into string
            answer = '{"answer":%d}' % answer               # transform 'answer' into json field format 
        except Exception as err:
            logger.exception(err)
            answer = str(err)
        self.wfile.write(answer.encode('utf-8'))                    
        logger.info('send to client: ' + answer)
        
class funcHttpProcessor(BaseHTTPRequestHandler):        
    def do_GET(self):
        global logger
        logger.info('Recieved kill signal')        
        self.send_response(200)
        self.send_header('content-type','text/html;charset=utf-8')
        self.end_headers()
        try:
            answer = '<html><body><h1>You killed Kenny!</h1></body></html>'
        except Exception as err:
            logger.exception(err)
            answer = '<html><body><h1>Something wrong</h1></body></html>'
        self.wfile.write(answer.encode('utf-8'))
    def do_POST(self):
        global logger
        logger.info('POST recieved')        
        self.send_response(200)
        self.send_header('content-type','application/json;charset=utf-8')
        self.end_headers()
        length = int(self.headers['content-length'])
        data = self.rfile.read(length).decode("utf-8")
        sender = self.client_address[0] + ':' + str(self.client_address[1])
        logger.info(sender + ' - Recieved data: ' + data) 
        try:
            data = json.loads(data)
            x = float(data['value'])
            answer = str(eval(data['expr']))
            answer = '{"answer":%s}' % answer
        except Exception as err:
            logger.exception(err)
            answer = str(err)
        self.wfile.write(answer.encode('utf-8'))                    
        logger.info('send to client: ' + answer)    
        
def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler, port = int):
        createlog()
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

def createlog():    
        global logger
    
        ch = logging.FileHandler('http_2.log')
        ch.setLevel(3)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s : %(levelname)s - %(message)s')
    
        # add formatter to ch
        ch.setFormatter(formatter)
        
        logger = logging.getLogger('HTTP')              
        logger.setLevel(3)
        logger.addHandler(ch)       
              
calendar_server_thread = threading.Thread(target=run, args=(HTTPServer, calendarHttpProcessor, 8000))
calendar_server_thread.start()

func_server_thread = threading.Thread(target=run, args=(HTTPServer, funcHttpProcessor, 8001))
func_server_thread.start()

calendar_server_thread.join()
func_server_thread.join()