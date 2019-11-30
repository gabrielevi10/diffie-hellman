import socket
from Math import Math
from DiffieHellman import DiffieHellman
import pyaes

class Client:
  def __init__(self, host, port):
    destination = (host, port)
    self.__tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__tcp_client.connect(destination)
  
  def establish_session(self):
    generator, prime = Math.generate_generator_and_prime(256)
    self.__tcp_client.send(bytes(str(generator), 'utf8'))
    self.__tcp_client.send(bytes(str(prime), 'utf8'))
    
    diffie_hellman = DiffieHellman(generator, prime)
    result = diffie_hellman.get_result()
    
    self.__tcp_client.send(bytes(str(result), 'utf8'))
    
    result_from_server = int(self.__tcp_client.recv(1024))

    self.__key = diffie_hellman.calculate_shared_secret(result_from_server)

    print("Session key: " + str(self.__key))
    
    self.__key = self.__key.to_bytes(32, byteorder = "big")
    print(len(self.__key))
    
    self.__aes = pyaes.AESModeOfOperationCTR(bytes(str(self.__key), 'utf8'))

  def send_message(self, message):
    message = self.__aes.encrypt(message)
    self.__tcp_client.send(bytes(message, 'utf8'))

if __name__ == "__main__":
  client = Client("localhost", 5000)
  client.establish_session()
  while True:
    msg = input("Type your message to the server: ")