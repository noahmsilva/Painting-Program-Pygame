import pygame

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 600))
    # set the title of the display window
    pygame.display.set_caption('Save File Concept')
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit() 

class Game:
    # An object in this class represents a complete game.
    
    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object
    
        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('cornflowerblue')
    
        self.FPS = 144
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True  
        
        # === game specific objects
        self.moving_sprites = pygame.sprite.Group()
        self.cursor = Cursor()
        self.moving_sprites.add(self.cursor)

        self.blocks = Blocks(self.surface)

        self.rect_save = pygame.Rect([25,515],[200,70])
        self.rect_open = pygame.Rect([275,515],[200,70])

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.
    
        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
                        
            if self.continue_game:
                self.draw()
                self.update()
                #self.decide_continue()
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second         
    
    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True 
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            if event.type == pygame.KEYUP:
                self.handle_keyup(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event.pos)
        
    def handle_keydown(self, event):
        
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if self.cursor.cursor_location[1] > 0:
                self.cursor.cursor_location[1] -= 1
        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if self.cursor.cursor_location[1] < 15:
                self.cursor.cursor_location[1] += 1
                self.cursor.lock = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if self.cursor.cursor_location[0] > 0:
                self.cursor.cursor_location[0] -= 1
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if self.cursor.cursor_location[0] < 15:
                self.cursor.cursor_location[0] += 1  
        if event.key == pygame.K_1:
            self.blocks.arr[self.cursor.cursor_location[1]][self.cursor.cursor_location[0]] = 0
        if event.key == pygame.K_2:
            self.blocks.arr[self.cursor.cursor_location[1]][self.cursor.cursor_location[0]] = 1
        if event.key == pygame.K_3:
            self.blocks.arr[self.cursor.cursor_location[1]][self.cursor.cursor_location[0]] = 2
        if event.key == pygame.K_4:
            self.blocks.arr[self.cursor.cursor_location[1]][self.cursor.cursor_location[0]] = 3
        if event.key == pygame.K_q:
            for row in self.blocks.arr:
                print(row)
    
    def handle_keyup(self, event):

        if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.cursor.lock = True
            self.cursor.accumulate_hold = 0

    def handle_mouse_up(self, event_location):

        # Save Button
        if self.rect_save.collidepoint(event_location):
            self.f = open("save_file.txt", "w")
            with open('save_file.txt', 'w') as f:
                for row in self.blocks.arr:
                    f.write("%s\n" % row)
            self.f.close()
                
        # Open Button
        if self.rect_open.collidepoint(event_location):
            self.f = open("save_file.txt", "r")
            self.read_data_list = []
            text_from_file = self.f.read()
            for item in text_from_file:
                if  48 <= ord(item) <= 57:
                    self.read_data_list.append(item)
            self.read_data = ''.join(self.read_data_list)

            i = 0
            for row in range(16):
                for col in range(16):
                    self.blocks.arr[row][col] = int(self.read_data[i])
                    i+=1
                    
            self.f.close()

    # main draw funct, draws gridsheet and calls to draw other objects
    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw
        
        self.surface.fill(self.bg_color) # clear the display surface first

        self.surface.blit(pygame.image.load("save.png"), self.rect_save)
        self.surface.blit(pygame.image.load("open.png"), self.rect_open)

        self.blocks.draw()

        # draw 16x16 grid
        for x in range(17):
            if x == 0:
                for y in range(16):
                    pygame.draw.line(self.surface, pygame.Color('black'), [int((500/16) * y), 0], [int((500/16) * y), 500], 2)
            pygame.draw.line(self.surface, pygame.Color('black'), [0,int((500/16) * x)], [500, int((500/16) * x)], 2)   

        # fast down
        if self.cursor.lock == False and self.cursor.cursor_location[1] < 15:
            self.cursor.accumulate_hold += self.cursor.cursor_hold_speed
            self.cursor.cursor_location[1] += int(self.cursor.accumulate_hold)

        self.moving_sprites.draw(self.surface)

        #self.surface.blit(pygame.image.load("attack1.png"), self.rect_attack1)

        pygame.display.update() # make the updated surface appear on the display

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        self.moving_sprites.update(0.095)

class Cursor(pygame.sprite.Sprite):
    # An object in this class represents a cursor

    def __init__(self):
        super().__init__()
        self.cursor_location = [7,7]
        self.cursor_hold_speed = 0.01
        self.accumulate_hold = 0
        self.sprites = []
        self.current_sprite = 0
        self.lock = True

        self.sprites.append(pygame.image.load('pointer1.png'))
        self.sprites.append(pygame.image.load('pointer2.png'))
        self.sprites.append(pygame.image.load('pointer3.png'))
        self.sprites.append(pygame.image.load('pointer4.png')) 
        self.sprites.append(pygame.image.load('pointer5.png')) 
        self.sprites.append(pygame.image.load('pointer6.png')) 
        self.sprites.append(pygame.image.load('pointer7.png')) 
        self.sprites.append(pygame.image.load('pointer6.png')) 
        self.sprites.append(pygame.image.load('pointer5.png')) 
        self.sprites.append(pygame.image.load('pointer4.png')) 
        self.sprites.append(pygame.image.load('pointer3.png'))
        self.sprites.append(pygame.image.load('pointer2.png'))

        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [int(500/16 * self.cursor_location[0] + 29), int(500/16 * self.cursor_location[1] + 19)]

    def update(self, speed):
        # Update the cursor pointing at a tile
        self.rect.topleft = [int(500/16 * self.cursor_location[0] + 27), int(500/16 * self.cursor_location[1] + 19)]

        self.current_sprite += speed

        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0

        # flips hand if it is at the furthest x value
        if self.cursor_location[0] >= 15:
            self.rect.topleft = [500/16 * (self.cursor_location[0] - 1) + 5, 500/16 * self.cursor_location[1] + 20]
            self.image = pygame.transform.flip(self.sprites[int(self.current_sprite)], True, False)
        else:
            self.image = self.sprites[int(self.current_sprite)]

class Blocks():
    
    def __init__(self,surface):
        # Make array where each value is initalized to 0
        self.surface = surface
        self.rows, self.cols = (16, 16)
        self.arr=[]
        for i in range(self.rows):
            self.col = []
            for j in range(self.cols):
                self.col.append(0)
            self.arr.append(self.col)

    def draw(self):
        for x in range(16):
            for y in range(16):
                pygame.draw.rect(self.surface, self.corresponding_color(x,y), pygame.Rect(int((500/16) * y), int((500/16) * x), 32, 32))

    def corresponding_color(self, x, y):
        if self.arr[x][y] == 0:
            return(pygame.Color('cornflowerblue'))
        elif self.arr[x][y] == 1:
            return(pygame.Color('darkolivegreen3'))
        elif self.arr[x][y] == 2:
            return(pygame.Color('cornsilk1'))
        elif self.arr[x][y] == 3:
            return(pygame.Color('goldenrod'))
        else:
            return(pygame.Color('black'))

    

main()     

# DONE - Make mouse icon that starts near center of grid, and track position of cursor, move using wasd.
# 2 200px long buttons for save icon and open icon. 25px buffer on left and right of each button, which means 50px between them
# Make 15px buffers on top and bottom (200,70)