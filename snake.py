import pygame
from random import randint
import random
pygame.init()
import os
import math
import neat


WIDTH = 500
HEIGHT = 500
screen = pygame.Surface(size=(WIDTH,HEIGHT))

# input parameter for neural network

# distance from snake head

# 1. north,north-south ,south,south-east,east,east-west , west,west-north wall distance   8
# 2.direction ---> up,left,right,down  4
# 3. distance from food,food-north,food-south,food-east,fooed-west  5 
# 4. snake size 1 
# distance from the tail -- -4
# 5 



white = pygame.Color(255,255,255)
red = pygame.Color(255,0,0)
blue = pygame.Color(0,0,255)
green = pygame.Color(0,255,0)

# x = 
choose = ["up","left","right","down"]
class Snake:
    def __init__(self) -> None:
        self.segements = [[WIDTH//2,WIDTH//2],
                        [WIDTH//2,WIDTH//2 +10],
                        [WIDTH//2,WIDTH//2 +20]]
        self.head = self.segements[0]
        self.width = 10
        self.height =10      
        self.direction = random.choice(choose)
        # self.direction = "right"
        self.change_to = self.direction 
        
        self.vel = 10

    def add_segement(self,x,y):
        self.segements.append([x,y])

    def draw(self,win):
        x = 1
        for pos in self.segements:
            if x  == 1:
                pygame.draw.rect(win,green,rect=(pos[0],pos[1],self.width,self.height))
                # pygame.draw.circle(win,green,center=(pos[0],pos[1]),radius=self.height,width=self.width)
                x+=1
            else:
                pygame.draw.rect(win,blue,rect=(pos[0],pos[1],self.width,self.height))
                # pygame.draw.circle(win,blue,center=(pos[0],pos[1]),radius=self.height,width=self.width)
                x+=1
        

    def move(self):
        for i in range(len(self.segements)-1,0,-1):
            self.segements[i][0] =self.segements[i-1][0]
            self.segements[i][1] =self.segements[i-1][1]

        if self.direction == "up":
            self.head[1] -= self.vel
        if self.direction == "down":
            self.head[1] +=self.vel
        if self.direction == "left":
            self.head[0] -=self.vel
        if self.direction == "right":
            self.head[0] +=self.vel
            

    

class Food:
    def __init__(self) -> None:
        self.width = 10
        self.height  = 10
        self.position = [i*10 for i in range(1,WIDTH//10)]
        self.x =  self.position[randint(5,WIDTH//10 -5)]
        self.y =  self.position[randint(5,WIDTH//10 -5)]
        


    def draw(self,win):
        pygame.draw.rect(win,(255,0,0),rect=(self.x,self.y,self.width,self.height))
        # pygame.draw.circle(win,green,center=(self.x,self.y),radius=self.height//2,width=self.width)

    def new_position(self,win):
        self.x = self.position[randint(5,WIDTH//10 -5)]
        self.y = self.position[randint(5,WIDTH//10 -5)]
        self.draw(win)

    
    


class Score:
    pass

    def draw(self,win):
        pass

def draw_window(win,snakes,food,score):
    win.blit(screen,(0,0))
    for sap in snakes:
        sap.draw(win)
    food.draw(win)
    score.draw(win)

    pygame.display.update()



    

def main(genoms,config):


    neural_network = []
    snakes = []
    ge = []

    for _,g in genoms:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        neural_network.append(net)
        snakes.append(snake:=Snake())
        g.fitness = 0
        ge.append(g)
    win = pygame.display.set_mode((WIDTH,HEIGHT))

    clock = pygame.time.Clock()

    
    

    food  = Food()
    food.draw(win)




    score = Score()
    run = True
    x = 10
    count = 0

# game loop
    while run:

# refresh rate
        # clock.tick(frame_rate)
        clock.tick(60)


        if len(snakes) <=  0:
            run = False

# getting event
        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        
        for x,sap in enumerate(snakes):
            sap.move()
            W = sap.head[0]
            E = WIDTH  - W
            N = sap.head[1]
            S = HEIGHT - N
    
    
            # 1 tail distance
            tail_distance = math.dist([sap.head[0],sap.head[1]],[sap.segements[-1][0],sap.segements[-1][1]])
            
            # 1 food distance from snake head
            food_distance = math.dist([sap.head[0],sap.head[1]],[food.x,food.y])
            
            food_x = sap.head[0] - food.x
            food_y= sap.head[1] - food.y
            
            food_north = food.y
            food_west = food.x
            food_east = WIDTH - food_west
            food_south = HEIGHT - food_north
            
            
            NW = (sap.head[1] - food_north)
            SW = (sap.head[1] - food_south)
            ES = (sap.head[0] - food_east)
            NE = (sap.head[0] - food_west)
    
            # 1 snake length
            snake_length = len(sap.segements)
    
            # ge[x].fitness += 1
            # input for neural network
            output = neural_network[x].activate([N,S,E,W,NW,SW,ES,NE,food_east,food_north,food_south,food_west,food_distance,food_x,food_y,tail_distance,snake_length])
            print(output)


            max_out = 0
            index = None
            for y,out in enumerate(output):
                if out > max_out:   
                    max_out = out
                    index = y

            if index==2  and  not sap.direction == "up":
                sap.direction =  "down"
            if index==0  and not sap.direction == "down":
                sap.direction = "up"
            if index==3  and not sap.direction == "right":
                sap.direction = "left"
            if index==1  and not sap.direction == "left":
                sap.direction = "right"

        print(count)
        count += 1
        
                



# game over
        for x,sap in enumerate(snakes):
            if sap.head[0] < 0:
                ge[x].fitness-=5
                snakes.pop(x)
                neural_network.pop(x)
                ge.pop(x)
                # run = False
            elif sap.head[1] <0:
                ge[x].fitness-=5
                snakes.pop(x)
                neural_network.pop(x)
                ge.pop(x)
                # run = False
            elif sap.head[0] >WIDTH-10:
                ge[x].fitness-=5
                snakes.pop(x)
                neural_network.pop(x)
                ge.pop(x)
                # run = False
            elif sap.head[1] >HEIGHT-10:
                ge[x].fitness-=5
                snakes.pop(x)
                neural_network.pop(x)
                ge.pop(x)
                # run = False
            if count > 500:
                ge[x].fitness -=20
                ge.pop(x)
                snakes.pop(x)
                neural_network.pop(x)
                count = 0
            match count:
                case   200:
                    ge[x].fitness -=2
                case   300:
                    ge[x].fitness -=4
                case   400:
                    ge[x].fitness -=6
                case   450:
                    ge[x].fitness -=8

        # for x,sap in enumerate(snakes):
        #     for pos in range(1,len(sap.segements)):
        #         if sap.head == sap.segements[pos]:
        #             print("game over")
        #             ge[x].fitness-=1
        #             snakes.pop(x)
        #             neural_network.pop(x)
        #             ge.pop(x)
        #             run=False



# collide
        for y,sap in enumerate(snakes):
            # if food_distance <50:
            #     ge[y].fitness +=2
            # elif food_distance < 30:
            #     ge[y].fitness += 3
            # elif food_distance < 20:
            #     ge[y].fitness +=5
        
            if (sap.head[0] - food.x == 0 ) and (sap.head[1] -food.y == 0 ):
                print("collide")
                yes = True
                ge[y].fitness += 20
                # if frame_rate <20:
                #     frame_rate+=1
                # else:
                #     frame_rate = 20
            else:
                yes = False
# adding new snake and food
            if yes:
                food.new_position(win)
                sap.add_segement(sap.segements[-1][0],sap.segements[-1][1]+1)
                # print("segement")
                count  = 0

        
                

# refreshing screen
        draw_window(win,snakes,food,score)

# want to continue
        # if run  == False:







def run(config_path):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    
    p = neat.Population(config)



    # adding report yo run in terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))


    winner = p.run(main,300)


    print(f"best genom is {winner}")




    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
    