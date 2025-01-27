import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
MESSAGE_HEIGHT = 100  # Space for the funny messages
GAME_HEIGHT = HEIGHT - MESSAGE_HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse Snake Game: Dodge the Blocks")

# Colors
STAGE_COLORS = [(0, 0, 0), (50, 50, 50), (100, 100, 100)]  # Background colors for stages
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Snake properties
snake = [pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2, 20, 20),
         pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2 + 20, 20, 20),
         pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2 + 40, 20, 20)]  # Initial length 3
snake_speed = 20
snake_direction = "UP"

# Blocks
blocks = []
new_block_timer = 0
block_display_time = 2000  # Blocks disappear after 2 seconds
block_spawn_time = 2000  # Blocks spawn every 2 seconds
falling_blocks = False

# Stages
stage = 1
stage_start_time = time.time()
stage_duration = {1: 15, 2: 10, 3: float('inf')}  # Stage durations in seconds

# Score and Timer
start_time = time.time()
score = 0
length_timer = time.time()
message_start_time = time.time()

# Witty messages
funny_messages = [
    "Oh great, another block!",
    "Seriously? Where did that come from?",
    "You call this fair?!",
    "I'm starting to feel cornered here!",
    "Can we just stop this madness?",
    "Another one? Really?",
    "I'm gonna need a miracle!",
    "Blocks everywhere! HELP!",
    "Is this a joke to you?",
    "Game over is calling my name..."
]
current_message = ""
message_timer = 0
message_display_time = 2000  # 2 seconds

# Game loop variables
running = True
clock = pygame.time.Clock()
restart_flag = False

# Function to spawn multiple blocks with random increment
def spawn_blocks():
    num_blocks = random.randint(1, 15)  # Randomize number of blocks (1 to 15)
    for _ in range(num_blocks):
        x = random.randint(0, WIDTH - 20)
        y = random.randint(MESSAGE_HEIGHT, GAME_HEIGHT - 20)
        blocks.append((pygame.Rect(x, y, 20, 20), pygame.time.get_ticks()))

# Function to display a message
def display_message():
    global current_message, message_timer
    current_message = random.choice(funny_messages)
    message_timer = pygame.time.get_ticks()

# Function to restart the game
def restart_game():
    global snake, blocks, new_block_timer, start_time, score, length_timer, message_start_time, running, restart_flag, snake_direction, stage, stage_start_time, falling_blocks
    snake = [pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2, 20, 20),
             pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2 + 20, 20, 20),
             pygame.Rect(WIDTH // 2, GAME_HEIGHT // 2 + 40, 20, 20)]  # Reset snake
    blocks = []
    new_block_timer = 0
    start_time = time.time()
    score = 0
    length_timer = time.time()
    message_start_time = time.time()
    snake_direction = "UP"
    stage = 1
    stage_start_time = time.time()
    falling_blocks = False
    restart_flag = True

# Function to display game over screen
def game_over_text():
    global score
    game_over_msg = large_font.render("Game Over", True, WHITE)
    score_msg = font.render(f"Final Score: {score}", True, WHITE)
    restart_msg = font.render("Press any key to restart", True, WHITE)

    # Centering the text
    game_over_rect = game_over_msg.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    score_rect = score_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_msg.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3))

    # Display the game over screen
    screen.fill(BLACK)
    screen.blit(game_over_msg, game_over_rect)
    screen.blit(score_msg, score_rect)
    screen.blit(restart_msg, restart_rect)

    pygame.display.flip()

