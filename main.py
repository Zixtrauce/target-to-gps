
import numpy as np

class Camera:
    #A class to represent a camera at an instant in time
    def __init__(self, width, height, angle, xAFOV, yAFOV):

        #width and height are in pixels
        self.w = width
        self.h = height

        #angle refers to angle between drone level (parallel to ground) and camera
        #all angles in degrees
        self.theta = angle
        self.xAFOV = xAFOV
        self.yAFOV = yAFOV

class Drone:
    #A class to represent a drone at an instant in time
    def __init__(self, altitude, xcoord, ycoord, heading):
        #altitude in meters
        self.h = altitude

        #GPS coordinates
        self.x = xcoord
        self.y = ycoord

        #heading in degrees (0 is north, 90 is east, 180 is south, 270 is west)
        self.heading = heading

class CameraDrone(Drone):
    #A class to represent a drone with a camera at an instant in time
    def __init__(self, altitude, xcoord, ycoord, heading, width, height, angle, xAFOV, yAFOV):
        Drone.__init__(self, altitude, xcoord, ycoord, heading)
        self.camera = Camera(width, height, angle, xAFOV, yAFOV)

        def getTargetVector(self, targetXPixel, targetYPixel):

            #calculates the Y component of the vector from the drone to the target
            yComponent = self.h * np.tan(self.angle + (self.height / 2 - targetYPixel) * self.yAFOV / self.height)

            #calculates the Y component of the vector from the drone to the centre of the camera frame
            yComponentToCentreFrame = self.h * np.tan(self.angle)

            #calculates the distance from the drone to the centre of the camera frame
            distanceToCentreFrame = np.sqrt(self.h ** 2 + yComponentToCentreFrame ** 2)

            #calculates the X component of the vector from the drone to the target
            xComponent = distanceToCentreFrame * np.tan((targetXPixel - self.width / 2) * self.xAFOV / self.width)

            #returns the components as a vector
            return np.array([xComponent], [yComponent])
        
        def globalizeTargetVector(self, targetVector):

            #takes a vector from the drone to the target in the drone's frame of reference and returns
            #a vector from the drone to the target with the y axis aligned with north and the x axis aligned with east

            #create a trasnformation matrix to rotate the vector using the drone's heading
            transformationMatrix = np.array([np.cos(self.heading), np.sin(self.heading)], [-np.sin(self.heading), np.cos(self.heading)])
            
            #multiply the vector by the transformation matrix and return value
            return np.matmul(transformationMatrix, targetVector)
        


        


