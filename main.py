# ------------------- Difficulty -------------------
difficulty = input("Select difficulty (E=Easy, M=Medium, H=Hard, R=Random): ").strip().upper()
if difficulty == "R":
    import random
    difficulty = random.choice(["E", "M", "H"])

if difficulty == "E":
    num_balloons = 10
elif difficulty == "M":
    num_balloons = 20
elif difficulty == "H":
    num_balloons = 30
else:
    print(f"Invalid input '{difficulty}', defaulting to Medium")
    num_balloons = 20

# ------------------- Imports -------------------
import pygame
import random
import time
from balloon_design import Balloon
from dart_design import Dart
# ------------------- Pygame Setup -------------------
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GAME_DURATION = 30  # seconds

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Balloon Popper Game")
pygame.key.set_repeat(1, 30)

FPS = 60
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ------------------- Load & Scale Balloon Images -------------------
balloon_images = [
    pygame.image.load("balloon1.png"),
    pygame.image.load("balloon2.png"),
    pygame.image.load("balloon3.png"),
    pygame.image.load("balloon4.png")
]
balloon_new_size=(40,60)
balloon_images = [pygame.transform.scale(img, balloon_new_size) for img in balloon_images]

# ------------------- Load Sounds -------------------
sound_balloon_pop = pygame.mixer.Sound("balloon_pop_sound.mp3")
sound_background = pygame.mixer.Sound("balloon_popper_bgmusic.mp3")
sound_gamewin = pygame.mixer.Sound("gamewin_sound_balloon_game.mp3")
sound_gameover = pygame.mixer.Sound("game_over_sound_balloon_game.mp3")
sound_background.play(-1)

# ------------------- Groups -------------------
dart_group = pygame.sprite.Group()
balloons_group = pygame.sprite.Group()

dart = Dart(WINDOW_WIDTH, WINDOW_HEIGHT)
dart_group.add(dart)

# ------------------- Game variables -------------------
running = True
gameover = False
gamewin = False
score = 0
next_image_index = 0
start_time = time.time()


# ------------------- Spawn all balloons at start -------------------
for number_of_bulloons in range(num_balloons):
    balloons_group.add(Balloon(
        random.randint(20, WINDOW_WIDTH-20),
        random.randint(50, WINDOW_HEIGHT-150),
        balloon_images[next_image_index],
        difficulty
    ))
    next_image_index += 1
    if next_image_index >= len(balloon_images):
        next_image_index = 0

# ------------------- Main Game Loop -------------------
while running:
    current_time = time.time()
    elapsed_time = current_time - start_time
    time_left = max(0, int(GAME_DURATION - elapsed_time))

    if time_left <= 0:
        gameover = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not gameover and not gamewin:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dart.is_shot:
                    dart.is_shot = True

    if not gameover and not gamewin:
        dart_group.update()
        balloons_group.update()

        # ------------------- Check collisions -------------------
        hit_balloons = pygame.sprite.spritecollide(dart, balloons_group, True)
        if hit_balloons:
            score += 10
            sound_balloon_pop.play()

        # ------------------- Check if any balloon escaped -------------------
        for balloon in balloons_group:
            if balloon.rect.top > WINDOW_HEIGHT - 100:
                balloon.kill()
                lives -= 1
                if lives <= 0:
                    gameover = True

        # ------------------- Win condition -------------------
        if len(balloons_group) == 0:
            gamewin = True

    # ------------------- Draw -------------------
    screen.fill(BLACK)
    dart_group.draw(screen)
    balloons_group.draw(screen)

    pygame.draw.rect(screen, WHITE, (0, 0, WINDOW_WIDTH, 50))
    pygame.draw.rect(screen, WHITE, (0, WINDOW_HEIGHT - 100, WINDOW_WIDTH, 100))

    score_text = font.render(f"Score: {score}", True, BLACK)
    time_text = font.render(f"Time: {time_left}s", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (WINDOW_WIDTH - 120, 10))

    # ------------------- Game over / win screens -------------------
    if gameover:
        screen.fill(BLACK)
        defeat_text = font.render(f"GAME OVER! Your score: {score}", True, WHITE)
        defeat_text_rect = defeat_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(defeat_text, defeat_text_rect)
        pygame.display.update()
        sound_background.stop()
        sound_gameover.play()
        pygame.time.delay(2000)  # 2 seconds
        running = False
        pygame.quit()
        print("Run to play again")
        exit()

    if gamewin:
        screen.fill(BLACK)
        gamewin_text = font.render(f"YOU WIN! Your score: {score}", True, WHITE)
        gamewin_text_rect = gamewin_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(gamewin_text, gamewin_text_rect)
        pygame.display.update()
        sound_background.stop()
        sound_gamewin.play()
        pygame.time.delay(7000)  # 7 seconds
        running = False
        pygame.quit()
        print("Run to play again!")
        exit()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
