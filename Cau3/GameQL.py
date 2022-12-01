import pygame, sys
from pygame.locals import *
import random
import time
class UFO:
    pygame.init()
    fuel = 200
    position = [0,0]
    speed = [0,0]
    acceleration = [0,0]
    mass = 1
    constT = 1/25
    power = 6
    background = pygame.image.load('background.png')
    up = [pygame.image.load('up.png'),pygame.image.load('up1.png')]
    down = [pygame.image.load("down.png"),pygame.image.load("down1.png")]
    left = [pygame.image.load("left.png"),pygame.image.load("left1.png")]
    right = [pygame.image.load("right.png"),pygame.image.load("right1.png")]
    none = pygame.image.load("none.png")
    clock = pygame.time.Clock()
    def doAction(self, action):      #action = 0 don't do every thing, 1=left,2=right,3=down,4=up
        end = 0
        success = 0
        rewar = 0
        self.acceleration = [0,2]
        if action == 0:
            rewar = -0.1
        elif action == 1:
            self.acceleration[0] += -self.power/self.mass
            rewar = -0.1
            self.fuel -= 1
        elif action == 2:
            self.acceleration[0] += self.power/self.mass
            rewar = -0.1
            self.fuel -= 1
        elif action == 3:
            #self.acceleration[1] += self.power/self.mass
            rewar = -0.1
            self.fuel -= 1
        elif action == 4:
            self.acceleration[1] += -self.power/self.mass
            rewar = -0.1
            self.fuel -= 1
        self.speed[0] += self.acceleration[0]*self.constT 
        self.speed[1] += self.acceleration[1]*self.constT
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]
        if self.speed[0] > 14:
            self.speed[0] = 14
        if self.speed[0] < -14:
            self.speed[0] = -14
        if self.speed[1] < -14:
            self.speed[1] = -14
        if self.speed[1] > 20:
            self.speed[1] = 20
        state = [self.position[0],self.position[1],self.speed[0],self.speed[1]]
        if self.position[1] >= 494:
            if self.position[0] > 170 and self.position[0] < 195:
                if abs(self.speed[0]) <= 3 and abs(self.speed[1]) <= 3:
                    success = 1
                    rewar = 10
                    end = 1
                else:
                    rewar = -0.5
                    end = 1
            else:
                rewar = -1
                end = 1
        if self.position[0] <= -14:
            self.position[0] = -14
            end = 1
            rewar = -5
        if self.position[0] >= 400:
            self.position[0] = 400
            end = 1
            rewar = -5
        if self.position[1] <= -1:
            self.position[1] = -1
        if self.position[1] >= 510:
            self.position[1] = 510
        if self.fuel <= 0:
            end = 1
            rewar = -0.1
        state = [self.position[0],self.position[1],self.speed[0],self.speed[1]]
        return state, end, rewar, self.fuel, success
        
    def __init__(self,position,speed,acceleration):
        print("+==================================================+")
        print("| Thư viện học tăng cường UFO được thực hiện bởi   |")
        print("| Nguyễn Thanh Toàn. Bạn có thể xem chi tiết tại   |")
        print("| Github.com/nttoan-khiem/Q_learning.              |")
        print("| Thanks pygame have support this libary.          |")
        print("+==================================================+")
        time.sleep(2)
        self.position = position
        self.speed = speed
        self.acceleration = acceleration
    
    def getPosision(self):
        return self.position
    
    def setPosision(self, x,y):
        self.position = [x,y]
        
    def render(self,action):
        screen = pygame.display.set_mode([400,600])
        index = 0
        self.clock.tick(20)
        screen.blit(self.background,([0,0]))
        if action == 0:
            image = self.none
            screen.blit(image,(self.position[0]-4,self.position[1]-13))
            pygame.display.update()
        elif action == 1:
            image = self.left[index]
            if index == 1:
                index = 0
            screen.blit(image,(self.position[0]-4,self.position[1]-13))
            pygame.display.update()
        elif action == 2:
            image = self.right[index]
            if index == 1:
                index = 0
            screen.blit(image,(self.position[0]-4,self.position[1]-13))
            pygame.display.update()
        elif action == 3:
            image = self.down[index]
            if index == 1:
                index = 0
            screen.blit(image,(self.position[0]-4,self.position[1]-13))
            pygame.display.update()
        elif action == 4:
            image = self.up[index]
            if index == 1:
                index = 0
            screen.blit(image,(self.position[0]-4,self.position[1]-13))
            pygame.display.update()
            
    def reset(self):
        self.position[0] = 100
        self.position[1] = 0
        self.speed[0] = 0
        self.speed[1] = 0
        self.fuel = 200
        result = [self.position[0],self.position[1],self.speed[0],self.speed[1]]
        return result
        
    def randomState(self):
        self.fuel = 200
        self.position[0] = random.randint(0,250)
        self.position[1] = random.randint(0,300)
        self.speed[0] = random.randint(-1,2)
        self.speed[1] = random.randint(-1,2)
        result = [self.position[0],self.position[1],self.speed[0],self.speed[1]]
        return result
    
    def setState(self, state):
        self.fuel = 200
        self.position[0] = state[0]
        self.position[1] = state[1]
        self.speed[0] = state[2]
        self.speed[1] = state[3]
        
    def show_xAxis(self):
        return -14,410
    def show_yAxis(self):
        return -1,498
    def show_speedX(self):
        return -14, 14
    def show_speedY(self):
        return -14, 20
    def show_listAction(self):
        print("0: don't do erything, 1:Left, 2:Right, 3:Down, 4:Up")
    def close(self):
        pygame.display.quit()
    
"""
e = UFO([20,0],[0,0],[0,0])
e.reset()
index = 0
actionT = 0
end = 0
posision = [0,0,0,0]
while not end:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                actionT = 4
            elif event.key == K_DOWN:
                actionT = 3
            elif event.key == K_LEFT:
                actionT = 1
            elif event.key == K_RIGHT:
                actionT = 2
            else:
                actionT = 0
        if event.type == KEYUP:
            actionT = 0
    posision,end,rewar,fuel,_ = e.doAction(action=actionT)
    e.render(actionT)
    print("posision is: ",posision)
    print("end: ",end)
    print("rewar: ",rewar)
    print("fuel: ", fuel)
    if posision[0] < 0 or posision[0] >= 400:
        break
    elif posision[1] < 0 or posision[1] >= 600:
        break
"""
#min speed follow x axis is -14
#max speed follow x axis is +14
#max speed follow y axis is +19.6
#min speed follow y axis is -13.9
"""
while True:
    x = input("nhap x0: ")
    y = input("nhap x1: ")
    x = int(x)
    y = int(y)
    e = UFO([x,y],[0,0],[0,0])
    e.render(0)
"""