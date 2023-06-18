
import numpy as np

class Camera:
    #A class to represent a camera at an instant in time
    def __init__(self, width, height, angle, xAFOV, yAFOV):
        self.w = width
        self.h = height
        self.theta = angle
        self.xAFOV = xAFOV
        self.yAFOV = yAFOV

class Drone:
    #A class to represent a drone at an instant in time
    def __init__(self, altitude, xcoord, ycoord, heading):
        self.h = altitude
        self.x = xcoord
        self.y = ycoord
        self.heading = heading

class CameraDrone(Drone):
    #A class to represent a drone with a camera at an instant in time
    def __init__(self, altitude, xcoord, ycoord, heading, width, height, angle, xAFOV, yAFOV):
        Drone.__init__(self, altitude, xcoord, ycoord, heading)
        self.camera = Camera(width, height, angle, xAFOV, yAFOV)

        def getTargetVector(self, targetXPixel, targetYPixel):

            yComponent = self.h * np.tan(self.angle + (self.height / 2 - targetYPixel) * self.yAFOV / self.height)
            yComponentToCentreFrame = self.h * np.tan(self.angle)
            distanceToCentreFrame = np.sqrt(self.h ** 2 + yComponentToCentreFrame ** 2)
            xComponent = distanceToCentreFrame * np.tan((targetXPixel - self.width / 2) * self.xAFOV / self.width)
            return np.array([xComponent, yComponent])


