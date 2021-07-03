import pygame,sys,random

pygame.init()



pygame.display.set_caption("FLOOD IT")

WHITE = (255,) * 3
BLACK = (0,) * 3

class Game:



    class Square(pygame.sprite.Sprite):

        def __init__(self,x,y,width,height,color):
            # x,y rperesent top-left x and y location of square
            super().__init__()
            self.color = color
            self.image = pygame.Surface((width,height))
            self.image.fill(color)
            self.rect = self.image.get_rect(topleft=(x,y))
            self.hovered_on = False
        




        
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
            


    BGCOLOR = (25,56,25)
    COLORS = [(0,150,200),(255,25,50),(125,200,0),(255,255,35),(150,0,150),(255,125,0)]
    
    title_font = pygame.font.SysFont("calibri",60,bold=True)
    text_font = pygame.font.SysFont("calibri",20)


    def __init__(self,screen_width=800,screen_height=800,rows=14,cols=14,edge_gap=20):
        self.edge_gap = edge_gap
        self.rows = rows
        self.cols = cols
        self.screen_height = screen_height
        self.title_text = self.title_font.render("Flood it",True,WHITE)
        self.instructions_text = self.text_font.render("Fill the entire board with the same color with 25 flood fills or less.",True,WHITE)


        self.board,self.screen_width = self._generate_board()
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        self.title_text_rect = self.title_text.get_rect(center=(self.screen_width//2,edge_gap + self.title_text.get_height()//2))
        self.instructions_text_rect = self.instructions_text.get_rect(center=(self.screen_width//2,edge_gap * 2 + self.title_text.get_height() + self.instructions_text.get_height()//2))
        self._generate_color_picker_squares()
        self._play()
    

    
    def _generate_board(self):


        
        topleft_y = 5 * self.edge_gap +60+ self.title_text.get_height()
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






    def _play(self):


        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            

            point = pygame.mouse.get_pos()
            self.screen.fill(Game.BGCOLOR)
            self.screen.blit(self.title_text,self.title_text_rect)
            self.screen.blit(self.instructions_text,self.instructions_text_rect)


            for color_picker in self.color_pickers:
                color_picker.draw(self.screen,point)
            

            self.board.draw(self.screen)

            pygame.display.update() 

if __name__ == "__main__":
    

    Game()