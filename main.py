import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BALL_SPEED = 4
PADDLE_SPEED = 7
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Casse-Brique")

# Classe pour la raquette
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 30))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += PADDLE_SPEED

# Classe pour la balle
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.vx = BALL_SPEED * random.choice((1, -1))
        self.vy = -BALL_SPEED

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Rebondir sur les murs
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.vx *= -1
        if self.rect.top <= 0:
            self.vy *= -1

        # Vérifier si la balle est tombée
        if self.rect.bottom >= HEIGHT:
            global game_over
            game_over = True

# Classe pour les briques
class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((75, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

# Fonction pour dessiner le score
def draw_score():
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    # Afficher le score en bas à gauche
    screen.blit(score_text, (10, HEIGHT - 30))

# Fonction pour afficher l'écran de fin de jeu
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = LARGE_FONT.render("Game Over", True, WHITE)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    restart_text = FONT.render("Press R to Restart", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))
    pygame.display.flip()

# Fonction pour redémarrer le jeu
def reset_game():
    global all_sprites, paddle, ball, bricks, score, game_over
    paddle = Paddle()
    ball = Ball()
    bricks = pygame.sprite.Group()
    for i in range(8):
        for j in range(5):
            brick = Brick(i * 100, j * 30)
            bricks.add(brick)
    all_sprites = pygame.sprite.Group(paddle, ball, *bricks)
    score = 0
    game_over = False

# Initialisation des objets et variables
game_over = False
reset_game()

# Boucle de jeu
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    if not game_over:
        all_sprites.update()
        
        # Collision balle/raquette
        if pygame.sprite.collide_rect(ball, paddle):
            ball.vy *= -1
        
        # Collision balle/briques
        hit_bricks = pygame.sprite.spritecollide(ball, bricks, True)
        if hit_bricks:
            ball.vy *= -1
            score += len(hit_bricks) * 10  # 10 points par brique détruite
        
        # Dessiner tout
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_score()
        pygame.display.flip()
    else:
        game_over_screen()

pygame.quit()
