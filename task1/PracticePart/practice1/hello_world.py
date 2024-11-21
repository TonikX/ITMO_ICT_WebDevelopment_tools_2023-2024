from fastapi import FastAPI

app = FastAPI()




@app.get('/default')
def hello_world():
    return 'hello world'


# Это не будет работать, потому что у нас просто вызовается экземпляр класса
@app.get('/class_based')
class HelloWorld:
    def __call__(self):
        return 'hello world'




class ClassWithStr:
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return f'page{self.n}'

#app.get можно скормить любой объект, имеющий str __str__ - ЭТО ЛОЖЬ
# надо обернуть в __str__
@app.get(str(ClassWithStr(1)))
def hello_world_2():
    return 'Hello with class url'
