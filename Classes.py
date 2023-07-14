# import classes
import random
from abc import ABC
import abc
import math# import classes
import random
from abc import ABC
import abc
import math


# abstract class - cannot instantiate character objects
class Character(ABC):
    def __init__(self, health, location, int_name):
        self.health = health
        self.location = location
        self.name = int_name
        self.eyesight = 15

    # define getter and setter methods

    def getHealth(self):
        return self.health

    def getLocation(self):
        return self.location

    def setHealth(self, health):
        self.health = health

    def setLocation(self, location_x, location_y):
        self.location = [location_x, location_y]

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    @abc.abstractmethod
    def move(self):
        pass


class Susceptible(Character):

    # susceptible class constructor
    def __init__(self, int_name):
        self.health = random.randint(80, 100)
        # all susceptibles that are created from the constructor
        # will be located at the base camp which is located from (1,1) to (25,25)
        location_x = random.randint(1, 25)
        location_y = random.randint(1, 25)
        self.location = [location_x, location_y]
        self.name = f"Susceptible_{int_name}"
        self.infected = False
        self.immunity_rate = 0
        self.have_been_cured = False

    # this is the find cure method which determines if the cure is found during the simulation

    def find_cure(self, B, C):
        if (6 + B) * (C - 3) == 54:
            return True
        else:
            return False

    # checks the distance between the susceptible and the Object
    def collocated(self, Object):
        x = (self.location[0] - Object.location[0]) ** 2
        y = (self.location[1] - Object.location[1]) ** 2
        distance_away = math.sqrt(x + y)
        if distance_away <= Object.eyesight:
            return True

    # update the susceptible immunity rate by 25%
    def get_boosted(self):
        self.immunity_rate += 25
        if self.immunity_rate >= 75:
            self.immunity_rate = 100

    def get_infection(self):
        if not self.have_been_cured:
            return True
        if self.have_been_cured:
            random_num = random.randint(1, 100)
            if random_num <= self.immunity_rate:
                return False
            else:
                return True

    # Generate random movement within a range of -2 to 2 in both X and Y directions
    def move(self):
        runx = random.randint(-2, 2)
        self.location[0] += runx
        run_y = random.randint(-2, 2)
        self.location[1] += run_y

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 15
        elif self.location[1] >= 100:
            self.location[1] -= 15
        elif self.location[0] <= 0:
            self.location[0] += 15
        elif self.location[1] <= 0:
            self.location[1] += 15

    # the explore method
    def explore(self):
        self.move()

    # run method returns if the susceptible escaped or not based on how far they ran away
    def run(self):
        run_x = random.randint(1, 4)
        self.location[0] += run_x
        run_y = random.randint(1, 4)
        self.location[1] += run_y
        running_distance = math.sqrt((run_x + run_y) ** 2)
        if running_distance < 5:
            return False
        else:
            return True

    def fight(self, zombie):
        if isinstance(zombie, RegularZombie):
            choice = random.randint(1, zombie.health)
            num = zombie.health - self.health

            # return true means human win fight

            if self.immunity_rate == 100:
                return True
            if num <= 0:
                return True
            else:
                if choice <= num:
                    return False
                else:
                    self.health -= 5
                    return True
        elif isinstance(zombie, SuperZombie):
            choice = random.randint(1, zombie.health)
            num = zombie.health - self.health

            if self.immunity_rate == 100:
                return True
            if num <= 0:
                return True
            else:
                if choice <= num:
                    return False
                else:
                    self.health -= 5
                    return True
        else:
            return False


class RegularZombie(Character):

    def __init__(self, int_name, location_x=None, location_y=None):
        self.health = random.randint(100, 120)
        if location_x is None:
            location_x = random.randint(1, 100)
        if location_y is None:
            location_y = random.randint(1, 100)
        self.location = [location_x, location_y]
        # eyesight is how far they can detect humans
        self.eyesight = 3
        self.name = f"RegularZombie_{int_name}"

    # Generate random movement within a range of 1 to 4 in both X and Y directions
    def move(self):
        # can use self.location[0] += random.randint(1,4)
        runx = random.randint(1, 4)
        self.location[0] += runx
        run_y = random.randint(1, 4)
        self.location[1] += run_y

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 20
        elif self.location[1] >= 100:
            self.location[1] -= 20
        elif self.location[0] <= 0:
            self.location[0] += 20
        elif self.location[1] <= 0:
            self.location[1] += 20


class SuperZombie(RegularZombie):

    def __init__(self, int_name, location_x=None, location_y=None):
        super().__init__(int_name)
        self.health = random.randint(120, 140)
        self.eyesight = 6
        if location_x is None:
            location_x = random.randint(1, 100)
        if location_y is None:
            location_y = random.randint(1, 100)
        self.location = [location_x, location_y]
        self.name = f"SuperZombie_{int_name}"

    def move(self):

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 30
        elif self.location[1] >= 100:
            self.location[1] -= 30
        elif self.location[0] <= 0:
            self.location[0] += 30
        elif self.location[1] <= 0:
            self.location[1] += 30


class Recovered(Susceptible):
    def __init__(self, int_name, X, Y):
        super().__init__(int_name)
        self.immunity_rate = 100
        self.name = f"Recovered_{int_name}"
        self.location[0] = X
        self.location[1] = Y
        self.location = [X, Y]
        self.eyesight = 15

    # override the collocated method from the susceptible class
    def FindZombie(self, Object):
        x = (self.location[0] - Object.location[0]) ** 2
        y = (self.location[1] - Object.location[1]) ** 2
        distance_away = math.sqrt(x + y)
        if distance_away <= self.eyesight:
            return True



