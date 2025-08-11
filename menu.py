import pygame 
import sys 


WIDTH=720
HEIGHT=480
WIN=pygame.display.set_mode((WIDTH,HEIGHT))


def show_menu():
    pygame.init()
    title_font=pygame.font.SysFont("Russo One", 50)
    button_font=pygame.font.SysFont("Russo One", 30)
    title_text=title_font.render("Snake Game", True,(255,255,255))
    
    button_texts=["Easy", "Intermediate", "Hard"]
    button_colors=[(100,200,100), (100,100,255),(200,50,50)]
    buttons=[]
    
    while True:
        WIN.fill((0,0,0))
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 80))
        buttons.clear()
        
        for i , text in enumerate(button_texts):
            btn_rect=pygame.Rect(WIDTH // 2 - 100, 180 + i * 80, 200 , 50)
            buttons.append(btn_rect)
            pygame.draw.rect(WIN, button_colors[i], btn_rect, border_radius=10)
            txt=button_font.render(text,True,(255,255,255))
            WIN.blit(txt, (btn_rect.x + 60 , btn_rect.y + 10))
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, rect in enumerate(buttons):
                    if rect.collidepoint((mx, my)):
                       return ["Easy", "Intermediate", "Hard"][i]

