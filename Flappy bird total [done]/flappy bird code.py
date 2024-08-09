import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)  # Background color
SCORE_BOX_COLOR = (82, 127, 36)  # #527f24
BUTTON_COLOR = (34, 139, 34)  # Green color for the button
BUTTON_TEXT_COLOR = WHITE

# Paths to images
current_dir = os.path.dirname(__file__)
bird_img_path = os.path.join(current_dir, 'bird.png')
pipe_img_path = os.path.join(current_dir, 'pole.png')

# Load images
bird_img = pygame.image.load(bird_img_path)
pipe_img = pygame.image.load(pipe_img_path)

# Resize images
bird_img = pygame.transform.scale(bird_img, (60, 45))  # Increased size of the bird
pipe_img = pygame.transform.scale(pipe_img, (100, HEIGHT))  # Increased size of the pipe

# Bird properties
bird_x, bird_y = 50, HEIGHT // 2
bird_velocity = 0
gravity = 0.25  # Adjusted gravity
flap_strength = -5  # Adjusted flap strength

# Pipe properties
pipe_width = 100
pipe_gap = 200  # Increased gap size
pipe_velocity = -3  # Slowed down pipe speed
pipe_frequency = 2000  # Slower frequency for pipe generation
last_pipe = pygame.time.get_ticks() - pipe_frequency

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()

def draw_bird():
    screen.blit(bird_img, (bird_x, bird_y))

def draw_pipe(x, y):
    screen.blit(pipe_img, (x, 0), (0, 0, pipe_width, y))  # Top pipe
    screen.blit(pipe_img, (x, y + pipe_gap), (0, 0, pipe_width, HEIGHT - y - pipe_gap))  # Bottom pipe

def draw_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    score_rect = pygame.Rect(10, 10, score_text.get_width() + 20, score_text.get_height() + 10)
    pygame.draw.rect(screen, SCORE_BOX_COLOR, score_rect)
    screen.blit(score_text, (score_rect.x + 10, score_rect.y + 5))

def draw_retry_button():
    button_width, button_height = 150, 50
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(button_x, button_y, button_width, button_height), border_radius=20)
    
    retry_text = font.render("Retry", True, BUTTON_TEXT_COLOR)
    screen.blit(retry_text, (button_x + (button_width - retry_text.get_width()) // 2, button_y + (button_height - retry_text.get_height()) // 2))

def show_game_over():
    screen.fill(BLUE)
    draw_retry_button()
    pygame.display.flip()

def main_game():
    global bird_x, bird_y, bird_velocity, score, pipes, last_pipe
    
    running = True
    pipes = []
    score = 0
    bird_x, bird_y = 50, HEIGHT // 2
    bird_velocity = 0
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = flap_strength
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    # Check if mouse click is within the button
                    button_width, button_height = 150, 50
                    button_x = (WIDTH - button_width) // 2
                    button_y = (HEIGHT - button_height) // 2
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        return True

        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Create new pipe
        current_time = pygame.time.get_ticks()
        if current_time - last_pipe > pipe_frequency:
            pipe_height = random.randint(150, HEIGHT - pipe_gap - 150)  # Adjust as needed
            pipes.append([WIDTH, pipe_height])
            last_pipe = current_time

        # Move pipes and check for collisions
        for pipe in pipes:
            pipe[0] += pipe_velocity
            if pipe[0] + pipe_width < 0:
                pipes.remove(pipe)
                score += 1
            if (bird_x + bird_img.get_width() > pipe[0] and bird_x < pipe[0] + pipe_width) and \
               (bird_y < pipe[1] or bird_y + bird_img.get_height() > pipe[1] + pipe_gap):
                running = False

        # Check for collisions with the ground or ceiling
        if bird_y + bird_img.get_height() > HEIGHT or bird_y < 0:
            running = False

        # Drawing
        screen.fill(BLUE)  # Draw background color
        draw_bird()
        for pipe in pipes:
            draw_pipe(pipe[0], pipe[1])
        draw_score()

        pygame.display.flip()
        clock.tick(30)

    show_game_over()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    # Check if mouse click is within the button
                    button_width, button_height = 150, 50
                    button_x = (WIDTH - button_width) // 2
                    button_y = (HEIGHT - button_height) // 2
                    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                        return True

if __name__ == "__main__":
    while main_game():
        pass
    pygame.quit()
