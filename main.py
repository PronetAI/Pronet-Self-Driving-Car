import sys
import pygame
from pygame.locals import *
import math
import math_car
vec = pygame.math.Vector2
pygame.init()
FPS = 60
fps_clock = pygame.time.Clock()
WIDTH = 1200
HEIGHT = 600
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
MAX_SPEED = 9
FSENSOR_LEN = 150
SSENSOR_LEN = 150
FSSENSOR_LEN = int (150 / math.sin(math.radians(45)))
gatesPassed = 0
collisions = 0
laps = 0
inGateZone = False
allSensors = ["F", "R", "L", "FR", "FL", "FRR", "FRL", "FLR", "FLL", "BR", "BL"]
rSensors = ["R", "FR", "FRR", "FRL", "BR"]
lSensors = ["L", "FL", "FLR", "FLL", "BL"]
Q = {}
sensorAngles = [90, -90, 45, -45, 22, -22, 67, -67, 135, -135]
allBounds = [[(100,50), (1100, 50)],[(100,50), (50,100)],[(1100,50), (1150,100)]],
[(50,100), (50,500)],[(1150,100), (1150,500)],[(50,500), (100, 550)]],
[(1150,500), (1100, 550)],[(100,550), (450, 550)],[(1100,550), (650, 550)],
[(450, 550), (500, 500)],[(650, 550), (600, 500)],[(500, 500), (500, 300)]],
[(600, 500), (600, 300)],[(500, 300), (550, 275)],[(600, 300), (550, 275)],
[(175,150), (1025, 150)],[(175,150), (160, 165)],[(1025, 150), (1040, 165)],
[(160, 165), (160, 415)],[(1040, 165), (1040, 415)],[(160, 415), (175, 430)],
[(1040, 415), (1025, 430)],[(175, 430), (375, 430)],[(1025, 430), (735, 430)],
[(735, 430), (720, 415)],[(375, 430), (390, 415)],[(720, 415), (720, 225)],
[(390, 415), (390, 225)],[(720, 225), (700, 210)],[(390, 225), (420, 210)],
(700, 210), (550, 170)]]
allBounds += [[(420, 210), (550, 170)]]
allGates = []
allGates += [[(200, 50), (200, 150)]]
allGates += [[(325, 50), (325, 150)]]
allGates += [[(450, 50), (450, 150)]]
allGates += [[(575, 50), (575, 150)]]
allGates += [[(700, 50), (700, 150)]]
allGates += [[(825, 50), (825, 150)]]
allGates += [[(950, 50), (950, 150)]]
allGates += [[(950, 50), (950, 150)]]
allGates += [[(1033, 158), (1125, 75)]]
allGates += [[(167, 158), (75, 75)]]
allGates += [[(160, 400), (50, 400)]]
allGates += [[(160, 200), (50, 200)]]
allGates += [[(1040, 300), (1150, 300)]]
allGates += [[(1040, 400), (1150, 400)]]
allGates += [[(1040, 200), (1150, 200)]]
allGates += [[(1033, 422), (1125, 525)]]
allGates += [[(167, 422), (75, 525)]]
allGates += [[(345, 430), (345, 550)]]
allGates += [[(225, 430), (225, 550)]]
allGates += [[(1000, 430), (1000, 550)]]
allGates += [[(760, 430), (760, 550)]]
allGates += [[(880, 430), (880, 550)]]
allGates += [[(475, 525), (382, 422)]]
allGates += [[(625, 525), (727, 422)]]
allGates += [[(720, 390), (600, 390)]]
allGates += [[(720, 320), (600, 320)]]
allGates += [[(390, 390), (500, 390)]]
allGates += [[(390, 320), (500, 320)]]
allGates += [[(390, 390), (500, 390)]]
allGates += [[(390, 320), (500, 320)]]
allGates += [[(670, 202), (585, 290)]]
allGates += [[(430, 208), (520, 290)]]
allGates += [[(550, 170), (550, 275)]]
finishLine = [(160, 300), (50, 300)]
allGates += [finishLine]
class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Car.png")
        DISPLAY.blit(self.image, (100, 250))
        self.original_image = self.image
        self.position = vec(100, 250)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.02)
        self.angle_speed = 0
        self.angle = 0
        self.direction = 1
        self.fsensor = None
        self.rsensor = None
        self.lsensor = None
        self.frsensor = None
        self.flsensor = None
        self.frrsensor = None
        self.frlsensor = None
        self.flrsensor = None
        self.fllsensor = None
        self.brsensor = None
        self.blsensor = None
        self.updateSensor()
    def getUpdatedSensor (self, angle):
        start = self.rect.center
        angle = - self.angle + angle
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return pygame.draw.line(DISPLAY, (255, 255, 255), start, end)

    def drawUpdatedSensor (self, angle):
        start = self.rect.center
        angle = - self.angle + angle
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        pygame.draw.line(DISPLAY, (255, 255, 255), start, end)

    def updateSensor (self):
        start = self.rect.center
        angle = - self.angle
        opp = FSENSOR_LEN * math.sin(math.radians(angle))
        adj = FSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        self.fsensor = pygame.draw.line(DISPLAY, (255, 255, 255), start, end)
        self.rsensor = self.getUpdatedSensor(90)
        self.lsensor = self.getUpdatedSensor(-90)
        self.frsensor = self.getUpdatedSensor(45)
        self.flsensor = self.getUpdatedSensor(-45)
        self.frlsensor = self.getUpdatedSensor(22)
        self.flrsensor = self.getUpdatedSensor(-22)
        self.frrsensor = self.getUpdatedSensor(67)
        self.fllsensor = self.getUpdatedSensor(-67)
        self.brsensor = self.getUpdatedSensor(135)
        self.blsensor = self.getUpdatedSensor(-135)
    def drawSensor (self):
        start = self.rect.center
        angle = - self.angle
        opp = FSENSOR_LEN * math.sin(math.radians(angle))
        adj = FSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        pygame.draw.line(DISPLAY, (255, 255, 255), start, end)

        global sensorAngles
        for angle in sensorAngles:
            self.drawUpdatedSensor(angle)

    def getFsensorEnd (self):
        start = self.rect.center
        angle = - self.angle
        opp = FSENSOR_LEN * math.sin(math.radians(angle))
        adj = FSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end

    def getRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 90
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end

    def getLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 90
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end

    def getFRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 45
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end

    def getFLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 45
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end

    def getFLLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 67
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getFLRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 22
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getFRLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 67
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getFRRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 22
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getBRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 135
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getBLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 135
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getBLRsensorEnd (self):
        start = self.rect.center
        angle = - self.angle - 112
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def getBRLsensorEnd (self):
        start = self.rect.center
        angle = - self.angle + 112
        opp = SSENSOR_LEN * math.sin(math.radians(angle))
        adj = SSENSOR_LEN * math.cos(math.radians(angle))
        end = (start[0] - int(opp), start[1] - int(adj))
        return end
    def update(self):
        self.updateSensor()
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rotateLeft()
        if keys[K_RIGHT]:
            self.rotateRight()
        if keys[K_UP]:
            self.vel += self.acceleration
        if keys[K_DOWN]:
            self.vel -= self.acceleration
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        if (self.angle > 270 and self.angle <= 360) or (self.angle >= 0 and self.angle < 90):
            self.direction = 1
        elif self.angle > 90 and self.angle < 270:
            self.direction = -1
        self.position += self.vel
        self.rect.center = self.position
    def rotate(self):
        self.acceleration.rotate_ip(self.angle_speed)
        self.vel.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def rotateRight (self):
        self.angle_speed = 2
        self.rotate()
    def rotateLeft (self):
        self.angle_speed = -2
        self.rotate()
    def slideRight (self):
        self.angle_speed = 0.5
        self.rotate()
    def slideLeft (self):
        self.angle_speed = -0.5
        self.rotate()
    def slowDown(self):
        if (self.vel.length() > 0.5):
            self.vel -= self.acceleration * 2
    def goFaster (self):
        self.vel += self.acceleration * 0.8