# Main game loop
while True:
    if restart_flag:
        running = True
        restart_flag = False

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Handle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_direction != "DOWN":
            snake_direction = "UP"
        if keys[pygame.K_DOWN] and snake_direction != "UP":
            snake_direction = "DOWN"
        if keys[pygame.K_LEFT] and snake_direction != "RIGHT":
            snake_direction = "LEFT"
        if keys[pygame.K_RIGHT] and snake_direction != "LEFT":
            snake_direction = "RIGHT"

        # Move snake
        head = snake[0].copy()
        if snake_direction == "UP":
            head.y -= snake_speed
        if snake_direction == "DOWN":
            head.y += snake_speed
        if snake_direction == "LEFT":
            head.x -= snake_speed
        if snake_direction == "RIGHT":
            head.x += snake_speed

        # Wrap around the screen
        if head.left < 0:
            head.right = WIDTH  # Wrap around to the right
        elif head.right > WIDTH:
            head.left = 0  # Wrap around to the left
        if head.top < MESSAGE_HEIGHT:
            head.bottom = HEIGHT  # Wrap around to the bottom
        elif head.bottom > HEIGHT:
            head.top = MESSAGE_HEIGHT  # Wrap around to the top

        snake = [head] + snake[:-1]  # Move snake by adding a new head and removing the tail

        # Manage stages
        elapsed_stage_time = time.time() - stage_start_time
        if stage == 1 and elapsed_stage_time > stage_duration[1]:
            stage = 2
            stage_start_time = time.time()
            falling_blocks = False
        elif stage == 2 and elapsed_stage_time > stage_duration[2]:
            stage = 3
            stage_start_time = time.time()
            falling_blocks = False

        # Stage 2: Blocks fall straight down
        if stage == 2 and elapsed_stage_time > 5:
            falling_blocks = True

        # Stage 3: Blocks fall diagonally (right to left)
        if stage == 3 and elapsed_stage_time > 5:
            falling_blocks = True

        # Spawn new blocks every 2 seconds
        current_time = pygame.time.get_ticks()
        if current_time - new_block_timer > block_spawn_time:
            spawn_blocks()
            if time.time() - start_time >= 2:  # Start messages after 2 seconds
                display_message()
            new_block_timer = current_time

        # Update blocks based on stage behavior
        updated_blocks = []
        for block, spawn_time in blocks:
            if falling_blocks:
                if stage == 2:
                    block.y += 10  # Blocks fall straight down
                elif stage == 3:
                    block.y += 10  # Blocks fall diagonally
                    block.x -= 5
            if block.top < HEIGHT and block.right > 0:  # Keep blocks within screen
                updated_blocks.append((block, spawn_time))
        blocks = updated_blocks

        # Check collision with blocks
        for block, _ in blocks:
            if head.colliderect(block):
                running = False

        # Increment score every 2 seconds based on stage
        if time.time() - length_timer >= 2:
            length_timer = time.time()
            if stage == 1:
                score += 2  # Stage 1: +2 points every 2 seconds
            elif stage == 2:
                score += 5  # Stage 2: +5 points every 2 seconds
            elif stage == 3:
                score += 10  # Stage 3: +10 points every 2 seconds

        # Draw everything
        screen.fill(STAGE_COLORS[stage - 1])

        # Draw funny message section
        pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, MESSAGE_HEIGHT))
        if current_message and current_time - message_timer < message_display_time:
            message_text = large_font.render(current_message, True, WHITE)
            text_rect = message_text.get_rect(center=(WIDTH // 2, MESSAGE_HEIGHT // 2))
            screen.blit(message_text, text_rect)

        # Draw game area
        pygame.draw.rect(screen, STAGE_COLORS[stage - 1], (0, MESSAGE_HEIGHT, WIDTH, GAME_HEIGHT))

        # Draw snake
        for i, segment in enumerate(snake):
            color = GREEN if i == 0 else BLUE  # Head is green, body is blue
            pygame.draw.ellipse(screen, color, segment)

        # Draw blocks
        for block, _ in blocks:
            pygame.draw.rect(screen, RED, block)

        # Draw score and stage
        score_text = font.render(f"Score: {score}", True, WHITE)
        stage_text = font.render(f"Stage: {stage}", True, WHITE)
        screen.blit(score_text, (10, MESSAGE_HEIGHT + 10))
        screen.blit(stage_text, (WIDTH - 150, MESSAGE_HEIGHT + 10))

        pygame.display.flip()
        clock.tick(10)

    # Game over screen
    while True:
        game_over_text()
        keys = pygame.key.get_pressed()
        if any(keys):  # If any key is pressed, restart the game
            restart_game()
            break
