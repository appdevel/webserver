from http.server import *
import logging
import json
import threading

logger = 0

class dataHttpProcessor(BaseHTTPRequestHandler):        
    def do_POST(self):
        global data_server_thread
        global _stop
        if _stop.is_set():
            _stop.clear()
            data_server_thread.exit()
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
        
class controlHttpProcessor(BaseHTTPRequestHandler):        
    def do_GET(self):
        global _stop
        global logger
        logger.info('Recieved kill signal')        
        self.send_response(200)
        self.send_header('content-type','text/html;charset=utf-8')
        self.end_headers()
        try:
            answer = '<html><body><h1>You killed Kenny!</h1></body></html>'
            _stop.set()
        except Exception as err:
            logger.exception(err)
            answer = '<html><body><h1>Please wait until data server is up</h1></body></html>'
        self.wfile.write(answer.encode('utf-8'))
        
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
              
global _stop
_stop = threading.Event()

global data_server_thread
data_server_thread = threading.Thread(target=run, args=(HTTPServer, dataHttpProcessor, 8000))
data_server_thread.start()

control_server_thread = threading.Thread(target=run, args=(HTTPServer, controlHttpProcessor, 8001))
control_server_thread.start()

data_server_thread.join()
control_server_thread.join()