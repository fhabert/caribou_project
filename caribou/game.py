import numpy as np
import pygame as pg
import random
import math
from pygame.locals import*

pg.init()

# window = pg.display.set_mode((1940, 1100))
window = pg.display.set_mode((600, 600))
window_x, window_y = window.get_size()

pg.display.set_caption('Caribou')
playground = pg.image.load('images/black_bg.jpg')

class Game:
    def __init__(self, num_flock):
        self.nb_dots = 5
        self.dots = self.init_dots()
        self.num_flock = num_flock
        self.flocks = self.init_flock()
        self.defos = []

    def init_dots(self):
        ar = []
        for _ in range(self.nb_dots):
            pos_x = random.randint(0, 600)
            pos_y = random.randint(0, 600)
            dot = Dot(pos_x, pos_y)
            ar.append(dot)
        return ar
    
    def init_flock(self):
        ar = []
        for _ in range(self.num_flock):
            ar.append(Flock())
        return ar

    def draw_game(self):
        window.blit(playground, (0,0))
        self.draw_zones()
        self.draw_flocks()
        pg.display.update()
    
    def draw_zones(self):
        for dot in self.dots:
            defo = Rect(dot.pos_x - 12, dot.pos_y - 12, 25, 25)
            pg.draw.circle(window, (255,255,255), (dot.pos_x, dot.pos_y), 1)
            pg.draw.rect(window, (255, 0, 0), pg.Rect(defo), width=1)
            self.defos.append(defo)
        
    def draw_flocks(self):
        for flock in self.flocks:
            flock.edges()
            flock.steer(self.flocks)
            flock.collision(self.defos)
            flock.update()
            flock.draw()


class Dot:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

class Flock:
    def __init__(self):
        self.position = np.array([random.randint(0, 600), random.randint(0, 600)])
        self.velocity = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        self.acceleration = np.array([0, 0])
        # self.maxSpeed = 4
        self.maxForce = 2
        self.rect = Rect(self.position[0], self.position[1], 8, 8)
    
    def distance(self, pt1, pt2):
        x = (pt1[0] - pt2[0]) ** 2
        y = (pt1[1] - pt2[1]) ** 2
        dis = math.sqrt(x + y)
        return dis

    def edges(self):
        if (self.position[0] > window_x):
            self.position[0] = 0
        elif (self.position[0] < 0):
            self.position[0] = window_x
        
        if (self.position[1] > window_y):
            self.position[1] = 0
        elif (self.position[1] < 0):
            self.position[1] = window_y

    def alignement(self, boids):
        steering = np.array([0, 0])
        total = 0
        perception = 25
        for boid in boids:
            d = self.distance(self.position, boid.position)
            if (boid != self and d < perception):
                total += 1
                steering = np.add(steering, boid.velocity)
        if total > 0:
            steering = np.divide(steering, total)
            steering = np.subtract(steering, self.velocity)
            magn = self.mag(steering)
            if magn > self.maxForce:
                steering[0] = 1
                steering[1] = 1
        return steering

    def cohesion(self, boids):
        steering = np.array([0, 0])
        total = 0
        perception = 30
        for boid in boids:
            d = self.distance(self.position, boid.position)
            if (boid != self and d < perception):
                total += 1
                steering = np.add(steering, boid.position)
        if total > 0:
            steering = np.divide(steering, total)
            steering = np.subtract(steering, self.velocity)
            steering = np.subtract(steering, self.position)
            magn = self.mag(steering)
            if magn > self.maxForce:
                steering[0] = 1
                steering[1] = 1
        return steering
    
    def separation(self, boids):
        steering = np.array([0, 0])
        perception = 5
        total = 0
        for boid in boids:
            d = self.distance(self.position, boid.position)
            if (boid != self and d < perception):
                diff = self.position - boid.position
                diff = np.divide(diff, d*d)
                steering = np.add(steering, diff)
                total += 1
        if total > 0:
            steering = np.divide(steering, total)
            steering = np.subtract(steering, self.velocity)
            magn = self.mag(steering)
            if magn > self.maxForce:
                steering[0] = 1
                steering[1] = 1
        return steering
    
    def collision(self, defos):
        for defo in defos:
            collide = pg.Rect.colliderect(self.rect, defo)
            if collide:
                rand = random.randint(0, 10)
                if rand >= 5:
                    self.position = np.add(self.position, np.array([-0.05, 0.08]))
                else:
                    self.position = np.add(self.position, np.array([-0.05, -0.08]))
    
    def mag(self, vector):
        return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

    def update(self):
        self.position = np.add(self.position, self.velocity)
        self.velocity = np.add(self.velocity, self.acceleration)
        magn = self.mag(self.velocity)
        if magn > self.maxForce:
            self.velocity[0] = 1
            self.velocity[1] = 1
        self.acceleration *= 0
    
    def draw(self):
        self.rect[0] = self.position[0]
        self.rect[1] = self.position[1]
        pg.draw.rect(window, "white", pg.Rect(self.rect))
    
    def steer(self, boids):
        alignement = self.alignement(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        forces = np.add(alignement, separation, cohesion)
        self.acceleration = np.add(self.acceleration, forces)

nb_caribou = 50
game = Game(nb_caribou)
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()
    game.draw_game()

pg.quit()