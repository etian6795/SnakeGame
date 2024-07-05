import pygame
import time
import random

class Snake:
    def __init__(self, game_width, game_height):
        # set game dimensions and tile size
        self.tile_size = 25
        self.game_width = game_width
        self.game_height = game_height
        # initialize snake properties
        self.head = [self.game_width//2, self.game_height//2]
        self.tails = []
        self.vel = [1, 0]
        self.length = 4
        self.open_tiles = set([])
        # set of open tiles for places to put apple
        for i in range(0, self.game_width):
            for j in range(0, self.game_height):
                self.open_tiles.add(i+j*self.game_width)
        # start with length of 4
        for i in range(3):
            self.tails.append([self.head[0] - (3-i), self.head[1]])
            self.open_tiles.remove(self.head[0] - (3-i) + self.head[1]*self.game_width)
        self.open_tiles.remove(self.head[0] + self.head[1]*self.game_width)

        self.runGame()

    def runGame(self):
        # start pygame screen
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode((self.game_width * self.tile_size, self.game_height * self.tile_size))
        self.fps = pygame.time.Clock()
        # place fruit
        self.fruit_pos = random.choice(list(self.open_tiles))
        self.open_tiles.remove(self.fruit_pos)
        # start game logic
        while True:
            # check for a key press
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return self.length
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.vel != [0, 1]:
                        self.vel = [0, -1]
                        break
                    elif event.key == pygame.K_DOWN and self.vel != [0, -1]:
                        self.vel = [0, 1]
                        break
                    elif event.key == pygame.K_LEFT and self.vel != [1, 0]:
                        self.vel = [-1, 0]
                        break
                    elif event.key == pygame.K_RIGHT and self.vel != [-1, 0]:
                        self.vel = [1, 0]
                        break
            # move snake
            self.move()
            # check bounds for game over
            if self.head[0] < 0 or self.head[1] < 0 or self.head[0] >= self.game_width or self.head[1] >= self.game_height or self.head in self.tails:
                self.game_over(False)
                return
            # draw game state
            self.screen.fill((15, 15, 15)) # black color for background
            self.draw_snake()

            pygame.display.update()
            self.fps.tick(10)

    def move(self):
        self.tails.append([self.head[0], self.head[1]])
        self.head[0] += self.vel[0]
        self.head[1] += self.vel[1]
        if self.fruit_pos != self.head[0] + self.head[1]*self.game_width:
            self.open_tiles.add(self.tails[0][0] + self.tails[0][1]*self.game_width)
            del self.tails[0]
            if self.head[0] + self.head[1]*self.game_width in self.open_tiles:
                self.open_tiles.remove(self.head[0] + self.head[1]*self.game_width)
        else:
            self.length += 1
            if len(self.open_tiles) == 0:
                self.game_over(True)
                return
            self.fruit_pos = random.choice(list(self.open_tiles))
            self.open_tiles.remove(self.fruit_pos)

    def draw_snake(self):
        # green color for snake
        pygame.draw.rect(self.screen, (43, 140, 24), pygame.Rect(self.head[0] * self.tile_size, self.head[1] * self.tile_size, self.tile_size-1, self.tile_size-1))
        # draw eyes
        if self.vel == [1, 0]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [-1, 0]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [0, 1]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [0, -1]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
        prev_x = self.head[0]
        prev_y = self.head[1]
        idx = len(self.tails)-1
        while idx >= 0:
            pygame.draw.rect(self.screen, (43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, self.tails[idx][1] * self.tile_size, self.tile_size-1, self.tile_size-1))
            from_dir = self.dir(prev_x, prev_y, self.tails[idx][0], self.tails[idx][1])
            # based on where the previous segment is, make the current segment connect with it
            if from_dir == 'U':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, self.tails[idx][1] * self.tile_size -1, self.tile_size-1, 1))
            if from_dir == 'D':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, (self.tails[idx][1]+1) * self.tile_size -1, self.tile_size-1, 1))
            if from_dir == 'L':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size -1, self.tails[idx][1] * self.tile_size, 1, self.tile_size-1))
            if from_dir == 'R':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect((self.tails[idx][0]+1) * self.tile_size -1, self.tails[idx][1] * self.tile_size, 1, self.tile_size-1))
            prev_x = self.tails[idx][0]
            prev_y = self.tails[idx][1]
            idx-=1
        # red color for apple
        pygame.draw.rect(self.screen, (198, 41, 41), pygame.Rect((self.fruit_pos%self.game_width) * self.tile_size, (self.fruit_pos//self.game_width) * self.tile_size, self.tile_size, self.tile_size))

    def dir(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 < y2:
                return 'U'
            else:
                return 'D'
        elif y1 == y2:
            if x1 < x2:
                return 'L'
            else:
                return 'R'

    def game_over(self, won):
        # creating font object
        my_font = pygame.font.SysFont('times new roman', self.tile_size*self.game_width//10)
        # creating a text surface to draw text
        game_over_surface = my_font.render('Your Score: '+str(self.length), True, 'blue')
        if won:
            game_over_surface = my_font.render('You Won!', True, 'blue')
        # create a rectangular object for the text surface object
        game_over_rect = game_over_surface.get_rect()
        # setting position of the text
        game_over_rect.midtop = (self.game_width*self.tile_size/2, self.game_height*self.tile_size/4)
        # blit will draw the text on screen
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        # quit after 2 seconds
        time.sleep(2)
        pygame.quit()
# grid must have even side lengths
snake = Snake(20, 20)