all_sprites = pygame.sprite.Group()
car = Car()
all_sprites.add(car)
def drawTrack():
    for line in allBounds:
        pygame.draw.line(DISPLAY, (255, 255, 255), (line[0]), (line[1]))
    for gate in allGates:
        pygame.draw.line(DISPLAY, (0, 255, 0), (gate[0]), (gate[1]))
    pygame.draw.line(DISPLAY, (0, 255, 0), (finishLine[0]), (finishLine[1]), 3)
def checkSensors ():
    global allBounds
    sensors = ""
    sensors = [ [car.rect.center, car.getFsensorEnd(), "F"], [car.rect.center, car.getRsensorEnd(), "R"], [car.rect.center, car.getLsensorEnd(), "L"],
                [car.rect.center, car.getFRsensorEnd(), "FR"], [car.rect.center, car.getFLsensorEnd(), "FL"],
                [car.rect.center, car.getFLLsensorEnd(), "FLL"], [car.rect.center, car.getFLRsensorEnd(), "FLR"],
                [car.rect.center, car.getFRLsensorEnd(), "FRL"], [car.rect.center, car.getFRRsensorEnd(), "FRR"],
                [car.rect.center, car.getBRsensorEnd(), "BR"], [car.rect.center, car.getBLsensorEnd(), "BL"],
                [car.rect.center, car.getBRLsensorEnd(), "BR"], [car.rect.center, car.getBLRsensorEnd(), "BL"] ]
    poiResults = {}
    for line in allBounds:
        for sensor in sensors:
            pt1 = sensor[0]
            pt2 = sensor[1]
            ptA = line[0]
            ptB = line[1]
            poi = math_car.calculatePOI(pt1, pt2, ptA, ptB)
            if (poi == False):
                pass
            else:
                entry = [poi,math_car.distance(pt1, poi), math_car.angleOfIntersection(pt1, pt2, ptA, ptB), sensor[2]]

                if (sensor[2] in poiResults):
                    if ((poiResults[sensor[2]])[1] > entry[1]):
                        poiResults[sensor[2]] = entry
                else:
                    poiResults[sensor[2]] = entry
    drawPOIS(poiResults)
    return poiResults