# abstract class - cannot instantiate character objects
class Character(ABC):
    def __init__(self, health, location, int_name):
        self.health = health
        self.location = location
        self.name = int_name
        self.eyesight = 15

    # define getter and setter methods

    def getHealth(self):
        return self.health

    def getLocation(self):
        return self.location

    def setHealth(self, health):
        self.health = health

    def setLocation(self, location_x, location_y):
        self.location = [location_x, location_y]

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    @abc.abstractmethod
    def move(self):
        pass


class Susceptible(Character):

    # susceptible class constructor
    def __init__(self, int_name):
        self.health = random.randint(80, 100)
        # all susceptibles that are created from the constructor
        # will be located at the base camp which is located from (1,1) to (25,25)
        location_x = random.randint(1, 25)
        location_y = random.randint(1, 25)
        self.location = [location_x, location_y]
        self.name = f"Susceptible_{int_name}"
        self.infected = False
        self.immunity_rate = 0
        self.have_been_cured = False

    # this is the find cure method which determines if the cure is found during the simulation

    def find_cure(self, B, C):
        if (6 + B) * (C - 3) == 54:
            return True
        else:
            return False

    # checks the distance between the susceptible and the Object
    def collocated(self, Object):
        x = (self.location[0] - Object.location[0]) ** 2
        y = (self.location[1] - Object.location[1]) ** 2
        distance_away = math.sqrt(x + y)
        if distance_away <= Object.eyesight:
            return True

    # update the susceptible immunity rate by 25%
    def get_boosted(self):
        self.immunity_rate += 25
        if self.immunity_rate >= 75:
            self.immunity_rate = 100

    def get_infection(self):
        if not self.have_been_cured:
            return True
        if self.have_been_cured:
            random_num = random.randint(1, 100)
            if random_num <= self.immunity_rate:
                return False
            else:
                return True

    # Generate random movement within a range of -2 to 2 in both X and Y directions
    def move(self):
        runx = random.randint(-2, 2)
        self.location[0] += runx
        run_y = random.randint(-2, 2)
        self.location[1] += run_y

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 15
        elif self.location[1] >= 100:
            self.location[1] -= 15
        elif self.location[0] <= 0:
            self.location[0] += 15
        elif self.location[1] <= 0:
            self.location[1] += 15

    # the explore method
    def explore(self):
        self.move()

    # run method returns if the susceptible escaped or not based on how far they ran away
    def run(self):
        run_x = random.randint(1, 4)
        self.location[0] += run_x
        run_y = random.randint(1, 4)
        self.location[1] += run_y
        running_distance = math.sqrt((run_x + run_y) ** 2)
        if running_distance < 5:
            return False
        else:
            return True

    def fight(self, zombie):
        if isinstance(zombie, RegularZombie):
            choice = random.randint(1, zombie.health)
            num = zombie.health - self.health

            # return true means human win fight

            if self.immunity_rate == 100:
                return True
            if num <= 0:
                return True
            else:
                if choice <= num:
                    return False
                else:
                    self.health -= 5
                    return True
        elif isinstance(zombie, SuperZombie):
            choice = random.randint(1, zombie.health)
            num = zombie.health - self.health

            if self.immunity_rate == 100:
                return True
            if num <= 0:
                return True
            else:
                if choice <= num:
                    return False
                else:
                    self.health -= 5
                    return True
        else:
            return False


class RegularZombie(Character):

    def __init__(self, int_name, location_x=None, location_y=None):
        self.health = random.randint(100, 120)
        if location_x is None:
            location_x = random.randint(1, 100)
        if location_y is None:
            location_y = random.randint(1, 100)
        self.location = [location_x, location_y]
        # eyesight is how far they can detect humans
        self.eyesight = 3
        self.name = f"RegularZombie_{int_name}"

    # Generate random movement within a range of 1 to 4 in both X and Y directions
    def move(self):
        # can use self.location[0] += random.randint(1,4)
        runx = random.randint(1, 4)
        self.location[0] += runx
        run_y = random.randint(1, 4)
        self.location[1] += run_y

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 20
        elif self.location[1] >= 100:
            self.location[1] -= 20
        elif self.location[0] <= 0:
            self.location[0] += 20
        elif self.location[1] <= 0:
            self.location[1] += 20


class SuperZombie(RegularZombie):

    def __init__(self, int_name, location_x=None, location_y=None):
        super().__init__(int_name)
        self.health = random.randint(120, 140)
        self.eyesight = 6
        if location_x is None:
            location_x = random.randint(1, 100)
        if location_y is None:
            location_y = random.randint(1, 100)
        self.location = [location_x, location_y]
        self.name = f"SuperZombie_{int_name}"

    def move(self):

        # If the new location is outside the bounds of the 100x100 island,
        # The character is going outside the island for resources and will be back again

        if self.location[0] >= 100:
            self.location[0] -= 30
        elif self.location[1] >= 100:
            self.location[1] -= 30
        elif self.location[0] <= 0:
            self.location[0] += 30
        elif self.location[1] <= 0:
            self.location[1] += 30


class Recovered(Susceptible):
    def __init__(self, int_name, X, Y):
        super().__init__(int_name)
        self.immunity_rate = 100
        self.name = f"Recovered_{int_name}"
        self.location[0] = X
        self.location[1] = Y
        self.location = [X, Y]
        self.eyesight = 15

    # override the collocated method from the susceptible class
    def FindZombie(self, Object):
        x = (self.location[0] - Object.location[0]) ** 2
        y = (self.location[1] - Object.location[1]) ** 2
        distance_away = math.sqrt(x + y)
        if distance_away <= self.eyesight:
            return True

