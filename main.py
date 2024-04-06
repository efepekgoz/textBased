import pygame
import random
import time
import asyncio


pygame.init()
pygame.mixer.init()


screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mayor of Boston")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 65)
check = 0

font = pygame.font.Font(None, 32)

def text_objects(text, font):
    textSurface = font.render(text, True, GREEN)
    return textSurface, textSurface.get_rect()

def message_display(text, x, y, width=200, height=40):
    TextSurf, TextRect = text_objects(text, font)
    TextRect.center = ((x+(width/2)), (y+(height/2)))
    screen.blit(TextSurf, TextRect)

class Mayor:
    def __init__(self, budget, pop, gov, content, mental, day):
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
        game_over_reason = ""  
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

        game_over = False
        if self.killmental >= 7:
            game_over_reason = "Lost your mind"
            game_over = True
        elif self.killcontent >= 10:
            game_over_reason = "Elected another candidate"
            game_over = True
        elif self.killpop == True:
            game_over_reason = "It's a ghost town"
            game_over = True
        elif self.killgov >= 5:
            game_over_reason = "Forced to resign"
            game_over = True
        elif self.killbudget >= 5:
            game_over_reason = "Bankrupted the Municipal"
            game_over = True

        return game_over, game_over_reason

class Event:
    def __init__(self, desc, opt1, opt2, out1, out2):
        self.desc = desc
        self.opt1 = opt1
        self.opt2 = opt2
        self.out1 = out1
        self.out2 = out2