def drawPOIS (data):
    global allSensors
    for sensor in allSensors:
        if (sensor in data):
            pygame.draw.circle(DISPLAY, (0,255,0), (data[sensor])[0], 5)

def autoCorrect():
    data = checkSensors()
    if (frontTriggered(data)):
        if (getFrontDist(data) < FSENSOR_LEN * 0.85):
            car.slowDown()
    turn = isTurnComingUp(data)
    if (turn == "STRAIGHT"):
        car.goFaster()
        pass
    else:
        turn = isTurnComingUp(data)
        if (turn == "RIGHT"):
            car.rotateRight()
        elif (turn == "LEFT"):
            car.rotateLeft()
    if (colliding() and getRightDist(data) > getLeftDist(data)):
        car.rotateRight()
    elif (colliding() and getRightDist(data) < getLeftDist(data)):
        car.rotateLeft()
    return data
def isTurnComingUp (data):
    global allSensors
    rightSide = 0
    leftSide = 0
    for sensor in rSensors:
        if sensor in data:
            rightSide += 1
    for sensor in lSensors:
        if sensor in data:
            leftSide += 1
    if (rightSide > leftSide):
        return "RIGHT"
    elif (leftSide > rightSide):
        return "LEFT"
    else:
        return "STRAIGHT"
def colliding ():
    global collisions
    global allBounds
    for bounds in allBounds:
        if (math_car.rectLineIntersect(car.rect.topleft[0], car.rect.topleft[1], car.rect.width, car.rect.height, bounds[0], bounds[1])):
            collisions += 1
            return True
def gatePassed ():
    global inGateZone
    global allGates
    global gatesPassed
    if not inGateZone:
        for gate in allGates:
            curr = pygame.draw.line(DISPLAY, (0, 255, 0), gate[0], gate[1])
            if car.rect.colliderect(curr):
                if (gate[0] == finishLine[0] and gate[1] == finishLine[1]):
                    gatesPassed += 10
                else:
                    gatesPassed += 1
                inGateZone = True
    else:
        exitedGateZone = True
        for gate in allGates:
            curr = pygame.draw.line(DISPLAY, (0, 255, 0), gate[0], gate[1])
            if car.rect.colliderect(curr):
                exitedGateZone = False
        inGateZone = not exitedGateZone
def frontTriggered (data):
    if ("F" in data):
        return True
    return False
def getFrontDist (data):
    if ("F" in data):
        return (data["F"])[1]
    return -1
def getRightDist (data):
    if ("R" in data):
        return (data["R"])[1]
    return -1
def getLeftDist (data):
    if ("L" in data):
        return (data["L"])[1]
    return -1
def getFrontRightDist (data):
    if ("FR" in data):
        return (data["FR"])[1]
    return -1
def getFrontLeftDist (data):
    if ("FL" in data):
        return (data["FL"])[1]
    return -1
def getFrontRightLeftDist (data):
    if ("FRL" in data):
        return (data["FRL"])[1]
    return -1
def getFrontRightRightDist (data):
    if ("FRR" in data):
        return (data["FRR"])[1]
    return -1
def getFrontLeftLeftDist (data):
    if ("FLL" in data):
        return (data["FLL"])[1]
    return -1
def getFrontLeftRightDist (data):
    if ("FLR" in data):
        return (data["FLR"])[1]
    return -1
def getBackRightDist (data):
    if ("BR" in data):
        return (data["BR"])[1]
    return -1
def getBackLeftDist (data):
    if ("BL" in data):
        return (data["BL"])[1]
    return -1
def getBackRightLeftDist (data):
    if ("BRL" in data):
        return (data["BRL"])[1]
    return -1
def getBackLeftRightDist (data):
    if ("BLR" in data):
        return (data["BLR"])[1]
def events():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
while True:
    events()
    all_sprites.update()
    DISPLAY.fill(BLACK)
    all_sprites.draw(DISPLAY)
    drawTrack()
    gatePassed()
    sensors = checkSensors()
    autoCorrect()
    colliding()
    pygame.display.set_caption('Velocity {}'.format(car.vel))
    pygame.display.update()
    fps_clock.tick(FPS)
