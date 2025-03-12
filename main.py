# pokergame!
import pygame
import random

window_width = 960
window_height = 540
screen = pygame.display.set_mode((window_width, window_height))

base_backround = (90, 90, 100)
backround1 = (53, 101, 77)
backround2 = (148, 34, 34)
backround3 = (52, 21, 57)

pygame.init()

class Game:
    def __init__(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption("cardgames!")
        run = True

        title_text1 = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/text1.png").convert_alpha()

        img1 = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button1.png").convert_alpha()
        img1down = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button1down.png").convert_alpha()
        button1 = StartButton(64, 340, img1, img1down, 0.4)

        img2 = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button2.png").convert_alpha()
        img2down = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button2down.png").convert_alpha()
        button2 = StartButton(362, 340, img2, img2down, 0.4)
        
        img3 = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button3.png").convert_alpha()
        img3down = pygame.image.load("C:/Users/ivalm/newgame/img/buttons_text/button3down.png").convert_alpha()
        button3 = StartButton(660, 340, img3, img3down, 0.4)

        transtion1 = Transition(backround1)
        transtion2 = Transition(backround2)
        transtion3 = Transition(backround3)

        wargame1 = WarGame()

        state = 0

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            if state == 0:
                screen.fill(base_backround)

                screen.blit(title_text1, (160, 80))

                if button1.Draw():
                    state = 1
                if button2.Draw():
                    state = 2
                if button3.Draw():
                    state = 3

            if state == 1:
                if transtion1.Expand():
                    wargame1.PlayRound()

            if state == 2:
                if transtion2.Expand():
                    # start game
                    if pygame.mouse.get_pressed()[0]:
                        run = False
            
            if state == 3:
                if transtion3.Expand():
                    # start game
                    if pygame.mouse.get_pressed()[0]:
                        run = False

            pygame.display.update()
            clock.tick(60)  # limits FPS to 60
        pygame.quit()

class WarGame:
    def __init__(self):
        self.deck1 = Deck()
        self.card_names = self.deck1.cards
        self.card_images = {}
        for name in self.card_names:
            filename = 'C:/Users/ivalm/newgame/img/cards/' + repr(name) + '.png'
            self.card_images[name] = pygame.image.load(filename).convert_alpha()

        self.red_cardstack = pygame.image.load("C:/Users/ivalm/newgame/img/cards_back/red1_stack.png").convert_alpha()
        self.blue_cardstack = pygame.image.load("C:/Users/ivalm/newgame/img/cards_back/blue1_stack.png").convert_alpha()

        self.red_card= pygame.image.load("C:/Users/ivalm/newgame/img/cards_back/red1.png").convert_alpha()
        self.blue_card= pygame.image.load("C:/Users/ivalm/newgame/img/cards_back/blue1.png").convert_alpha()

        self.movecardx1, self.movecardy1 = 40, 120
        self.movecardx2, self.movecardy2 = 724, 120

        self.player1_cards = self.card_names[0:26]
        self.player2_cards = self.card_names[26:52]

        self.stackbutton1 = CardButton()
        self.stackbutton2 = CardButton()
        self.cardbutton1 = CardButton()
        self.cardbutton2 = CardButton()
        self.main_state = 0
        self.speed = 10

        self.p1_state = 0
        self.p2_state = 0

    def PlayRound(self):
        pos = pygame.mouse.get_pos()

        player1_card = self.player1_cards[-1]
        player2_card = self.player2_cards[-1]

        image1 = self.card_images[player1_card]
        image2 = self.card_images[player2_card]

        scale_stackcard_red = pygame.transform.scale(self.red_cardstack, (196, 292))
        screen.blit(scale_stackcard_red, (40, 120))
        scale_stackcard_blue = pygame.transform.scale(self.blue_cardstack, (196, 292))
        screen.blit(scale_stackcard_blue, (724, 120))

        scale_card_red = pygame.transform.scale(self.red_card, (192, 256))
        scale_card_blue = pygame.transform.scale(self.blue_card, (192, 256))

        player1_deck_target = scale_stackcard_red.get_rect(center=(138, 268))
        player2_deck_target = scale_stackcard_blue.get_rect(center=(822, 268))
        player1_card_target = scale_card_red.get_rect(center=(366, 288))
        player2_card_target = scale_card_blue.get_rect(center=(590, 288))

        stack1_state = self.stackbutton1.isClicked(pos, player1_deck_target, self.main_state)
        stack2_state = self.stackbutton2.isClicked(pos, player2_deck_target, self.main_state)
        card1_state = self.cardbutton1.isClicked(pos, player1_card_target, self.main_state)
        card2_state = self.cardbutton2.isClicked(pos, player2_card_target, self.main_state)

        if self.main_state == 0:
            if self.p1_state == 0:
                if stack1_state:
                    screen.blit(scale_card_red, (self.movecardx1, self.movecardy1))
                    if self.movecardx1 < 270:
                        self.movecardx1 += self.speed
                    elif self.movecardx1 >= 270 and self.movecardy1 < 160:
                        self.movecardy1 += self.speed
                    else:
                        self.p1_state = 1
            elif self.p1_state == 1:
                screen.blit(scale_card_red, (self.movecardx1, self.movecardy1))
                if card1_state:
                    p1_placed_card = pygame.transform.scale(image1, (192, 256))
                    screen.blit(p1_placed_card, (270, 160))

            if self.p2_state == 0:
                if stack2_state:
                    screen.blit(scale_card_blue, (self.movecardx2, self.movecardy2))
                    if self.movecardx2 > 494:
                        self.movecardx2 -= self.speed
                    elif self.movecardx2 <= 494 and self.movecardy2 < 160:
                        self.movecardy2 += self.speed
                    else:
                        self.p2_state = 1
            elif self.p2_state == 1:
                screen.blit(scale_card_blue, (self.movecardx2, self.movecardy2))
                if card2_state:
                    p2_placed_card = pygame.transform.scale(image2, (192, 256))
                    screen.blit(p2_placed_card, (494, 160))

            if card1_state and card2_state:
                self.main_state = 1

        elif self.main_state == 1:
            if True:
                pass

        """ 
        When you come back to work on this add individual functionality for each card
        so player1 cand have card moved and then flipped but from there futher action requires
        player 2 to have both actions performed first.
        Also add when winner is chosen cards both flip to winner's color and then they
        slide under winners deck.

        Previous code to refrence
        
        scale_p1 = pygame.transform.scale(image1, (240, 320))
        screen.blit(scale_p1, (50, 110))

        scale_p2 = pygame.transform.scale(image2, (240, 320))
        screen.blit(scale_p2, (670, 110))

        self.movecardx1, self.movecardy1 = 357.5, 65
        self.movecardx2, self.movecardy2 = 357.5, 65

        self.main_state = 0
        repr(self.deck1.take_card())
        repr(self.deck1.take_card())
        
        """

class CardButton:
    def __init__(self):
        self.clicked = False
        self.letgo = False
        self.card_move = 0
        self.game_state = False

    def isClicked(self, pos, card_target, mainstate):
        if card_target.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.letgo = True
        
        if pygame.mouse.get_pressed()[0] == 0 and self.letgo == True:
            self.game_state = not self.game_state
            self.card_move = 1
            self.letgo = False
        elif pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        return self.game_state

class Transition:
    def __init__(self, backround_color):
            self.transitioned = False
            self.backround = backround_color

            self.rect_center = (480, 270)
            self.rect_x, self.rect_y = 480, 270
            self.rect_width, self.rect_height = 9, 5
            self.scale_by = 1.1
    
    def Expand(self):
        if self.transitioned == False:
            self.rect_width *= self.scale_by
            self.rect_height *= self.scale_by

            self.rect_x = self.rect_center[0] - self.rect_width // 2
            self.rect_y = self.rect_center[1] - self.rect_height // 2

            pygame.draw.rect(screen, self.backround, (self.rect_x, self.rect_y, self.rect_width, self.rect_height))
            
            if self.rect_width > 1000 or self.rect_height > 600:
                self.transitioned = True

        if self.transitioned == True:
            screen.fill(self.backround)
            return True

class StartButton:
    def __init__(self, x, y, image, image_down, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.image_down = pygame.transform.scale(image_down, (int(width * scale), int(height * scale)))

        self.clicked = False
        self.hold = False
    
    def Draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # if mouse is over button then if mouse is click and hasn't been clicked before 
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                screen.blit(self.image_down, (self.rect.x, self.rect.y))
                self.hold = True
        
        if pygame.mouse.get_pressed()[0] == 0 and self.clicked == False and self.hold == True:
            action = True
            self.clicked = True

        return action

class Card:
    suits = ["spades",
             "hearts",
             "diamonds",
             "clubs"]
    
    values = [None, None,"2", "3",
              "4", "5", "6", "7",
              "8", "9", "10",
              "Jack", "Queen",
              "King", "Ace"]

    def __init__(self, v, s):
        self.value = v
        self.suit = s

    def cardImage(self):
        if self.suit == 1:
            pass
            

    def __lt__(self, c2):
        if self.value < c2.value:
            return True
        # if self.value == c2.value:
        #     if self.suit < c2.suit:
        #         return True
        #     else:
        #         return False
        return False
    
    def __gt__(self, c2):
        if self.value > c2.value:
            return True
        # if self.value == c2.value:
        #     if self.suit > c2.suit:
        #         return True
        #     else:
        #         return False
        return False
    
    def __str__(self):
        return self.values[self.value] + " of " + self.suits[self.suit]

    def __repr__(self):
        return self.values[self.value] + "_" + self.suits[self.suit]
    
class Deck:
    def __init__(self):
        self.cards = []

        for i in range(2, 15):
            for j in range(4):
                self.cards.append(Card(i,j))

        random.shuffle(self.cards)

    def take_card(self):
        if len(self.cards) == 0:
            return
        return self.cards.pop()
    
class Player:
    def __init__(self, name):
        self.balance = 10
        self.cards = []
        self.name = name

class PokerGame:
    def __init__(self):
        name = input("Player name: ")
        self.deck = Deck()
        self.player = Player(name)
        self.npc1 = Player("Bob")
        self.npc2 = Player("Lenard")
        self.npc3 = Player("Tasha")

Game()