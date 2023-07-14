# import classes
import random
import matplotlib.pyplot as plt

import Classes

# arrays to hold objects of susceptibles, regular zombies, and super zombies
susceptibles = []
regularZombies = []
superZombies = []
recovered = []

# number of susceptibles, regular zombies, and super zombies at the beginning of simulation
susceptible_count = 80
regularZombie_count = 15
superZombie_count = 5
recovered_count = 0
human_count = susceptible_count + recovered_count
count = 0
have_cure = False

# plotting
regularzombiecount = []
regularzombiecount.append(regularZombie_count)
superzombiecount = []
superzombiecount.append(superZombie_count)
susceptiblecount = []
susceptiblecount.append(susceptible_count)
recoveredcount = []
recoveredcount.append(recovered_count)

# create objects of susceptibles
for susceptible in range(susceptible_count):
    susceptible = Classes.Susceptible(susceptible + 1)
    susceptibles.append(susceptible)
# create objects of regular zombies
for regularZombie in range(regularZombie_count):
    regularZombie = Classes.RegularZombie(regularZombie + 1)
    regularZombies.append(regularZombie)
# create objects of super zombies
for superZombie in range(superZombie_count):
    superZombie = Classes.SuperZombie(superZombie + 1)
    superZombies.append(superZombie)

keep_going = True
is_rescued = False

