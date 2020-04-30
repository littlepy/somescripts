from Sunlink import Sunlink






def client():
    sun = Sunlink()
    
    head = dict(
        TrType=b'0001',
        DestNode=b'001',
        Sleng=len(b'hello')
    )
    ret = sun.cli_sndrcv(b'001', head, b'hello', b'')


    for i in ret:
        print(i)



if __name__ == '__main__':
    client()

