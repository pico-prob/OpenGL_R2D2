from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from objloader import *
import sys
import pygame

class Game(object):
    def __init__(self, xWidth, yWidth):
        self.xWidth = xWidth+1
        self.yWidth = yWidth+1
        self.objects = []
        self.models = {}
        self.textures = {}
        self.field_size = 1.0
        self.zAngle = 0
        self.yAngle = 0
        self.light = [1.6, -1.3, 2, 0] # light position
        self.player = None
        self.finish = False
        self.keyPressPossible = True

    # Called when a key is pressed
    def key_pressed(self, key, x, y):
        if self.keyPressPossible:
            if key == "w":
                self.player.move("up")
            elif key == "a":
                self.player.move("left")
            elif key == "s":
                self.player.move("down")
            elif key == "d":
                self.player.move("right")
            elif key == "q":
                sys.exit()
            elif key == "g":
                self.zAngle+=10
            elif key == "h":
                self.yAngle+=10
        glutPostRedisplay()

    def special_keys_pressed(self, key, x, y):
        if self.keyPressPossible:
            if key == GLUT_KEY_LEFT:
                self.player.move("left")
            elif key == GLUT_KEY_RIGHT:
                self.player.move("right")
            elif key == GLUT_KEY_UP:
                self.player.move("up")
            elif key == GLUT_KEY_DOWN:
                self.player.move("down")
        glutPostRedisplay()

    # Called to updated rendering
    def display(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -30)
        glRotatef(-110+self.zAngle, 1, 0, 0)
        glRotatef(0+self.yAngle, 0, 1, 0)

        self.addWalls()
        self.drawFloor()
        self.drawObjects()

        if self.finish and self.keyPressPossible:
            # TODO: won-animation
            print "Gewonnen!"
            glutLeaveMainLoop()

        glFlush()
        glutSwapBuffers()
        glutPostRedisplay()

    def addWalls(self):
        for i in range(0,self.xWidth+1):
            try:
                self.addObject(Wall(i,0,self))
            except:
                pass
            try:
                self.addObject(Wall(i,self.yWidth,self))
            except:
                pass
        for i in range(1,self.yWidth):
            try:
                self.addObject(Wall(0,i,self))
            except:
                pass
            try:
                self.addObject(Wall(self.xWidth,i,self))
            except:
                pass

    def drawObjects(self):
        for obj in self.objects:
            obj.draw()

    # Called when the window is created or resized
    def reshape(self, width, height):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(20, width/height, 10, 100)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_MODELVIEW)
        glutPostRedisplay()

    def drawFloor(self):
        x1 = -(self.xWidth/2*self.field_size+self.field_size/2)
        x2 = self.xWidth/2*self.field_size+self.field_size/2
        z1 = -(self.yWidth/2*self.field_size+self.field_size/2)
        z2 = self.yWidth/2*self.field_size+self.field_size/2
        glBindTexture(GL_TEXTURE_2D, self.textures['floor'])
        glNormal3f(0.0, -1.0, 0.0)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(x1, 1, z1)
        glTexCoord2f(0.0, 4.0)
        glVertex3f(x2, 1, z1)
        glTexCoord2f(4.0, 4.0)
        glVertex3f(x2, 1, z2)
        glTexCoord2f(4.0, 0.0)
        glVertex3f(x1, 1, z2)
        glEnd()

    def addObject(self, object):
        if not self.getObject(object.xPos, object.yPos):
            self.objects.append(object)
        else:
            raise Exception("Position (%i,%i) is already taken." % (object.xPos, object.yPos))

    def getObject(self, xPos, yPos):
        for object in self.objects:
            if object.xPos == xPos and object.yPos == yPos:
                return object
        return None

    def positionOnBoard(self, xPos, yPos):
        if ((xPos > 0 and xPos < self.xWidth)
            and (yPos > 0 and yPos < self.yWidth)):
            return True
        return False

    def start(self):
        # Glut Initialization
        argv = glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB|GLUT_DOUBLE|GLUT_DEPTH)
        glutInitWindowSize(600,500)
        glutCreateWindow("Crates")

        glClearColor(0, 0, 0, 0);
        glEnable(GL_DEPTH_TEST);

        # Textures
        glEnable(GL_TEXTURE_2D)
        self.textures['floor'] = self.loadTexture("floor.png")
        self.textures['crate'] = self.loadTexture("crate.png")
        self.textures['toolbox'] = self.loadTexture("toolbox.png")
        self.textures['wall'] = self.loadTexture("wall.png")

        # Light
        LightPosition = (self.light[0], self.light[1], self.light[2], self.light[3])
        LightAmbient = (0.5, 0.5, 0.5, 0.0)
        LightDiffuse = (0.6, 0.6, 0.6, 1.0)
        LightSpecular = (0.5, 0.5, 0.5, 1.0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, LightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, LightPosition)
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_SHININESS, 1.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.35, 0.35, 0.35, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.35, 0.35, 0.35, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.4, 0.4, 0.0])
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)

        # Models
        self.models['r2d2'] = OBJ("R2D2.obj", swapyz=True).gl_list

        # Glut-Functions
        #glutFullScreen()
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.key_pressed)
        glutSpecialFunc(self.special_keys_pressed)
        glutMainLoop()

    def loadTexture(self, file):
        textureSurface = pygame.image.load(file)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        return texture


