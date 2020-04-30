from cffi import FFI
import sys



class Sunlink:
    ''' Wraper for sunlink c lib '''
    def __init__(self, header="include/sunlink.h"):
        self.ffi = FFI()
        self.ffi.cdef(self.headerFromFile(header))
        self.sunlink = self.ffi.dlopen("lib/libsunlink.so")


    def headerFromFile(self, file):
        header = None
        with open(file) as conf:
            header = conf.read()
        return header

    def cli_sndrcv(self, nodeid, head, reqdata,
                   reqfiles, timeout=60):
        ret, arg_ip, arg_port = self.getaddr(nodeid)
        if ret != 0:
            sys.exit("Can't get address(ip, port)")
        arg_head = self.ffi.new("TAPIHEAD *", head)
        arg_reqdata = self.ffi.new("char [1024]", reqdata)
        arg_reqfiles = self.ffi.new("char [1024]", reqfiles)
        arg_ansdta = self.ffi.new("char [1024]")
        arg_resfiles = self.ffi.new("char [1024]")

        ret = self.sunlink.cli_sndrcv(arg_ip, arg_port[0], arg_head,
                                arg_reqdata, arg_reqfiles,
                                arg_ansdta, arg_resfiles, timeout)
        if ret != 0:
            sys.exit("Send data fail.")

        return tuple(map(self.ffi.string, (arg_ansdta, arg_resfiles)))


        
    def svr_snd(self, head, ansdata, resfiles, timeout=60):
        ret = 0
        arg_head = self.ffi.new("TAPIHEAD *", head)
        arg_ansdta = self.ffi.new("char [1024]", ansdata)
        arg_resfiles = self.ffi.new("char [1024]", resfiles)

        ret = self.sunlink.svr_snd(arg_head, arg_ansdta, 
                                   arg_resfiles, timeout)
        return ret
        


    def svr_rcv(self, timeout=60):
        ret = 0
        arg_head = self.ffi.new("TAPIHEAD *")
        arg_reqdata = self.ffi.new("char [1024]")
        arg_reqfiles = self.ffi.new("char [1024]")

        ret = self.sunlink.svr_rcv(arg_head, arg_reqdata, 
                                   arg_reqfiles, timeout)
        
        return (ret, self.ffi.string(arg_reqdata),
                     self.ffi.string(arg_reqfiles))


    def svrend(self):
        ret = self.sunlink.tapi_svrend()

        return ret

    def getaddr(self, nodeid):
        ret = 0
        arg_svrname = self.ffi.new("char [16]", nodeid)
        arg_ip = self.ffi.new("char [16]")
        arg_port = self.ffi.new("int *")
        ret = self.sunlink.tapi_getaddr(arg_svrname, arg_ip, arg_port)
        
        return (ret, arg_ip, arg_port[0])

