
import numpy as np

class Camera:
    #A class to represent a camera at an instant in time
    def __init__(self, width, height, angle, xAFOV, yAFOV):

        #width and height are in pixels
        self.width = width
        self.height = height

        #angle refers to angle between drone level (parallel to ground) and camera
        #all angles in degrees
        self.angle = angle
        self.xAFOV = xAFOV
        self.yAFOV = yAFOV

class Drone:
    #A class to represent a drone at an instant in time
    def __init__(self, altitude, long, lat, heading):
        #altitude in meters
        self.h = altitude

        #GPS coordinates
        self.x = long
        self.y = lat

        #heading in degrees (0 is north, 90 is east, 180 is south, 270 is west)
        self.heading = heading

class CameraDrone(Drone):
    #A class to represent a drone with a camera at an instant in time
    def __init__(self, altitude, long, lat, heading, width, height, angle, xAFOV, yAFOV):
        Drone.__init__(self, altitude, long, lat, heading)
        self.camera = Camera(width, height, angle, xAFOV, yAFOV)


    def getTargetVector(self, targetXPixel, targetYPixel):

        #calculates the Y component of the vector from the drone to the target
        yComponent = self.h * np.tan(self.camera.angle + (self.camera.height / 2 - targetYPixel) * self.camera.yAFOV / self.camera.height)

        #calculates the Y component of the vector from the drone to the centre of the camera frame
        yComponentToCentreFrame = self.h * np.tan(self.camera.angle)

        #calculates the distance from the drone to the centre of the camera frame
        distanceToCentreFrame = np.sqrt(self.h ** 2 + yComponentToCentreFrame ** 2)

        #calculates the X component of the vector from the drone to the target
        xComponent = distanceToCentreFrame * np.tan((targetXPixel - self.camera.width / 2) * self.camera.xAFOV / self.camera.width)

        #returns the components as a vector
        return np.array([[xComponent], [yComponent]])
    
    def globalizeTargetVector(self, targetVector):

        #takes a vector from the drone to the target in the drone's frame of reference and returns
        #a vector from the drone to the target with the y axis aligned with north and the x axis aligned with east

        #create a trasnformation matrix to rotate the vector using the drone's heading
        transformationMatrix = np.array([[np.cos(self.heading), np.sin(self.heading)], [-np.sin(self.heading), np.cos(self.heading)]])
        
        #multiply the vector by the transformation matrix and return value
        return np.matmul(transformationMatrix, targetVector)
    
    def targetCoords(self, globalTargetVector):

        #convert target vector into GPS offsets based on Williams' Aviation Forumlae
        EARTH_RADIUS = 6378137

        #calculate the latitude offset
        latOffset = globalTargetVector[1] / EARTH_RADIUS

        #calculate the longitude offset
        lonOffset = globalTargetVector[0] / (EARTH_RADIUS * np.cos(np.pi * self.x / 180))

        #add offsets to drone's GPS coordinates
        targetLat = self.x + latOffset
        targetLon = self.y + lonOffset

        #return target coordinates as an array in [longitude, latitude] format

        return np.array([targetLon, targetLat])


# sample usage

# create a drone with a camera
drone = CameraDrone(500, -122.7584068, 49.2892931, 300, 1920, 1080, 60, 70, 40)

# get the vector from the drone to a target at pixel
targetVector = drone.getTargetVector(0, 0)

# convert the vector to the drone's frame of reference to a global vector
globalTargetVector = drone.globalizeTargetVector(targetVector)

# convert the global vector to GPS coordinates
targetCoords = drone.targetCoords(globalTargetVector)

# print the GPS coordinates
print(targetCoords)