class GameObject(object):
    def __init__(self, xPos, yPos, game):
        self.xPos = xPos    # position on board
        self.yPos = yPos
        self.game = game
        self.xOffset = 0.0  # offset of *PosGL while animating
        self.yOffset = 0.0
        self.xDir = 0       # direction of current move
        self.yDir = 0
        self.xDirLast = 0   # direction of last move
        self.yDirLast = -1
        self.yAngle = 0     # current angle
        self.turnAngle = 0  # angle needed for turn from *dirLast to *dir

    # Position in 3d-World:
    @property
    def xPosGL(self):
        return 0 - self.game.xWidth/2.0 + self.xPos + self.xOffset
    @property
    def yPosGL(self):
        return 0 - self.game.yWidth/2.0 + self.yPos + self.yOffset

    def draw(self):
        glPushMatrix()
        glTranslatef(self.xPosGL,0.5,self.yPosGL)
        glScalef(0.5, 0.5, 0.5)
        glBindTexture(GL_TEXTURE_2D, self.game.textures['crate'])
        self.makeCrate()
        glPopMatrix()

    # TODO: store in glList
    def makeCrate(self):
        glBegin(GL_QUADS)
        # Top
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1, -1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1, -1, -1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, -1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1, -1, 1)
        # Back
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1, -1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1, -1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1, 1, 1)
        # Front
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1, -1, -1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1, 1, -1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, 1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1, -1, -1)
        # Left
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1, -1, -1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1, -1, 1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1, 1, 1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-1, 1, -1)
        # Right
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1, -1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1, -1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(1, 1, -1)
        # Bottom
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-1, 1, -1)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1, 1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1, 1, -1)
        glEnd()

    def __repr__(self):
        return str((self.xPos, self.yPos))

