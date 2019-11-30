import socket
from Math import Math
from DiffieHellman import DiffieHellman

# HOST = '127.0.0.1'     # Endereco IP do Servidor
# PORT = 5000            # Porta que o Servidor esta
# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# dest = (HOST, PORT)
# tcp.connect(dest)
# print 'Para sair use CTRL+X\n'
# msg = raw_input()
# while msg <> '\x18':
#     tcp.send (msg)
#     msg = raw_input()
# tcp.close()

class Client:
  def __init__(self, host, port):
    destination = (host, port)
    self.__tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__tcp_client.connect(destination)
  
  def establish_session(self):
    generator, prime = Math.generate_generator_and_prime(128)
    self.__tcp_client.send(bytes(str(generator), 'utf8'))
    self.__tcp_client.send(bytes(str(prime), 'utf8'))
    
    diffie_hellman = DiffieHellman(generator, prime)
    result = diffie_hellman.get_result()
    
    self.__tcp_client.send(bytes(str(result), 'utf8'))
    
    result_from_server = int(self.__tcp_client.recv(1024))

    self.__key = diffie_hellman.calculate_shared_secret(result_from_server)

    print("Session key: " + str(self.__key))


if __name__ == "__main__":
  client = Client("localhost", 5000)
  client.establish_session()