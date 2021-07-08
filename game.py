import pygame,sys,random

pygame.init()



pygame.display.set_caption("FLOOD IT")

WHITE = (255,) * 3
BLACK = (0,) * 3
RED = (255,0,0)



class Button(pygame.sprite.Sprite):


    def __init__(self,x,y,button_text,button_color,text_color,font):
        super().__init__()

        
        text=font.render(button_text,True,text_color)
        self.original_image = pygame.Surface((text.get_width(),text.get_height() + 20))

        self.original_image.fill(button_color)
        self.original_image.blit(text,(0,10))
        self.bigger_image = pygame.Surface((text.get_width() + 10,text.get_height() + 30))
        self.bigger_image.fill(button_color)
        self.bigger_image.blit(text,(5,15))
        self.original_rect = self.original_image.get_rect(topleft=(x,y))
        self.bigger_rect = self.bigger_image.get_rect(center=self.original_rect.center)
        self.image = self.original_image
        self.rect = self.original_rect
        self.hovered_on = False


    def update(self,point):


        on = self.clicked_on(point)


        if not self.hovered_on and on:
            self.hovered_on = True
            self.rect = self.bigger_rect
            self.image = self.bigger_image
        elif self.hovered_on and not on:
            self.hovered_on = False
            self.rect = self.original_rect
            self.image = self.original_image


    def clicked_on(self,point):
        return self.rect.collidepoint(point)









