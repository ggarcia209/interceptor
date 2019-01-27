""" interceptor.py is used to calculate the distance between two vehicles moving in the same direction
 and the time required for the intercepting vehicle to close the distance between the target vehicle.
  In real-life application, distance and speed values would be calculated once every second using live GPS data. """

class Intercept:
    def __init__(self, distance=0, speed1=0, speed2=0):
        self.distance = distance
        self.speed1 = speed1
        self.speed2 = speed2

    def get_time(self):
        """ Calculates time until interception given current distance & speed rates.
         speed rates are converted from Km/h to m/s. Time is calculated by dividing
         current distance by the differences of the rates of speed. """
        self.r1 = float(self.speed1 * 1000 / 3600)
        self.r2 = float(self.speed2 * 1000 / 3600)
        rd = self.r2 - self.r1
        if rd == 0:
            rd = 0.0000000001
        self.time = float(self.distance / rd)
        return self.time

    def get_distance(self):
        """Calculates the total distance currently between both vehicles (gap).
        net_distance == distance gained/lost each second. net_distance is not used in this version. """
        self.net_distance = float(self.distance / self.time)
        if self.time < 0:
            self.time = -1 * self.time
        dt1 = 1 * self.r1
        dt2 = 1 * self.r2
        self.gap = (dt1 - dt2) + self.distance
        return self.gap, self.net_distance


