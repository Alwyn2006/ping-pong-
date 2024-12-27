import pygame
import random

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_SPEED = 10  # Increased speed of paddles

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

# Paddle and Ball positions
paddle1 = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Ball speed variables
ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]
ball_speed_increment = 0.5  # Speed increment after each score

# Scores
score1, score2 = 0, 0
font = pygame.font.SysFont('Arial', 36)

# Function to display the score
def display_score():
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))

# Function to reset the ball and increase speed
def reset_ball(winner):
    global ball_speed
    ball.x, ball.y = WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2
    ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]
    if winner == "player1":
        global score1
        score1 += 1
    else:
        global score2
        score2 += 1
    # Increase ball speed after each point
    ball_speed[0] *= (1 + ball_speed_increment)
    ball_speed[1] *= (1 + ball_speed_increment)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle1.top > 0: paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT: paddle1.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle2.top > 0: paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT: paddle2.y += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT: ball_speed[1] = -ball_speed[1]

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2): ball_speed[0] = -ball_speed[0]

    # Ball out of bounds (scoring)
    if ball.left <= 0:
        reset_ball("player2")
    if ball.right >= WIDTH:
        reset_ball("player1")

    # Drawing everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    display_score()

    # Check for win condition
    if score1 >= 5 or score2 >= 5:
        winner_text = "Player 1 Wins!" if score1 >= 5 else "Player 2 Wins!"
        winner_surface = font.render(winner_text, True, WHITE)
        screen.blit(winner_surface, (WIDTH//2 - winner_surface.get_width()//2, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        score1, score2 = 0, 0  # Reset the game
        pygame.time.delay(500)
    
    pygame.display.update()
    clock.tick(FPS)
    