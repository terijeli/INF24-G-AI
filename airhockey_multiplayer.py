import pygame
import random
import sys

# Init
pygame.init()
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Airhockey")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Game state
x = WIDTH // 2
y = HEIGHT // 2
speedX = random.uniform(-3, 5)
speedY = random.uniform(-3, 5)
diam = 10
rectSize = 75
playerScore = 0
aiScore = 0

# Startpositioner og hastigheder for begge spillere
playerY = HEIGHT // 2
opponentY = HEIGHT // 2
paddleSpeed = 5

def reset():
    global x, y, speedX, speedY
    x = WIDTH // 2
    y = HEIGHT // 2
    speedX = random.uniform(-3, 5)
    speedY = random.uniform(-3, 5)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            reset()

    # Tastatur input
    keys = pygame.key.get_pressed()

    # Player 1 - Højre bat (piletaster)
    if keys[pygame.K_UP]:
        playerY -= paddleSpeed
    if keys[pygame.K_DOWN]:
        playerY += paddleSpeed
    playerY = max(rectSize // 2, min(HEIGHT - rectSize // 2, playerY))

    # Player 2 - Venstre bat (W/S)
    if keys[pygame.K_w]:
        opponentY -= paddleSpeed
    if keys[pygame.K_s]:
        opponentY += paddleSpeed
    opponentY = max(rectSize // 2, min(HEIGHT - rectSize // 2, opponentY))

    # Scoring
    if x < 0:
        playerScore += 1
        reset()
    if x > WIDTH:
        aiScore += 1
        reset()

    # Draw score
    score_text = f"{aiScore}  :  {playerScore}"
    text_surface = font.render(score_text, True, (0, 255, 0))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, 10))
    screen.blit(text_surface, text_rect)

    # Draw ball
    pygame.draw.ellipse(screen, (255, 255, 255), (x, y, diam, diam))

    # Draw bats
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 30, playerY - rectSize // 2, 10, rectSize))   # Spiller 1
    pygame.draw.rect(screen, (255, 255, 255), (20, opponentY - rectSize // 2, 10, rectSize))         # Spiller 2

    # Move ball
    x += speedX
    y += speedY

    # Player 1 paddle collision
    if WIDTH - 30 < x < WIDTH - 20 and playerY - rectSize / 2 < y < playerY + rectSize / 2:
        speedX *= -1

    # Player 2 paddle collision
    if 20 < x < 30 and opponentY - rectSize / 2 < y < opponentY + rectSize / 2:
        speedX *= -1

    # Bounce off ceiling/floor
    if y < 0 or y > HEIGHT:
        speedY *= -1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