class MovableObject(GameObject):
    def movePossible(self, xPos, yPos):
        if not self.game.getObject(xPos, yPos)  and self.game.positionOnBoard(xPos, yPos):
            return True
        return False

    def move(self, direction):
        directions = ["up", "right", "down", "left"]
        if direction not in directions:
            raise Exception("Direction not in: %s" % ", ".join(directions))
        else:
            self.xDir = 0
            self.yDir = 0
            if direction == "up":
                self.yDir = 1
            elif direction == "right":
                self.xDir = 1
            elif direction == "down":
                self.yDir = -1
            elif direction == "left":
                self.xDir = -1
        newX = self.xPos+self.xDir
        newY = self.yPos+self.yDir
        pushing = False
        blockingObject = self.game.getObject(newX, newY)
        if blockingObject: # is there an object in the way?
            try: # push another object (if allowed)
                pushing = self.pushObject(blockingObject, direction)
            except (AttributeError):
                pass
        if self.movePossible(newX, newY) or pushing:
            self.turnAngle = self.getTurnAngle()
            self.game.keyPressPossible = False
            self.animateMove()
            return True
        else:
            return False

    def animateMove(self,step=0):
        steps = 5
        step += 1
        if steps >= step:
            self.yAngle += (self.turnAngle/steps)
            if self.yAngle > 360:
                self.yAngle -= 360
        else:
            distance = self.game.field_size/steps
            self.xOffset += distance*self.xDir
            self.yOffset += distance*self.yDir
        if steps*2 >= step:
            glutTimerFunc(20,self.animateMove,step)
        else:
            self.xPos = self.xPos+self.xDir
            self.yPos = self.yPos+self.yDir
            self.xOffset = 0.0
            self.yOffset = 0.0
            self.xDirLast = self.xDir
            self.yDirLast = self.yDir
            self.turnAngle = 0
            self.game.keyPressPossible = True

    # Calculate needed angle for turn from previous to current direction
    def getTurnAngle(self):
        angle = 0
        if self.xDirLast == 1 and self.yDir == 1:
            angle = -90
        elif self.xDirLast == 1 and self.yDir == -1:
            angle = 90
        elif self.xDirLast == 1 and self.xDir == -1:
            angle = 180
        elif self.yDirLast == 1 and self.xDir == 1:
            angle = 90
        elif self.yDirLast == 1 and self.xDir == -1:
            angle = -90
        elif self.yDirLast == 1 and self.yDir == -1:
            angle = 180
        elif self.xDirLast == -1 and self.xDir == 1:
            angle = 180
        elif self.xDirLast == -1 and self.yDir == 1:
            angle = 90
        elif self.xDirLast == -1 and self.yDir == -1:
            angle = -90
        elif self.yDirLast == -1 and self.xDir == 1:
            angle = -90
        elif self.yDirLast == -1 and self.xDir == -1:
            angle = 90
        elif self.yDirLast == -1 and self.yDir == 1:
            angle = 180
        return angle

class Player(MovableObject):
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xPosGL,0.67,self.yPosGL)
        glRotatef(self.yAngle,0,1,0)
        glRotatef(90,1,0,0)
        glScalef(0.05, 0.05, 0.05)
        glCallList(self.game.models['r2d2'])
        glPopMatrix()

    def pushObject(self, object, direction):
        return object.move(direction)

class Box(MovableObject):
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xPosGL,0.5,self.yPosGL)
        glScalef(0.5, 0.5, 0.5)
        glBindTexture(GL_TEXTURE_2D, self.game.textures['crate'])
        self.makeCrate()
        glPopMatrix()

class StaticObject(GameObject):
    pass

class Wall(StaticObject):
    def draw(self):
        glPushMatrix()
        glTranslatef(self.xPosGL,0.5,self.yPosGL)
        glScalef(0.5, 0.5, 0.5)
        glBindTexture(GL_TEXTURE_2D, self.game.textures['wall'])
        self.makeCrate()
        glPopMatrix()

class Gate(StaticObject):
    def draw(self):
        pass

class HeavyBox(StaticObject):
    pass

class BananaBox(Box):
    def movePossible(self, xPos, yPos):
        if ((not self.game.getObject(xPos, yPos) and self.game.positionOnBoard(xPos, yPos)) or isinstance(self.game.getObject(xPos, yPos), Gate)):
            if isinstance(self.game.getObject(xPos, yPos), Gate):
                self.game.finish = True
            return True
        return False

    def draw(self):
        glPushMatrix()
        glTranslatef(self.xPosGL,0.5,self.yPosGL)
        glScalef(0.5, 0.5, 0.5)
        glBindTexture(GL_TEXTURE_2D, self.game.textures['toolbox'])
        self.makeCrate()
        glPopMatrix()

def main():
    game = Game(7,7)
    player = Player(3,4, game)
    game.addObject(player)
    game.player = player
    game.addObject(Box(1,2,game))
    game.addObject(Box(1,7,game))
    game.addObject(Box(2,6,game))
    game.addObject(Box(3,6,game))
    game.addObject(Box(4,5,game))
    game.addObject(Box(5,4,game))
    game.addObject(Box(2,4,game))
    game.addObject(Box(6,1,game))
    game.addObject(Box(6,2,game))
    game.addObject(Box(6,4,game))
    game.addObject(Box(7,5,game))
    game.addObject(BananaBox(4,2,game))
    game.addObject(Box(3,2,game))
    game.addObject(Box(2,1,game))
    game.addObject(Gate(2,0,game))
    game.start()

if __name__ == '__main__':
    main()
