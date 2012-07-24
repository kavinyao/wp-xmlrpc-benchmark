#!/usr/bin/env python

# Source: http://naxxfish.eu/2011/xml-rpc-benchmarking/

# This script benchmarks XML-RPC performance
# use redirection of your shell to save results!

from twisted.web.xmlrpc import Proxy
from twisted.internet import reactor
from generator import generate_methods
import sys
import datetime
import itertools

class Request():
    _id = itertools.count(1)

    def __init__(self, url, method, params, log_file, err_file):
        self.id = self._id.next()
        self.url = url
        self.method = method
        self.params = params
        self.start_time = 0
        self.end_time = 0
        self.value =  ""
        self.error = ""
        self.finished = False
        self.log_file = log_file
        self.err_file = err_file

    def addCallback(self, callback):
        self.callback = callback

    def addErrback(self, errback):
        self.errback = errback

    def makeRequest(self):
        proxy = Proxy(self.url)
        proxy.callRemote(self.method,*self.params).addCallbacks(self.retSuccess, self.retFail)
        self.start_time = datetime.datetime.now()
        self.log_file.write('%s/%d/%s/start\n' % (self.start_time, self.id, self.method))

    def __returned(self):
        self.end_time = datetime.datetime.now()
        #sys.stderr.write('request[%d] finished!\n' % self.id)

    def retSuccess(self, value):
        self.__returned()
        self.log_file.write('%s/%d/%s/end\n' % (self.end_time, self.id, self.method))
        self.finished = True
        self.value = value
        self.callback(self,value)

    def retFail(self, error):
        self.__returned()
        self.err_file.write('%s/%d/%s/%s/end\n' % (self.end_time, self.id, self.method, error))
        self.finished = True
        self.error = error
        self.callback(self,error)

    def isFinished(self):
        return self.finished

    def getTime(self):
        return (self.end_time - self.start_time) # this should be a timedelta

class Benchmark():
    def __init__(self, url, concurrent, total, methods, log_file_name):
        self.url = url
        self.concurrent_reqs = concurrent
        self.total_reqs = total
        self.methods = iter(methods)
        self.log_file = open(log_file_name, 'w')
        self.err_file = open(log_file_name + '-error', 'w')

        self.open_reqs = 0
        self.current_reqs = 0

    def makeLog(self, filename):
        #self.log_file = open(filename,'w+')
        pass

    def makeRequest(self):
        method, params = self.methods.next()
        req = Request(self.url, method, params, self.log_file, self.err_file)
        req.addCallback(self.reqSuccess)
        req.addErrback(self.reqError)
        req.makeRequest()
        self.open_reqs = self.open_reqs + 1

    def printReqDetail(self, req):
        #print "Request time: %d ms" % req.getTime().microseconds
        delta = req.getTime()
        #print delta

    def reqFinished(self, req):
        #self.printReqDetail(req)
        self.open_reqs = self.open_reqs - 1
        self.current_reqs = self.current_reqs + 1 # completed requests
        if ((self.current_reqs + self.open_reqs) < self.total_reqs):
            self.makeRequest()
        else:
            if self.open_reqs == 0:
                self.log_file.close()
                self.err_file.close()
                reactor.stop() # made as many requests as we wanted to

    def reqSuccess(self,req,value):
        self.reqFinished(req)
        #print repr(value)

    def reqError(self,req, error):
        self.reqFinished(req)
        #print 'error', error

    def setupReqs(self):
        for i in range(0,self.concurrent_reqs): # make the initial pool of requests
            self.makeRequest()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write('Usage: %s config_file concurrent_request_number total_request_number\n' % (sys.argv[0]))
        exit(1)

    config = __import__(sys.argv[1].split('.')[0])

    concurrent_reqs = int(sys.argv[2])
    total_reqs = int(sys.argv[3])
    filename = 'log%d-%d-%s' % (concurrent_reqs, total_reqs, datetime.datetime.now().strftime('%m-%d-%H:%M:%S'))

    methods = generate_methods(config.method_specification, config.site_info, total_reqs)

    benchmark = Benchmark(config.site_info['endpoint'], concurrent_reqs, total_reqs, methods, filename)
    benchmark.setupReqs()

    reactor.run() # start the reactor!
