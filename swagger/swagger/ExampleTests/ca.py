def CallMe(param):
    print (param)
def callBackOnErr(err):
    print (err)

lstfunc=[]

def func():
    lst=[1,2,3,4,5,6,7,8]
    for i in range(1,len(lst)+1):
        for f in lstfunc:
            f(lst[-1*i])





def Subscribe(func):
    lstfunc.append(func)

Subscribe(CallMe)
Subscribe(callBackOnErr)
Subscribe(CallMe)
Subscribe(callBackOnErr)
func()