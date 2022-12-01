import lamport

def f(clock):
    clock.local()
    clock.send(1)
    clock.local()
    clock.recv(1)
    clock.local()

def g(clock):
    clock.recv(0)
    clock.send(0)
    clock.send(2)
    clock.recv(2)
    

def h(clock):
    clock.recv(1)
    clock.send(1)



lamport.wind([f, g, h])()