import os



class Txt:
    def __init__(self):
        pass
        
    def read(self , path):
        print(path)
        os.chdir(path=path)
        for i in os.listdir():
            if i.endswith(".txt"):
                file = open(i,"r",encoding='utf-8')
                content = file.read()
                return content
                
