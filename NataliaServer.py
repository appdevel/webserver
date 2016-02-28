from http.server import *
import logging
import json
import datetime

now = datetime.datetime.now()
logger = 0

class HttpProcessor(BaseHTTPRequestHandler):        # inheritance from BaseHTTP... class
    
    def do_GET(self):                               # re-defining method do_GET of BaseHTTP... class
        global logger                               # using defined in 'createLog' global variable 'logger'
        logger.info('GET recieved')                 # writing 'INFO' message in log
        self.send_response(200)                     # sending 'OK' response, the page was successfully found 
        self.send_header('content-type','text/html;charset=utf-8')      # sending specific headers
        self.end_headers()                                              # finishing headers sending               
        answer = '<form name="inp" method="post"><p>Enter the number:</p><p><input maxlength="25" size="40" value="Calendar"></p></form>' 
        self.wfile.write(answer.encode('utf-8'))                # sending response message (answer, encoded in utf-8) - writing in send socket
       
    def do_POST(self):                              # re-defining method do_POST of BaseHTTP... class
        global logger                               # using defined in 'createLog' global variable 'logger' 
        logger.info('POST recieved')                # writing 'INFO' message in log 
        self.send_response(200)                     # sending 'OK' response 
        self.send_header('content-type','application/json;charset=utf-8')       # sending specific headers
        self.end_headers()                                                      # finishing headers sending
        length = int(self.headers['content-length'])                            # getting recieved request length
        data = self.rfile.read(length).decode("utf-8")                          # reading recieve socket at length of recieved request 
        sender = self.client_address[0] + ':' + str(self.client_address[1])     # saving server's (our) address in variable, first address, second - port
        logger.info(sender + ' - Recieved data: ' + data)                       # writing in log file received data
        filename = 'calendar.json'
        try:                                                # if everything ok...
            with open(filename) as data_file:               # we parse raw data into json structure
                data = json.load(data_file)                 # read initial value from parsed data    
            
            y = now.year                                    # take the sysdate
            m = now.month
            d = now.day  
            
            #temporary variables for evaluation process
            JDNnum = int(eval(data['JDN']['JDNnum']))
            JDNc = int(eval(data['JDN']['JDNc']))
            JDNd = int(eval(data['JDN']['JDNd']))
            JDNe = int(eval(data['JDN']['JDNe']))
            JDNm = int(eval(data['JDN']['JDNm']))
          
            #dict. for sending answer
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
            
            nepal = dict()              # subdict for nepal
            answerdict['nepal'] = nepal
            nepal['day'] = int(eval(data['nepal']['day'])) 
            nepal['month'] = int(eval(data['nepal']['month'])) 
            nepal['year'] = int(eval(data['nepal']['year']))             
            
            JDN = dict()                 # subdict for JDN
            answerdict['JDN'] = JDN            
            JDN['JDNday'] = int(eval(data['JDN']['JDNday'])) 
            JDN['JDNmonth'] = int(eval(data['JDN']['JDNmonth']))
            JDN['JDNyear'] = int(eval(data['JDN']['JDNyear'])) 
       
            answer = json.dumps(answerdict, sort_keys=False)        #put answerdict structure in a json format string
            
        except Exception as err:                            # ... and if everything is fucked up
            logger.exception(err)                           # write error message into log file
            answer = str(err)                               # write error answer into 'answer'
        self.wfile.write(answer.encode('utf-8'))            # sending response message (answer, encoded in utf-8) - writing in send socket        
        logger.info('send to client: ' + answer)            # write 'send to client' INFO into log file
        
def run(server_class = HTTPServer, handler_class = BaseHTTPRequestHandler):     # main procedure
        createlog()                                         # starting log procedure
        server_address = ('', 8000)                         # '' = localhost
        httpd = server_class(server_address, handler_class) # initiating server
        httpd.serve_forever()                               # starting server

def createlog():    
        global logger                               # defining global variable 'logger'
    
        ch = logging.FileHandler('http_2.log')      # setting log file
        ch.setLevel(3)                              # setting up lowest log level (if I understand right it would be WARN for '3') which would be written into log file by this handler

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s : %(levelname)s - %(message)s')
     
        # add formatter to ch
        ch.setFormatter(formatter)
        
        logger = logging.getLogger('HTTP')     # creating logger with name 'HTTP'         
        logger.setLevel(3)                     # setting up lowest log level for this logger
        logger.addHandler(ch)                  # adding handler (file handler which would write into the log file) to the logger
              
run(HTTPServer, HttpProcessor)          # starting main procedure with standart HTTP server and our self-written HTTP Processor
    
