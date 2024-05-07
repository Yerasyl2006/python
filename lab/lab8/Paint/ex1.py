import pygame

class SceneBase: 
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):# 
        self.SwitchToScene(None)

class DrawingScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.shapes = []  
        self.current_color = (0, 0, 0)  
        self.current_tool = "Rectangle"  
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if self.current_tool == "Rectangle":
                        pos = pygame.mouse.get_pos()
                        rect = pygame.Rect(pos[0], pos[1], 50, 50)  
                        self.shapes.append((rect, self.current_color))
                    elif self.current_tool == "Circle":
                        pos = pygame.mouse.get_pos()
                        circle = (pos[0], pos[1], 25)
                        self.shapes.append((circle, self.current_color))
                    elif self.current_tool == "Eraser":
                    
                        pos = pygame.mouse.get_pos()
                        for shape in self.shapes:
                            if isinstance(shape[0], pygame.Rect) and shape[0].collidepoint(pos):
                                self.shapes.remove(shape)
                            elif isinstance(shape[0], tuple) and ((shape[0][0] - pos[0])**2 + (shape[0][1] - pos[1])**2) <= shape[0][2]**2:
                                self.shapes.remove(shape)
                elif event.button == 3:  
                    
                    self.current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            elif event.type == pygame.KEYDOWN:#клавиш басуын тексереді
                if event.key == pygame.K_r:
                    self.current_tool = "Rectangle"
                elif event.key == pygame.K_c:
                    self.current_tool = "Circle"
                elif event.key == pygame.K_e:
                    self.current_tool = "Eraser"
    
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((255, 255, 255))  
        for shape, color in self.shapes:
            if isinstance(shape, pygame.Rect):
                pygame.draw.rect(screen, color, shape)
            elif isinstance(shape, tuple):
                pygame.draw.circle(screen, color, (shape[0], shape[1]), shape[2])
                
def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)
        
        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen)
        
        active_scene = active_scene.next
        
        pygame.display.flip()
        clock.tick(fps)

run_game(800, 600, 60, DrawingScene())