async def main():
    pygame.mixer.music.load('./resources/usanthem.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05) 
    mayor = Mayor(budget=100, pop=500, gov=100, content=100, mental=100, day=0)
    events = [
    Event("Unexpected budget surplus.", "Increase public services.", "Save for future needs.", {"budget": -40, "content": 15}, {"budget": 80}),
    Event("A great molasses flood reported!", "Strengthen flood defenses.", "Offer relief to affected.", {"budget": -35, "pop": 10, "content": 5}, {"budget": -5, "content": 10, "mental":40}),
    Event("Local school underfunded.", "Invest in education.", "Promote private donations.", {"budget": -30, "content": 10, "mental": 5}, {"gov": 5, "content": 5}),
    Event("Rising crime rates.", "Fund police department.", "Community policing initiatives.", {"budget": -40, "content": -25, "mental": -25}, {"budget": -25, "content": 10, "mental": 5}),
    Event("Factory pollution concerns.", "Impose environmental regulations.", "Encourage voluntary measures.", {"budget": -25, "content": 10, "gov": -25}, {"content": 5, "gov": 5}),
    Event("Historic building in disrepair.", "Restore the landmark.", "Sell it to private developers.", {"budget": -40, "content": 20}, {"budget": 15, "content": -30, "mental":-20}),
    Event("Increase in homeless population.", "Open new shelters.", "Fund job training programs.", {"budget": -35, "content": 15}, {"budget": -30, "content": 10, "pop": -50}),
    Event("Tourism decline.", "Advertise in other cities.", "Improve local attractions.", {"budget": -30, "content": 10}, {"budget": -40, "content": 15}),
    Event("Local library lacks books.", "Fund new acquisitions.", "Organize a donation drive.", {"budget": -25, "content": 10}, {"content": 5, "pop": 20}),
    Event("Public transport is overcrowded.", "Expand service routes.", "Increase ticket prices.", {"budget": -35, "content": 15}, {"budget": 5, "content": -30}),
    Event("City park needs renovation.", "Allocate funds for upgrade.", "Encourage volunteer work.", {"budget": -20, "content": 10}, {"content": -15, "gov": 5}),
    Event("Water supply contamination.", "Invest in water treatment.", "Distribute bottled water.", {"budget": -30, "pop": -20, "content": -10}, {"budget": -15, "content": 5}),
    Event("Food poisoning outbreak at festival.", "Strengthen food safety laws.", "Compensate affected individuals.", {"budget": -15, "gov": -25, "content": -30}, {"budget": -40, "content": 40}),
    Event("Public art funding cuts.", "Restore funding.", "Support private art displays.", {"budget": -35, "content": 10}, {"content": 25, "gov": 5}),
    Event("Veterans request more support.", "Increase veterans' benefits.", "Promote private charity support.", {"budget": -10, "content": 15, "gov": 5}, {"content": 5, "mental": 5}),
    Event("Teachers strike for higher wages.", "Meet their demands.", "Negotiate for future raises.", {"budget": -40, "content": 50, "gov": -35}, {"budget": -10, "content": 5, "gov": 5}),
    Event("Rural areas lack healthcare.", "Build new clinics.", "Subsidize travel for treatment.", {"budget": -20, "pop":55, "content": 30}, {"budget": -10, "content": 5}),
    Event("City zoo faces closure.", "Provide financial assistance.", "Seek private investors.", {"budget": -20, "content": 10}, {"content": -5, "gov": 15}),
    Event("Downtown parking shortages.", "Construct parking garages.", "Promote public transit use.", {"budget": -35, "content": 5}, {"budget": -5, "content": 10}),
    Event("Demand for renewable energy.", "Invest in solar panels.", "Offer tax incentives.", {"budget": -40, "content": 10, "gov": 5}, {"budget": -5, "content": 5, "gov": 10}),
    Event("Need for elderly care services.", "Fund public senior centers.", "Incentivize private care facilities.", {"budget": -35, "content": 15}, {"budget": -15, "content": 10, "gov": 5}),
    Event("Public outcry over taxes.", "Lower tax rates.", "Explain necessity for public services.", {"budget": 320, "content": 20}, {"content": -30, "gov": 5}),
    Event("City hall needs repairs.", "Allocate budget for renovation.", "Delay repairs for other projects.", {"budget": -25, "content": 5}, {"budget": 10, "content": -5}),
    Event("Feral cats problem in neighborhoods.", "Implement catch and release program.", "Encourage adoption.", {"budget": -5, "content": 10}, {"content": 5, "pop": 1}),
    Event("Local sports team requests new stadium.", "Fund the construction.", "Decline funding, suggest private investment.", {"budget": -50, "content": 20, "gov": -15}, {"content": -20, "gov": 20}),
    Event("A big company proposes building their new headquarters in your city.", "Offer tax incentives.", "Decline, focusing on small businesses.", {"budget": 100, "content": -5, "gov": -10}, {"budget": -10, "content": 50, "gov": 45}),
    Event("A neighboring city's dam is at risk of breaking, threatening their water supply.", "Sell water at a premium.", "Provide water aid for free.", {"budget": 120, "content": -20, "gov": 5, "mental": -100}, {"budget": -20, "content": 20, "gov": 10, "mental": 20}),
    Event("A major film studio wants to shoot a blockbuster in your city.", "Negotiate a high fee for city scenes.", "Allow them to film for free for the publicity.", {"budget": 80, "content": 5, "gov": -5}, {"budget": -5, "content": 15, "gov": -45}),
    Event("Discover a rare mineral resource within city limits.", "Lease the land to mining companies.", "Preserve the land for environmental reasons.", {"budget": 150, "content": -15, "gov": 10}, {"budget": -10, "content": 20, "gov": -5}),
    Event("A billionaire offers to pay off the city's debt.", "Accept the offer with a public partnership naming.", "Politely decline, fearing too much influence.", {"budget": 200, "content": -10, "gov": -20}, {"budget": 0, "content": 10, "gov": 20}),
    Event("A renowned international festival is looking for a new home city.", "Bid to host the festival.", "Focus on local events.", {"pop": 100, "budget": -30, "content": 15}, {"budget": 10, "content": -5}),
    Event("A large-scale riot breaks out after a controversial court ruling.", "Deploy the national guard.", "Let local law enforcement handle the situation with minimal interference.", {"gov": 40, "content": -100, "pop": -100}, {"budget": -10, "content": -60, "gov": -10, "pop": -200}),
    Event("A virulent disease outbreak threatens the city's population.", "Enforce a city-wide quarantine.", "Do nothing and hope it passes.", {"pop": 50, "content": -80, "mental": -10}, {"pop": -200, "content": 80, "mental": -120}),
    Event("The city's crops are contaminated with a harmful chemical.", "Provide food to all residents.", "Hide the truth.", {"budget": -100, "content": 50, "mental": 40}, {"budget": 10, "content": -40, "pop": -300,"gov":-70})

]

    clock = pygame.time.Clock()
    running = True
    waiting_for_input = False
    selected_event = None
    game_over = False
    game_over_reason = ""

    game_started = False

    while not game_started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_started = True
            elif event.type == pygame.KEYDOWN:
                game_started = True

        screen.fill(BLACK)
        message_display("Welcome to Boston, this is your first day as Mayor!", 100, 100, 600, 50)
        pygame.display.flip()
        await asyncio.sleep(0.1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not waiting_for_input and not game_over:
                selected_event = random.choice(events)
                waiting_for_input = True
            elif event.type == pygame.KEYDOWN and waiting_for_input:
                if event.key == pygame.K_1:
                    mayor.update_stats(selected_event.out1)
                    waiting_for_input = False
                    mayor.day += 1
                elif event.key == pygame.K_2:
                    mayor.update_stats(selected_event.out2)
                    waiting_for_input = False
                    mayor.day += 1
                game_over, game_over_reason = mayor.check_game_over_conditions()

        screen.fill(BLACK)

        if not game_over:
            if not waiting_for_input:
                message_display("Press any key for the next day", 100, 80, 600, 50)
            else:
                message_display(selected_event.desc, 100, 100, 600, 50)
                message_display("1. " + selected_event.opt1, 100, 200, 600, 50)
                message_display("2. " + selected_event.opt2, 100, 250, 600, 50)
        else:
            message_display(f"Game Over: {game_over_reason}", 100, 100, 600, 50)
            message_display(f"Survived for {mayor.day} days!",100, 180, 600, 50)

        # Stats
        message_display(f"Day: {mayor.day}", 50, 350)
        message_display(f"Budget: {mayor.budget}", 50, 400)
        message_display(f"Population: {mayor.pop}", 50, 450)
        message_display(f"Government Relations: {mayor.gov}", 400, 350)
        message_display(f"People's Contentment: {mayor.content}", 400, 400)
        message_display(f"Mental Health: {mayor.mental}", 400, 450)

        pygame.display.flip()
        clock.tick(30)
        await asyncio.sleep(0)
    pygame.quit()

"""if __name__ == "__main__":
    run_game()
"""

asyncio.run(main())