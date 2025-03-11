import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Load sound effects using pygame.mixer.music for MP3
def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

# Basket properties
basket_width, basket_height = 100, 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - 50
basket_speed = 8

# Object properties
obj_width, obj_height = 20, 20
obj_speed = 5

# Object lists
good_objects = []
bad_objects = []
powerups = []

# Score and Lives
score = 0
lives = 3
level = 1
high_score = 0
font = pygame.font.Font(None, 36)

# Load high score from file
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())

def spawn_objects():
    if random.random() < 0.6:  # 60% chance for a good object
        good_objects.append([random.randint(0, WIDTH - obj_width), 0])
    bad_object_chance = max(0.1, 0.3 - (score // 10) * 0.05)  # Reduces chance with score increase
    if random.random() < bad_object_chance:
         bad_objects.append([random.randint(0, WIDTH - obj_width), 0])
    if random.random() < 0.1:  # 10% chance for a power-up
        powerups.append([random.randint(0, WIDTH - obj_width), 0])

# Game loop
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get key states
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Spawn objects
    spawn_objects()

    # Move objects
    for obj in good_objects:
        obj[1] += obj_speed
    for obj in bad_objects:
        obj[1] += obj_speed + 2
    for obj in powerups:
        obj[1] += obj_speed - 2
    
    # Check collisions
    for obj in good_objects[:]:
        if obj[1] + obj_height >= basket_y and basket_x < obj[0] < basket_x + basket_width:
            score += 1
            play_sound("C:\\Users\\veda\\Music\\catch.mp3")  # Escape backslashes
            good_objects.remove(obj)
    
    for obj in bad_objects[:]:
        if obj[1] + obj_height >= basket_y and basket_x < obj[0] < basket_x + basket_width:
            lives -= 1
            play_sound("C:\\Users\\veda\\Music\\miss.mp3")  # Escape backslashes
            bad_objects.remove(obj)
    
    for obj in powerups[:]:
        if obj[1] + obj_height >= basket_y and basket_x < obj[0] < basket_x + basket_width:
            lives += 1
            play_sound("C:\\Users\\veda\\Music\\powerup.mp3")  # Escape backslashes
            powerups.remove(obj)
    
    # Remove off-screen objects
    good_objects = [obj for obj in good_objects if obj[1] < HEIGHT]
    bad_objects = [obj for obj in bad_objects if obj[1] < HEIGHT]
    powerups = [obj for obj in powerups if obj[1] < HEIGHT]

    # Increase difficulty
    if score % 5 == 0 and score > 0:
        level += 1
        obj_speed += 0.2
    
    # Draw basket
    pygame.draw.rect(screen, BLUE, (basket_x, basket_y, basket_width, basket_height))
    
    # Draw objects
    for obj in good_objects:
        pygame.draw.rect(screen, GREEN, (obj[0], obj[1], obj_width, obj_height))
    for obj in bad_objects:
        pygame.draw.rect(screen, RED, (obj[0], obj[1], obj_width, obj_height))
    for obj in powerups:
        pygame.draw.rect(screen, YELLOW, (obj[0], obj[1], obj_width, obj_height))
    
    # Display score and lives
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (10, 70))
    screen.blit(high_score_text, (10, 100))

    # Check for game over
    if lives <= 0:
        if score > high_score:
            high_score = score
            with open("highscore.txt", "w") as f:
                f.write(str(high_score))
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    pygame.display.update()
    pygame.time.delay(30)  # Control frame rate

pygame.quit()
