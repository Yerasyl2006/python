import pygame

pygame.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption('Bad - Media - Player')
# music_list = ['song1.mp3','song2.mp3','song3.mp3','song4.mp3','song5.mp3','song6.mp3']
music_list = ['song1.mp3','song2.mp3','song3.mp3','song4.mp3','song5.mp3','song6.mp3']


SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

c = 0
paused = False  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RIGHT:
              c += 1
              if c > len(music_list) - 1:
                c = 0
              pygame.mixer.music.stop()
              pygame.mixer.music.load(music_list[c])
              pygame.mixer.music.play(-1)
            
            if event.key == pygame.K_LEFT:
               c -= 1
               if c < 0:
                    c = len(music_list) - 1
               pygame.mixer.music.stop()
               pygame.mixer.music.load(music_list[c])
               pygame.mixer.music.play(-1)
            
            if event.key == pygame.K_SPACE:
               if paused:
                    pygame.mixer.music.unpause()  
                    paused = False
               else:
                    pygame.mixer.music.pause()  
                    paused = True

    screen.fill((255, 255, 255))
    pygame.display.flip()
