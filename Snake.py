import pygame
from pygame.math import Vector2
import random
import os 

from menu import show_menu

pygame.init()
pygame.mixer.init()


WIDTH=720
HEIGHT=480 

SNAKE_BODY = pygame.transform.scale(pygame.image.load(
    r"C:\Users\Dayana Castro\Downloads\Images\snakebody.png"), (20, 20))

APPLE = pygame.transform.scale(pygame.image.load(
    r"C:\Users\Dayana Castro\Downloads\Images\manzana.png"), (20, 20))

SNAKE_HEAD = []
for x in range(1, 5):
    SNAKE_HEAD.append(pygame.transform.scale(
        pygame.image.load(rf"C:\Users\Dayana Castro\Downloads\Images\SnakeHead{x}.png"), (20, 20)))


EAT_SOUND = pygame.mixer.Sound(r"C:\Users\Dayana Castro\Downloads\Images\coin.wav")




WIN=pygame.display.set_mode((WIDTH, HEIGHT))
SCORE_TEXT=pygame.font.SysFont("Russo One", 15)


class Snake:
  def __init__(self):
    start_x = WIDTH // 2
    start_y = HEIGHT // 2
    self.body = [
        Vector2(start_x, start_y),
        Vector2(start_x, start_y + 20),
        Vector2(start_x, start_y + 40)
    ]
    self.direction = Vector2(0, -20)
    self.add = False

        
  def draw(self):
    for block in self.body[1:]:  # Dibuja SOLO el cuerpo, no la cabeza
        WIN.blit(SNAKE_BODY, (block.x, block.y))  

    # Dibuja la cabeza según dirección
    if self.direction == Vector2(0, -20):
        WIN.blit(SNAKE_HEAD[0], (self.body[0].x, self.body[0].y))  # Arriba
    elif self.direction == Vector2(0, 20):
        WIN.blit(SNAKE_HEAD[2], (self.body[0].x, self.body[0].y))  # Abajo
    elif self.direction == Vector2(20, 0):
        WIN.blit(SNAKE_HEAD[1], (self.body[0].x, self.body[0].y))  # Derecha
    elif self.direction == Vector2(-20, 0):
        WIN.blit(SNAKE_HEAD[3], (self.body[0].x, self.body[0].y))  # Izquierda

                              
  def move(self):
   if self.add:
            body_copy = self.body[:]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy
            self.add = False
   else:
            body_copy = self.body[:-1]
            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy
  
  def move_up(self):
    self.direction = Vector2(0, -20)

  def move_down(self):
    self.direction = Vector2(0, 20)

  def move_right(self):
    self.direction = Vector2(20, 0)

  def move_left(self):
    self.direction = Vector2(-20, 0)

  
  def die(self):
    if (self.body[0].x < 0 or self.body[0].x >= WIDTH or
        self.body[0].y < 0 or self.body[0].y >= HEIGHT):
        return True
    for i in self.body[1:]:
        if self.body[0] == i:
            return True
    return False

      
class Apple:
    def __init__(self):
        self.pos = Vector2(0, 0)

    def draw(self):
        WIN.blit(APPLE, (self.pos.x, self.pos.y))

    def generate(self, snake):
        while True:
            self.x = random.randint(0, WIDTH // 20 - 1)
            self.y = random.randint(0, HEIGHT // 20 - 1)
            self.pos = Vector2(self.x * 20, self.y * 20)
            if self.pos not in snake.body:
                break

    def check_collision(self, snake):
        if snake.body[0] == self.pos:
            self.generate(snake)
            snake.add = True
            return True
        for block in snake.body[1:]:
            if self.pos == block:
                self.generate(snake)
        return False


          

def main():
    # 👇 Mostrar menú y guardar dificultad elegida
    nivel = show_menu()

    # 👇 Configurar fondo y velocidad según el nivel
    if nivel == "Easy":
        bg_color = (175, 215, 70)
        speed = 8
    elif nivel == "Intermediate":
        bg_color = (70, 130, 180)
        speed = 12
    else:  # difícil
        bg_color = (139, 0, 0)
        speed = 18

    
    snake = Snake()
    apple = Apple()
    apple.generate(snake)
    score=0
    clock = pygame.time.Clock()

    while True:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != Vector2(0, 20):
                    snake.move_up()
                elif event.key == pygame.K_DOWN and snake.direction != Vector2(0, -20):
                    snake.move_down()
                elif event.key == pygame.K_RIGHT and snake.direction != Vector2(-20, 0):
                    snake.move_right()
                elif event.key == pygame.K_LEFT and snake.direction != Vector2(20, 0):
                    snake.move_left()

        snake.move()

        if apple.check_collision(snake):
            score += 1
            EAT_SOUND.play()

        WIN.fill(bg_color)
        snake.draw()
        apple.draw()
        text = SCORE_TEXT.render(f"Score: {score}", True, (255, 255, 255))
        WIN.blit(text, (WIDTH - text.get_width() - 20, 20))

        if snake.die():
         print("🐍 Game Over: la serpiente murió.")
         pygame.time.wait(2000)  # Espera 2 segundos
         main()  # 👈 Esto vuelve a empezar desde el menú
         return
 
        pygame.display.update()  # <- Final del bucle


if __name__ == "__main__":
    main()
