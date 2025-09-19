import random
import pygame
from view import View

class Controller():
    def __init__(self):
        self.view = View(600,600)
        self.run = True
        self.already_used_words = []
        self.word = self.random_word()
        self.pressed_letters = ""
        self.penalties = 0
        self.words_found = 0
        self.game_over_sound = True

    # Main function (loop)
    def start(self): 
        
        while self.run:
            if self.is_over():
                
                if self.game_over_sound:
                    self.view.death_sound() if self.penalties >= 10 else self.view.victory_sound()
                    self.game_over_sound = False

                self.view.game_over(self.word, self.penalties, self.words_found)
                self.get_pygame_event_over()
            else:
                self.get_pygame_event()
                self.view.main_window(self.word, self.pressed_letters, self.penalties, self.words_found)
            
            pygame.display.update()

        pygame.quit()

    # Key events
    def get_pygame_event(self):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False

                    # Keybord alphabet    
                    if event.unicode.isalpha():
                        letter = event.unicode
                        self.is_in_word(letter)    
                        self.pressed_letters += letter

                    if event.key == pygame.K_RETURN:
                        self.scoreboard()

                if event.type == pygame.QUIT:
                    self.run = False


    # Key events for game over
    def get_pygame_event_over(self):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run = False
                    if event.key == pygame.K_r:
                        self.restart()
                    if event.key == pygame.K_RETURN:
                        self.scoreboard()
                if event.type == pygame.QUIT:
                    self.run = False


    # Restart the game
    def restart(self):
        
        if self.is_found():
            self.words_found += 1
        else:
            self.words_found = 0
        
        self.word = self.random_word()
        self.pressed_letters = ""
        self.penalties = 0
        self.run = True
        self.game_over_sound = True


    # Return a random english word from the words.txt file
    def random_word(self):
        english_words = f = open('ressources/words_minecraft.txt')
        english_words = f.read().splitlines()
        f.close()

        word = english_words[random.randint(0, len(english_words)-1)].lower()

        if word not in self.already_used_words:
            self.already_used_words.append(word)
            return word
        else:
            self.random_word()  
    
    def is_in_word(self, letter):
        if letter not in self.word and letter not in self.pressed_letters:
            self.penalties += 1
            self.view.hit_sound()
        if letter in self.word and letter not in self.pressed_letters:
            self.view.plop_sound()
        if letter in self.pressed_letters:
            self.view.button_sound()



    # Return True if more than 10 penalities
    def is_over(self):
        return self.penalties >= 10 or self.is_found()
    
    
    def insert_score(self, name, score):
        f = open('ressources/scoreboard.txt', 'a')
        score = name + " : " + str(score) + "\n"
        f.write(score)
        f.close()

        print("score inserted")

    # Test if each letter have been found
    def is_found(self):
        for char in self.word:
            if char not in self.pressed_letters:
                # Return false if one letter isn't
                return False
        # Return true if none is missing
        return True
    

    def get_score(self):
        f = open('ressources/scoreboard.txt', 'r')
        scores = f.read().splitlines()
        f.close()
        return scores

    def scoreboard(self):
        run = True
        name = ""
        while run:
            self.view.scoreboard(name, self.get_score(), self.penalties)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():        
                        letter = event.unicode
                        name += letter
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    if event.key == pygame.K_RETURN and self.penalties <= 10 and name != "":
                        self.insert_score(name, self.words_found)
                    if event.key == pygame.K_ESCAPE:
                        run = False
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()