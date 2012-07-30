import pygame
from pygame.locals import *
import colour
import math
import sys
import time

TABLE_WIDTH, TABLE_HEIGHT, TABLE_COLOUR = 250, 125, colour.dark_green
BORDER = 10
SCREEN_WIDTH, SCREEN_HEIGHT = TABLE_WIDTH + 2 * BORDER, TABLE_HEIGHT + 2 * BORDER
BALL_RADIUS = 9
DECELERATION = 1
X, Y = 0, 1

UPDATE_DISPLAY = False

# Pygame initialisation
pygame.init()
pygame.display.set_caption('GAME')
pygame.key.set_repeat(250, 125)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font('consola.ttf', 20)

table = pygame.Surface((TABLE_WIDTH, TABLE_HEIGHT))
table.fill(TABLE_COLOUR)
screen.blit(table, table.get_rect().move(10, 10))
pygame.display.flip()

class Ball(object):
    def __init__(self, x, y, colour=colour.white):
        self.x, self.y = x, y
        self.colour = colour
        self.speed, self.direction = 0, [0, 0]

    def draw(self, clear=False):
        pygame.draw.circle(table, self.colour if not clear else TABLE_COLOUR, (int(self.x), int(self.y)), BALL_RADIUS + clear)
        if not clear:
            pygame.draw.circle(table, colour.black, (int(self.x), int(self.y)), BALL_RADIUS, 1)    

    def move(self):
        global UPDATE_DISPLAY, objects
        self.draw(True)
        if self.speed:
            UPDATE_DISPLAY = True
            move_x, move_y = self.speed * 0.001, self.speed * 0.001
            self.speed -= DECELERATION #if self.speed > 0 else (-1 * DECELERATION)
            if self.speed <= 0:
               self.speed = 0
               self.direction = [0, 0]

            finished = False
            while not finished:
                self.x += move_x * self.direction[X]
                self.y += move_y * self.direction[Y]
                left, right = self.x - BALL_RADIUS, TABLE_WIDTH - self.x - BALL_RADIUS
                top, bottom = self.y - BALL_RADIUS, TABLE_HEIGHT - self.y - BALL_RADIUS
                if min([top, bottom, left, right]) > 0: # no collision - nothing more to do here.
                    finished = True
                else:
                    # Collisions with two cushions near a corner. No need to worry about the corner itself because pockets will be added.
                    #if left <= 0  and top <= 0:            
                    #    if abs(left) > abs(top):
                    #        pass
                    #    else:
                    #        pass
                    #elif left <= 0  and bottom <= 0:
                    #    if abs(left) > abs(bottom):
                    #        pass
                    #    else:
                    #        pass
                    #elif right <= 0  and top <= 0:
                    #    if abs(right) > abs(top):
                    #        pass
                    #    else:
                    #        pass
                    #elif right <= 0  and bottom <= 0:
                    #    if abs(right) > abs(bottom):
                    #        pass
                    #    else:
                    #        pass
                    # Collisions with a single cushion away from corners
                    if right <= 0:
                        self.direction[X] *= -1
                        self.x = TABLE_WIDTH - BALL_RADIUS
                    elif left <= 0:
                        self.direction[X] *= -1
                        self.x = BALL_RADIUS
                    if bottom <= 0:
                        self.direction[Y] *= -1
                        self.y = TABLE_HEIGHT- BALL_RADIUS
                    elif top <= 0:
                        self.direction[Y] *= -1
                        self.y = BALL_RADIUS

                    finished = True # placeholder remove when finished
            for ball in [item for item in objects if item is not self]:
                self.collide(ball)

    def collide(self, ball):
        diff = distance((self.x, self.y), (ball.x, ball.y))
        if  diff < (2 * BALL_RADIUS): # 2 balls have collided
            self.x -= (2 * BALL_RADIUS - diff) / 2 * self.direction[X]
            self.y -= (2 * BALL_RADIUS - diff) / 2 * self.direction[Y]
            self.direction[X] *= self.speed
            self.direction[Y] *= self.speed
            ball.direction[X] *= ball.speed
            ball.direction[Y] *= ball.speed
            resultant = (self.direction[X] + ball.direction[X], self.direction[Y] + ball.direction[Y])
            self.direction[X], self.direction[Y] = normalize((resultant[X] - self.direction[X], resultant[Y] - self.direction[Y]))
            ball.direction[X], ball.direction[Y] = normalize((resultant[X] - ball.direction[X], resultant[Y] - ball.direction[Y]))
            return True
        return False

def normalize(vector): # Normalize a vector to a length of 1 while retaining its direction
    if vector[X] == 0.0 and vector[Y] == 0.0: # Can't do anything with a zero vector
        return [0.0, 0.0]
    l = pythagoras(vector)
    #print str([vector[X] / l, vector[Y] / l])
    return [vector[X] / l, vector[Y] / l]

def distance(point_1, point_2): # Return the absolute distance between to points
    return pythagoras(((point_1[X] - point_2[X]), (point_1[Y] - point_2[Y])))

def pythagoras(vector):
    return (vector[X] ** 2 + vector[Y] ** 2) ** 0.5

objects = [
           Ball(TABLE_WIDTH // 2, TABLE_HEIGHT - 15, colour.red),
           Ball(TABLE_WIDTH // 2, 15, colour.yellow),
           Ball(TABLE_WIDTH - 50, TABLE_HEIGHT // 2),
           Ball(50, TABLE_HEIGHT // 2, colour.black),
          ]
objects[0].speed = 1750
objects[0].direction = normalize([1, 0])
objects[1].speed = 1500
objects[1].direction = normalize([-1, -1])
objects[2].speed = 1250
objects[2].direction = normalize([1,-1])
objects[3].speed = 1000
objects[3].direction = normalize([0, 1])
UPDATE_DISPLAY = True

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
    if UPDATE_DISPLAY:
        UPDATE_DISPLAY = False
        for ball in objects:
            ball.move()
        for ball in objects:
            ball.draw()
        screen.blit(table, table.get_rect().move(10, 10))
        pygame.display.flip()
        time.sleep(0.01)
    else:
        time.sleep(1)
        sys.exit()