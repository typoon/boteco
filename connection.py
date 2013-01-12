import socket
import select

class Connection:
    _instance = None
    is_connected = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
            
        return cls._instance

    def connect(self, host, port):
        self._host = host
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._host, self._port))
        self.is_connected = True

    def disconnect(self):
        self._sock.shutdown(socket.SHUT_RDWR)
        self._sock.close()
        self.is_connected = False

    def send(self, data):
        print("Sending %s\n" % data)
        self._sock.send(bytes(data + "\r\n", "utf-8"))

    def read_line(self):
        
        check = select.select([self._sock], [], [], 10)
        if check[0] == []:
            return ""

        line = b''

        try:
            while 1:
                b = self._sock.recv(1)
                line += b

                # Next byte is the last, read it and get out!
                if b == b'\r':
                    line += self._sock.recv(1)
                    break
                    
        except:
            print("error reading byte")

        
        return line.decode("utf-8").strip()
