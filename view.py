import pygame

class View():
    def __init__(self, width, height):
            self.width = width
            self.height = height
            self.background_color = (20,20,20)
            self.game_title = "MineWord"
            self.font_path = "ressources/minecraft_font.ttf"
            self.bg = pygame.image.load("ressources/background.png")
            pygame.init()

            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(self.game_title)

    # Main game window
    def main_window(self, word, pressed_letters, penalties, words_found):
        self.clear_screen()
        self.render_counter(words_found)
        self.render_title()
        self.render_life(penalties)
        self.render_word(word, pressed_letters)
        self.render_keyboard(pressed_letters)
        self.render_shortcuts()

    # Show the main title
    def render_title(self):
        font = pygame.font.Font(self.font_path, 40)
        title = font.render(self.game_title, True, 'white')
        self.screen.blit(title, (self.width/2 - title.get_width()/2, title.get_height() + 20))


    # Show the word with found letters and _ for not found letters
    def render_word(self, word, pressed_letters):
        letter_size = 30
        margin = 5
        word_width = (letter_size + margin) * len(word) - margin
        start_x = (self.width - word_width) / 2        

        font = pygame.font.Font(self.font_path, 30)
        for char in word:
            display_char = char if char in pressed_letters else "_"
            rendered_char = font.render(display_char, True, 'white')
            self.screen.blit(rendered_char, (start_x, self.height - 200))
            start_x += letter_size + margin

    # Clear the screen
    def clear_screen(self):
        self.screen.blit(self.bg, (0, 0))
        #self.screen.fill(self.background_color)        
        self.font= pygame.font.Font(self.font_path, 15)

    # Show the keyboard on screen
    def render_keyboard(self, pressed_letters):
        alphabet = "azertyuiopqsdfghjklmwxcvbn"
        letter_size = 20
        margin = 10

        keyboard_width = (letter_size + margin) * len(alphabet) - margin
        start_x = (self.width - keyboard_width/2) / 2
        start_y = self.height - 120

        for char in alphabet:
            
            font = pygame.font.Font(self.font_path, letter_size)
            letter = font.render(char, True, 'white')
            
            if char in pressed_letters:
                letter = font.render(char, True, (30,30,30))

            if(alphabet.index(char) == len(alphabet) // 2):
                margin = 10
                start_y += letter_size + margin
                
            self.screen.blit(letter, (start_x + margin, start_y))
            margin += letter_size + 10

    def game_over(self, word, penalties, words_found):
        self.clear_screen()

        self.render_counter(words_found + 1 if penalties < 10 else words_found)

        # Game Over text
        font = pygame.font.Font(self.font_path, 50)
        title_text = "You Lost!" if penalties >= 10 else "You Won!"
        title = font.render(title_text, True, 'white')
        self.screen.blit(title, (self.width/2 - title.get_width()/2, self.height/2 - title.get_height()/2 - 100))

        # Show the correct word
        font = pygame.font.Font(self.font_path, 30)
        word_display = font.render("The word was : " + word, True, 'white')
        self.screen.blit(word_display, (self.width/2 - word_display.get_width()/2, self.height/2 - word_display.get_height()/2))

        if penalties <= 10:
            # Show the number of penalties
            penalties_display = font.render("Penalties : " + str(penalties) , True, 'white')
            self.screen.blit(penalties_display, (self.width/2 - penalties_display.get_width()/2, self.height/2 - penalties_display.get_height()/2 + 50))

        # Press any key to restart
        font = pygame.font.Font(self.font_path, 20)
        restart_display = font.render("Press R to continue", True, 'white')
        self.screen.blit(restart_display, (self.width/2 - restart_display.get_width()/2, self.height/2 - restart_display.get_height()/2 + 100))

        if penalties >= 10:
            score_display = font.render("Press enter to see the scoreboard", True, 'white')
            self.screen.blit(score_display, (self.width/2 - score_display.get_width()/2, self.height/2 - score_display.get_height()/2 + 130))

    def render_counter(self, words_found):
        font = pygame.font.Font(self.font_path, 15)
        counter = font.render(f"Words found : " + str(words_found), True, 'white')
        self.screen.blit(counter, (10, 10))


    def render_life(self, penalties):
        heart_img = pygame.image.load("ressources/heart.png").convert_alpha()
        heart_empty_img = pygame.image.load("ressources/heart_empty.png").convert_alpha()
        
        heart_size = 30
        heart_img = pygame.transform.scale(heart_img, (heart_size, heart_size))
        heart_empty_img = pygame.transform.scale(heart_empty_img, (heart_size, heart_size))
        max_lives = 10
        x_start = self.width/2 - (heart_size * max_lives + 5 * (max_lives - 1)) / 2
        y = self.height/2 - heart_size - 10
        
        for i in range(max_lives):

            x = x_start + i * (heart_size + 5)

            if i < (max_lives - penalties):
                self.screen.blit(heart_img, (x, y))
            else:
                self.screen.blit(heart_empty_img, (x, y))

    def render_shortcuts(self):
        
        font = pygame.font.Font(self.font_path, 12)
        word_display = font.render("Press ENTER to access the scoreboard", True, 'white')
        self.screen.blit(word_display, (self.width/2 - word_display.get_width()/2, self.height - word_display.get_height() - 35))
        
        word_display = font.render("Press ESCAPE to exit the game", True, 'white')
        self.screen.blit(word_display, (self.width/2 - word_display.get_width()/2, self.height - word_display.get_height() - 15))


    def scoreboard(self, name, scores, penalties):
        self.clear_screen()

        font = pygame.font.Font(self.font_path, 40)
        title = font.render("Scoreboard", True, 'white')
        self.screen.blit(title, (self.width/2 - title.get_width()/2, 50))

        font = pygame.font.Font(self.font_path, 20)

        y_offset = 150
        for score in scores[-10:]:
            score_text = font.render(score, True, 'white')
            self.screen.blit(score_text, (self.width/2 - score_text.get_width()/2, y_offset))
            y_offset += 30

        font = pygame.font.Font(self.font_path, 15)

        if penalties >= 10:

            restart_display = font.render("Enter your name : " + name, True, 'white')
            self.screen.blit(restart_display, (self.width/2 - restart_display.get_width()/2, self.height - 150))

            restart_display = font.render("Press ENTER to add your score to the leaderboard", True, 'white')
            self.screen.blit(restart_display, (self.width/2 - restart_display.get_width()/2, self.height - 100))

        restart_display = font.render("Press ESC to quit the scoreboard", True, 'white')
        self.screen.blit(restart_display, (self.width/2 - restart_display.get_width()/2, self.height - 50))