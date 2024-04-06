import time
import random

def main():
    class Mayor:
        def __init__(self, budget, pop, gov, content, mental,day):
            self.budget = budget
            self.pop = pop
            self.gov = gov
            self.content = content
            self.mental = mental
            self.day = day
            self.killbudget = 0
            self.killpop = False
            self.killgov = 0
            self.killcontent = 0
            self.killmental = 0

        def update_stats(self, changes):

            for key, value in changes.items():
                if hasattr(self, key):
                    setattr(self, key, getattr(self, key) + value)
            self.check_game_over_conditions()
        
        def check_game_over_conditions(self):
            if self.mental < 0:
                self.killmental += 1
            else:
                self.killmental = 0
            if self.content < 50:
                self.killcontent += 1
            else:
                self.killcontent = 0
            if self.gov <= 0:
                self.killgov +=1
            else:
                self.killgov = 0
            if self.pop <= 0:
                self.killpop = True
            if self.budget < 0:
                self.killbudget += 1
            else:
                self.killbudget = 0

            if self.killmental >= 7:
                print(f"Game Over: You lost your mind during this job. Survived {mayor.day} days !")
                return True
            if self.killcontent >= 10:
                print(f"Game Over: People elected other candidate! Survived {mayor.day} days !")
                return True
            if self.killpop == True:
                print(f"Game Over: It's a ghost town! Survived {mayor.day} days !")
                return True
            if self.killgov >=5:
                print(f"Game Over: You were forced to resign by the government. Survived {mayor.day} days !")
                return True 
            if self.killbudget >= 5:
                print(f"Game Over: You bankrupted the Municipal for too long. Survived {mayor.day} days !")
                return True 
            return False  

    mayor = Mayor(budget=100, pop=1000, gov=100, content=100, mental=100, day=0)

    def printStats(mayor):
        mayor.day+=1   
        return print(f"Day {mayor.day}\nBudget: {mayor.budget} Pop size: {mayor.pop} Gov relation: {mayor.gov} People relation: {mayor.content} Your mental: {mayor.mental}")


    class Events:
        def __init__(self, serial, desc, opt1, opt2, out1, out2):
            self.serial = serial
            self.desc = desc
            self.opt1 = opt1
            self.opt2 = opt2
            self.out1 = out1
            self.out2 = out2

    def handle_event(event, mayor):
        print(event.desc)
        print("1.", event.opt1)
        print("2.", event.opt2)
        choice = int(input("Choose option 1 or 2: ")) 
        if choice == 1:
            mayor.update_stats(event.out1)
        elif choice == 2:
            mayor.update_stats(event.out2)
        else:
            print("Invalid choice.")

    mayor = Mayor(budget=100, pop=1000, gov=100, content=100, mental=100, day=0)

    print("Welcome to Boston, this is your first day as Mayor")
    time.sleep(1)

    printStats(mayor)

    events = [
        Events(serial=1, desc="A surge in local industry boosts the economy.", opt1="Invest in local businesses.", opt2="Save the extra revenue.", out1={"budget": 120, "gov": 10, "content": 10}, out2={"budget": 30, "content": 5}),
        Events(serial=2, desc="A natural disaster causes widespread damage.", opt1="Allocate funds for relief.", opt2="Focus on rebuilding.", out1={"budget": 30, "pop": 10, "content": 20, "mental": -110}, out2={"budget": -20, "content": -10, "gov": 5}),
        # Add more events...
    ]

    for i in range(5):
        selected_event = random.choice(events)
        handle_event(selected_event, mayor)
        printStats(mayor)
        time.sleep(1)
        if mayor.check_game_over_conditions():
            break
    
main()