""" test_values.py creates user-defined n amount of values to be passed into each instance of the Intercept class in interceptor.py
Each value represents the value for each variable at every second passed in the simulation. In real life application,
speed and distance values would be calculated by live GPS data once every second. """

import random


class TestValues:
    def __init__(self):
        self.values = {"d_value": [], "s1_value": [], "s2_value": [], "Vi1": [], "Vf1": [], "Vi2": [], "Vf2": [],
                       "second": [0], "a1": [0], "a2": [0], "dt1": [0], "dt2": [0], "tdt1": [0], "tdt2": [0]}

    def get_input(self):
        """ User inputs values for starting distance,
        the min/max speed range (km/h) of both target and interceptor vehicles,
        and number of seconds (n) simulation will run for. """

        print("""
Distance measured in Km / Speed measured in Km/H""")
        print("-" * 15)
        while True:
            try:
                self.initial_distance = float(input("Initial Distance:  ")) * 1000  # converted from km to meters
                self.values["d_value"].append(self.initial_distance)
                self.count = int(input("# of Simulations (1/sec):  "))
                self.s1_lo = float(input("Target Speed Range - Lower Bound:  "))
                self.s1_hi = float(input("Target Speed Range - Upper Bound:  "))
                if self.s1_lo > self.s1_hi:
                    raise ValueError("")
                self.s2_lo = float(input("Interceptor Speed Range - Lower Bound:  "))
                self.s2_hi = float(input("Inteceptor Speed Range - Upper Bound:  "))
                if self.s2_lo > self.s2_hi:
                    raise ValueError("")
                break
            except ValueError:
                print("Invalid Entry!!")
        return self.values

    def generate_values(self):
        """ Starting speed values = random choice between speed ranges """

        if self.s1_hi - self.s1_lo == 0:
            self.values["s1_value"].append(self.s1_lo)
        else:
            self.values["s1_value"].append(random.randrange(self.s1_lo, self.s1_hi, 1))
        if self.s2_hi - self.s2_lo == 0:
            self.values["s2_value"].append(self.s2_lo)
        else:
            self.values["s2_value"].append(random.randrange(self.s2_lo, self.s2_hi, 1))
        return self.values

    def s1_speed_values(self, speed_range=3):  # measured in Km/Hour
        """ Subsequent speed values are calculated by first randomly determining if the vehicle will
        accelerate, decelerate, or remain at constant speed. If accelerating or decelerating,
        next value will be within speed range defined in get_input()
         and not greater/less than the current value +- the absolute value of speed_range parameter.
          ie: vehicle will not acel/decel faster than speed_range km/h in one second. """
        if self.s1_hi == self.s1_lo:
            speed_range = 0
        select_first = self.values["s1_value"][0]
        for _ in range(self.count):
            choice = random.randint(-1, 1)
            select_next = select_first + (choice * speed_range)
            if select_next < select_first:
                new = random.randint(select_next, select_first)
            elif select_next == select_first:
                new = select_first
            else:
                new = random.randint(select_first, select_next)
            if new < self.s1_lo:
                new = new + speed_range
            elif new > self.s1_hi:
                new = new - speed_range
            select_first = new
            self.values["s1_value"].append(new)
        return self.values["s1_value"]

    def s2_speed_values(self, speed_range_2=3):  # measured in Km/Hour
        """ Calculates speed values for interceptor vehicle in Km/h. """
        if self.s2_hi == self.s2_lo:
            speed_range_2 = 0
        select_first_2 = self.values["s2_value"][0]
        for _ in range(self.count):
            choice = random.randint(-1, 1)
            select_next_2 = select_first_2 + (choice * speed_range_2)
            if select_next_2 < select_first_2:
                new = random.randint(select_next_2, select_first_2)
            elif select_next_2 == select_first_2:
                new = select_first_2
            else:
                new = random.randint(select_first_2, select_next_2)
            if new < self.s2_lo:
                new = new + speed_range_2
            elif new > self.s2_hi:
                new = new - speed_range_2
            select_first_2 = new
            self.values["s2_value"].append(new)
        return self.values["s2_value"]

    def acceleration_values(self):  # measured in meters/second
        """ Calculates the initial & final velocities in m/s of both vehicles after each second. """
        item_count = 0
        sec = 0
        for i in range(len(self.values["s1_value"]) - 1):
            Vi_1 = float((self.values["s1_value"][i] * 1000) / 3600)  # Vi - Initial Velocity
            self.values["Vi1"].append(Vi_1)
            Vf_1 = float((self.values["s1_value"][i + 1] * 1000) / 3600)  # Vf - Final Velocity
            self.values["Vf1"].append(Vf_1)
            Vi_2 = float((self.values["s2_value"][i] * 1000) / 3600)
            self.values["Vi2"].append(Vi_2)
            Vf_2 = float((self.values["s2_value"][i + 1] * 1000) / 3600)
            self.values["Vf2"].append(Vf_2)
            sec += 1
            self.values["second"].append(sec)
            item_count += 1
        return self.values

    def calc_a_vals(self):  # meters/second
        """ Acceleration values are calculated using initial/final velocities
        to account for differences in rate of speed between each second"""
        for i in range(len(self.values["Vi1"])):
            a1 = float((self.values["Vf1"][i] - self.values["Vi1"][i]) / 1)
            a2 = float((self.values["Vf2"][i] - self.values["Vi2"][i]) / 1)
            self.values["a1"].append(a1)
            self.values["a2"].append(a2)
        return self.values

    def calc_d_gap(self):  # meters / dt = 'distance traveled', tdt = 'total dt'
        """ The distance gap between both vehicles is calculated by totaling the distance traveled
        by both vehicles in each second, then subtracting the total distance traveled by the interceptor
        from the sum of the total distance traveled by the target and the initial distance. """
        time_interval = 1
        for i in range(len(self.values["second"]) - 1):
            dt1 = (self.values["Vi1"][i] * time_interval) + (self.values["a1"][i])  # dt = distance traveled/second
            dt2 = (self.values["Vi2"][i] * time_interval) + (self.values["a2"][i])
            self.values["dt1"].append(dt1)
            self.values["dt2"].append(dt2)
        for i in range(len(self.values["dt1"]) - 1):
            tdt1 = sum(self.values["dt1"][0:i + 1])
            tdt2 = sum(self.values["dt2"][0:i + 1])
            self.values["tdt1"].append(tdt1)
            self.values["tdt2"].append(tdt2)
        for i in range(len(self.values["tdt1"])):
            d_gap = (self.values["tdt1"][i] + self.initial_distance) - self.values["tdt2"][i]
            self.values["d_value"].append(d_gap)
        return self.values

    def clear_used_values(self):
        """ Clears all values used to calculate the final values being passed to Intercept instances. """
        del (self.values["Vi1"], self.values["Vf1"], self.values["Vi2"], self.values["Vf2"],
             self.values["a1"], self.values["a2"], self.values["dt1"], self.values["dt2"],
             self.values["tdt1"], self.values["tdt2"])
        return self.values

    def convert_km(self, raw_values):  # convert to km rounded to 2 decimals
        """ Converts meters to kilometers - practical application of this function may
        require further refactoring and/or design changes """
        converts = []
        for item in raw_values:
            converts.append(round((item / 1000), 2))
        return converts

    def create_test(self):
        """ Functions above are ran as one command for simplicity and ease of use. """
        self.get_input()
        self.generate_values()
        self.s1_speed_values()
        self.s2_speed_values()
        self.acceleration_values()
        self.calc_a_vals()
        self.calc_d_gap()
        self.clear_used_values()