class Game:

    
    place_sound = pygame.mixer.Sound("pop_sound.wav")
    high_score_file = "high_scores.txt"
    class Square(pygame.sprite.Sprite):

        def __init__(self,x,y,width,height,color):
            # x,y rperesent top-left x and y location of square
            super().__init__()
            self.color = color
            self.image = pygame.Surface((width,height))
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft=(x,y))
            self.hovered_on = False
        

        

        def update_color(self,color):
            self.color = color
            self.image.fill(color)


        
        def draw(self,screen,point=None):

            screen.blit(self.image,self.rect)
            

            if point:
                if self.clicked_on(point):
                    pygame.draw.rect(screen,WHITE,(*self.rect.topleft,self.rect.width,self.rect.height),6,border_radius=5)
            else:
                pygame.draw.rect(screen,BLACK,(*self.rect.topleft,self.rect.width,self.rect.height),1)










        def clicked_on(self,point):

            return self.rect.collidepoint(point)
    
    
    class Board(pygame.sprite.Sprite):


        def __init__(self,rows,cols,square_width,topleft_x,topleft_y):


            self.board = [[Game.Square(topleft_x + (square_width * j),topleft_y + (square_width * i),square_width,square_width,random.choice(Game.COLORS)) for j in range(cols)] for i in range(rows)]

        
        def draw(self,screen):


            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    self.board[row][col].draw(screen)
        

        def reset(self):
            for row in range(len(self.board)):
                for col in range(len(self.board[0])):
                    self.board[row][col].update_color(random.choice(Game.COLORS))


        def update_color(self,row,col,color):
            self.board[row][col].update_color(color)
        def get_color(self,row,col):
            return self.board[row][col].color

    BGCOLOR = (25,56,25)
    COLORS = [(0,150,200),(255,25,50),(125,200,0),(255,255,35),(150,0,150),(255,125,0)]
    
    title_font = pygame.font.SysFont("calibri",60,bold=True)
    text_font = pygame.font.SysFont("calibri",20)
    button_font = pygame.font.SysFont("calibri",30)


    def __init__(self,screen_width=800,screen_height=800,rows=14,cols=14,edge_gap=20):
        self.edge_gap = edge_gap
        self.rows = rows
        self.cols = cols
        self.screen_height = screen_height
        self.title_text = self.title_font.render("Flood it",True,WHITE)
        self.instructions_text = self.text_font.render("Fill the entire board with the same color with 25 flood fills or less.",True,WHITE)

        

        self.moves = 0


        self.board,self.screen_width = self._generate_board()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.title_text_rect = self.title_text.get_rect(center=(self.screen_width//2,edge_gap + self.title_text.get_height()//2))
        self.instructions_text_rect = self.instructions_text.get_rect(center=(self.screen_width//2,edge_gap * 2 + self.title_text.get_height() + self.instructions_text.get_height()//2))
        self.move_text = self.title_font.render("0/25",True,WHITE)
        y= self._generate_color_picker_squares()
        self.move_text_y = y


        self.move_text_rect = self.move_text.get_rect(center=(self.screen_width//2,y+  5+ self.move_text.get_height()//2 ))
        self.game_over_text = self.title_font.render("GAME OVER",True,WHITE)
        self.game_over_surface = pygame.Surface(self.game_over_text.get_size(),pygame.SRCALPHA)
        new_game_button = Button(edge_gap,self.title_text_rect.top,"NEW GAME",RED,BLACK,self.button_font)
        self.high_scores_button = Button(self.title_text_rect.right +edge_gap,self.title_text_rect.top,"TOP SCORES",RED,BLACK,self.button_font)
        

        self._read_high_scores()

        self.high_scores_surface = pygame.Surface((self.screen_width * 3/4,self.screen_height * 3/4),flags=pygame.SRCALPHA)
        self.high_scores_surface_rect = self.high_scores_surface.get_rect(center=(self.screen_width//2,self.screen_height//2))
        self.high_scores_surface.fill((255,255,255,225))
        self._update_high_scores_surface()
        self.buttons = pygame.sprite.Group(new_game_button,self.high_scores_button)


        self.game_over_surface.fill((255,255,255,230))


        self.game_over_surface.blit(self.game_over_text,(0,0),special_flags=pygame.BLEND_RGBA_MULT)



        self.game_over = False


        self._play()
    

    def _read_high_scores(self):
        with open(self.high_score_file,'r') as f:
            text = f.read()
            
        if text:
            self.high_scores = list(map(int,f.readlines()))
        else:
            self.high_scores = []
    
    def _update_high_scores_surface(self):
        high_score_text = self.title_font.render("HIGH SCORES",True,BLACK)

        self.high_scores_surface.blit(high_score_text,(self.high_scores_surface.get_width()//2 - high_score_text.get_width()//2,10))
        start_y = 20 + high_score_text.get_height()
        if not self.high_scores:
            text = self.title_font.render("NO FILLS YET!",True,BLACK)
            self.high_scores_surface.blit(text,(self.high_scores_surface.get_width()//2 - text.get_width()//2,start_y))

        else:
        
            gap = 5
            for i,score in enumerate(self.high_scores):
                text = self.title_font.render(f"{i + 1:<2}. {str(score):<2}",True,BLACK)
                self.high_scores_surface.blit(text,(self.high_scores_surface.get_width()//2 - text.get_width()//2,start_y + (text.get_height() +gap ) * i))


    
    def _generate_board(self):


        
        topleft_y = 5 * self.edge_gap +100+ self.title_text.get_height()
        square_width = (self.screen_height - topleft_y - self.edge_gap)//self.cols
        #square_width = (self.screen_width - 4 * self.edge_gap)//self.cols
        screen_width =  self.edge_gap * 2+ square_width * self.cols
        
        topleft_x = self.edge_gap
        return Game.Board(self.rows,self.cols,square_width,topleft_x,topleft_y),screen_width

    
    def _generate_color_picker_squares(self):

        self.color_pickers = pygame.sprite.Group()
        gap = 10
        square_width = (self.screen_width - self.edge_gap * 2 - gap * (len(self.COLORS) - 1))//len(self.COLORS)
        top_y = self.instructions_text_rect.bottom + self.edge_gap
        for i,color in enumerate(self.COLORS):
            square = Game.Square(self.edge_gap + (square_width + gap) * i,top_y,square_width,60,color)
            self.color_pickers.add(square)


        return top_y + 60



    def _update_moves_text(self):
        self.move_text = self.title_font.render(f"{self.moves}/25",True,WHITE)


        self.move_text_rect = self.move_text.get_rect(center=(self.screen_width//2,self.move_text_y+  5+ self.move_text.get_height()//2 ))

    
    def flood_fill(self,color):

        

        matching_color = self.board.get_color(0,0)
        print(matching_color)
        

        in_bounds = lambda row,col: 0 <= row < self.rows and 0 <= col < self.cols

        def _flood_fill(row,col):
            

            visited.add((row,col))
            self.board.update_color(row,col,color)

        


            for x_diff,y_diff in ((0,1),(0,-1),(1,0),(-1,0)):
                neighbor_row,neighbor_col = row + x_diff,col + y_diff
                if in_bounds(neighbor_row,neighbor_col) and (neighbor_row,neighbor_col) not in visited and self.board.get_color(neighbor_row,neighbor_col)== matching_color:
                    _flood_fill(neighbor_row,neighbor_col)


        visited = set()
        _flood_fill(0,0)







    def _reset(self):
        self.board.reset()
        self.moves = 0
        self.move_text = self.title_font.render(f"{self.moves}/25",True,WHITE)






    def _play(self):

            

        showing_stats = False
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:


                    point = pygame.mouse.get_pos()
                    

                    if not showing_stats:
                        for color_picker in self.color_pickers:
                            if color_picker.clicked_on(point):
                                self.place_sound.play()
                                self.flood_fill(color_picker.color)
                                self.moves += 1
                                self._update_moves_text()
                                if self.moves == 25:
                                    self.game_over = True

                        for i,button in enumerate(self.buttons): 
                            if button.clicked_on(point):
                                if i == 0:
                                    self._reset()
                                else:
                                    showing_stats = True
                    else:
                        if not self.high_scores_button.clicked_on(point):
                            showing_stats = False


            point = pygame.mouse.get_pos()

            self.buttons.update(point)
            self.screen.fill(Game.BGCOLOR)

            self.screen.blit(self.title_text,self.title_text_rect)
            self.screen.blit(self.instructions_text,self.instructions_text_rect)
            self.screen.blit(self.move_text,self.move_text_rect)


            for color_picker in self.color_pickers:
                color_picker.draw(self.screen,point)
            
            self.buttons.draw(self.screen)
            self.board.draw(self.screen)

            if self.game_over:
                self.screen.blit(self.game_over_surface,(self.screen_width//2 - self.game_over_surface.get_width()//2,self.screen_height//2 - self.game_over_surface.get_height()//2))

            if showing_stats:
                self.screen.blit(self.high_scores_surface,self.high_scores_surface_rect)



            pygame.display.update() 

if __name__ == "__main__":
    

    Game()
