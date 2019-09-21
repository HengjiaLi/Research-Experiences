import socket
import pygame


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(),5000))

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption('Remote Webcam Viewer')
font = pygame.font.SysFont("Arial",14)
clock = pygame.time.Clock()

while 1:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
      
  data = client_socket.recv(409600000)
  
  image = pygame.image.frombuffer(data,(80,60),"RGB")
  
  output = image
                            
  screen.blit(output,(0,0))
  
  clock.tick(60)
  pygame.display.flip()
