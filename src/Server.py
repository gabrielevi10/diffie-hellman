import socket
from DiffieHellman import DiffieHellman
import pyaes

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
      while True:
        msg = con.recv(1024)
        if not msg:
          break
        print("Encrypted message received: " + str(msg))
        message = self.__decrypt_message(msg)
        print("Decrypted message: " + message.decode('utf-8'))
      self.__session_estabilished = False

  def __receive_generator_and_prime(self, con):
    generator = int(con.recv(1024))  
    prime = int(con.recv(1024))
    return generator, prime
  
  def __establish_session(self, con):
    generator, prime = self.__receive_generator_and_prime(con)

    diffie_hellman = DiffieHellman(generator, prime)
    result = diffie_hellman.get_result()
    result_from_client = int(con.recv(1024))
    con.send(bytes(str(result), 'utf8'))
    
    self.__key = diffie_hellman.calculate_shared_secret(result_from_client)
    self.__session_estabilished = True
    print("Session key: " + str(self.__key))

    self.__key = self.__key.to_bytes(32, byteorder = "big")

    self.__aes = pyaes.AESModeOfOperationCTR(self.__key)

  def __decrypt_message(self, message):
    message = self.__aes.decrypt(message) 
    return message

if __name__ == "__main__":
  server = Server("", 5000)
  server.listen()