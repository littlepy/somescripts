#!/opt/anaconda386/bin/python

from Sunlink import Sunlink

def main():
    print("start")
    sunlink = Sunlink()
    ret = sunlink.svr_rcv()
    for i in ret:
        print(i)
    sunlink.sunlink.tapi_svrend()
    print("end")
    


main()