# zombie simulation loop
while keep_going and not is_rescued and human_count < 100:
    # During each hour of the simulation, someone will dial a number
    # if the number is 911 then the simulation will end with susceptibles being rescued by 911
    rescue_num = random.randint(1, 2000)
    if rescue_num == 911:
        is_rescued = True
        if count == 1:
            print(f"On the 1st hour of the simulation:")
        elif count == 2:
            print(f"On the 2nd hour of the simulation:")
        elif count == 3:
            print(f"On the 3nd hour of the simulation:")
        else:
            print(f"On the {count}th hour of the simulation:")
        print("Simulation Over!")
        print("Everyone have been successfully rescued!")

    if have_cure and recovered_count > 0:
        for recov in recovered:
            recov.move()
            for regularZombie in regularZombies:
                # checks to see if a zombie is close to the susceptible
                if recov.FindZombie(regularZombie):
                    if regularZombie in regularZombies:
                        x = regularZombie.location[0]
                        y = regularZombie.location[1]
                        regularZombies.remove(regularZombie)
                        regularZombie_count -= 1
                        recovered_count += 1
                        human_count += 1
                        new_recovered = Classes.Recovered(recovered_count, x, y)
                        recovered.append(new_recovered)
        for recov in recovered:
            recov.move()
            for superZombie in superZombies:
                # checks to see if a zombie is close to the susceptible
                if recov.FindZombie(superZombie):
                    if superZombie in superZombies:
                        x = superZombie.location[0]
                        y = superZombie.location[1]
                        superZombies.remove(superZombie)
                        superZombie_count -= 1
                        recovered_count += 1
                        human_count += 1
                        new_recovered = Classes.Recovered(recovered_count, x, y)
                        recovered.append(new_recovered)

    for susceptible in susceptibles:
        susceptible.explore()
        # this loop checks distance between regular zombies and susceptibles
        for regularZombie in regularZombies:
            # checks to see if a zombie is close to the susceptible
            if susceptible.collocated(regularZombie):
                escaped = susceptible.run()
                if not escaped:
                    # if susceptible did not run far enough, they will have to fight that zombie
                    won = susceptible.fight(regularZombie)
                    if not won:
                        B = random.randint(1, 12)
                        C = random.randint(5, 15)
                        cure_found = susceptible.find_cure(B, C)
                        if cure_found:
                            have_cure = True
                        infected = susceptible.get_infection()
                        if susceptible in susceptibles and infected:
                            x = susceptible.location[0]
                            y = susceptible.location[1]
                            susceptibles.remove(susceptible)
                            susceptible_count -= 1
                            human_count -= 1
                            regularZombie_count += 1
                            new_regularZombie = Classes.RegularZombie(regularZombie_count, x, y)
                            regularZombies.append(new_regularZombie)
                    if won:
                        if have_cure and (susceptible.location[0] < 25 and susceptible.location[1] < 25):
                            susceptible.get_boosted()
                        if regularZombie in regularZombies and have_cure:
                            x = regularZombie.location[0]
                            y = regularZombie.location[1]
                            regularZombies.remove(regularZombie)
                            regularZombie_count -= 1
                            recovered_count += 1
                            human_count += 1
                            new_recovered = Classes.Recovered(recovered_count, x, y)
                            recovered.append(new_recovered)

        if not susceptible.infected:
            for superZombie in superZombies:
                # checks to see if a zombie is close to the susceptible
                if susceptible.collocated(superZombie):
                    # invoke run method if susceptible is seen by a super zombie
                    escaped = susceptible.run()
                    if not escaped:
                        # if susceptible did not run far enough, they will have to fight that zombie
                        won = susceptible.fight(superZombie)
                        if not won:
                            B = random.randint(1, 15)
                            C = random.randint(1, 20)
                            cure_found = susceptible.find_cure(B, C)
                            if cure_found:
                                have_cure = True
                            infected = susceptible.get_infection()
                            # if susceptible gets infected, destroy susceptible and create new super zombie
                            if susceptible in susceptibles and infected:
                                x = susceptible.location[0]
                                y = susceptible.location[1]
                                susceptibles.remove(susceptible)
                                susceptible_count -= 1
                                human_count -= 1
                                superZombie_count += 1
                                new_superZombie = Classes.SuperZombie(superZombie_count, x, y)
                                superZombies.append(new_superZombie)

                        if won:
                            if have_cure and (susceptible.location[0] < 25 and susceptible.location[1] < 25):
                                susceptible.get_boosted()
                            if superZombie in regularZombies and have_cure:
                                x = superZombie.location[0]
                                y = superZombie.location[1]
                                superZombies.remove(superZombie)
                                superZombie_count -= 1
                                recovered_count += 1
                                human_count += 1
                                new_recovered = Classes.Recovered(recovered_count, x, y)
                                recovered.append(new_recovered)

    count += 1
    regularzombiecount.append(regularZombie_count)
    superzombiecount.append(superZombie_count)
    susceptiblecount.append(susceptible_count)
    recoveredcount.append(recovered_count)

    if human_count <= 0:
        # print results of the simulation
        if count == 1:
            print(f"On the 1st hour of the simulation:")
        elif count == 2:
            print(f"On the 2nd hour of the simulation:")
        elif count == 3:
            print(f"On the 3nd hour of the simulation:")
        else:
            print(f"On the {count}th hour of the simulation:")
        print("All humans have turned into zombies")
        print(f"Number of Regular Zombies: {superZombie_count}")
        print(f"Number of Super Zombies: {regularZombie_count}")
        print(f"Number of Recovered: {recovered_count}")
        print(f"Number of Susceptibles: {susceptible_count}")
        print(f"Number of total humans: {human_count}")
        print("Simulation Over!")
        keep_going = False

    if human_count >= 100:
        if count == 1:
            print(f"On the 1st hour of the simulation:")
        elif count == 2:
            print(f"On the 2nd hour of the simulation:")
        elif count == 3:
            print(f"On the 3nd hour of the simulation:")
        else:
            print(f"On the {count}th hour of the simulation:")
        print("All humans are immune to the infection")
        print(f"Number of Susceptibles: {susceptible_count}")
        print(f"Number of Regular Zombies: {superZombie_count}")
        print(f"Number of Super Zombies: {regularZombie_count}")
        print(f"Number of Recovered: {recovered_count}")
        print(f"Number of total humans: {human_count}")
        print("Simulation Over!")
        keep_going = False

plt.plot(susceptiblecount, label='Susceptible')
plt.plot(regularzombiecount, label='Regular Zombie')
plt.plot(superzombiecount, label='Super Zombie')
plt.plot(recoveredcount, label='Recovered')

plt.xlabel('Time ')
plt.ylabel('Population')
plt.title('Zombie Outbreak Simulation')

plt.legend()

plt.show()
