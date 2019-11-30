import socket
from DiffieHellman import DiffieHellman

# HOST = ''              # Endereco IP do Servidor
# PORT = 5000            # Porta que o Servidor esta
# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# orig = (HOST, PORT)
# tcp.bind(orig)
# tcp.listen(1)
# while True:
#     con, cliente = tcp.accept()
#     print 'Concetado por', cliente
#     while True:
#         msg = con.recv(1024)
#         if not msg: break
#         print cliente, msg
#     print 'Finalizando conexao do cliente', cliente
#     con.close()

class Server:
  def __init__(self, host, port):
    self.__tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (host, port)
    self.__tcp_server.bind(orig)
    self.__tcp_server.listen(1)
    
    self.__session_estabilished = False

  def listen(self):    
    while True:
      con, client = self.__tcp_server.accept()
      if not self.__session_estabilished:
        self.__establish_session(con)
      msg = con.recv(1024)
      while msg:
        msg = con.recv(1024)
        print(msg)

  def __establish_session(self, con):
    generator = int(con.recv(1024))  
    prime = int(con.recv(1024))
    diffie_hellman = DiffieHellman(generator, prime)

    result = diffie_hellman.get_result()

    result_from_client = int(con.recv(1024))

    con.send(bytes(str(result), 'utf8'))

    self.__key = diffie_hellman.calculate_shared_secret(result_from_client)

    self.__session_estabilished = True

    print("Session key: " + str(self.__key))


if __name__ == "__main__":
  server = Server("", 5000)
  server.listen()