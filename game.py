import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Red Rectangle Shooter")

# Colors
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Initial rectangle position
rect_x, rect_y = width // 2 - 25, height - 50
rect_width, rect_height = 50, 50
rect_speed = 5

# Initial shooter position
shooter_width, shooter_height = 10, 20
shooter_speed = 10

# Blue rectangle position
blue_rect_x, blue_rect_y = width // 2 - 25, 0
blue_rect_width, blue_rect_height = 50, 50
blue_rect_speed = 5

bullets = []

blue_rect_hit = False  # Flag to track if the blue rectangle has been hit
red_rect_hit = False # Flag to track if the red rectangle has been hit
red_wins_message = False  # Flag to track if the "Red Wins" message has been displayed

# Fonts
font = pygame.font.Font(None, 74)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not blue_rect_hit:  # Allow shooting only if the blue rectangle has not been hit
                    shot_x = rect_x + rect_width // 2 - shooter_width // 2
                    shot_y = rect_y - 20
                    bullets.append((shot_x, shot_y))
            if event.key == pygame.K_q:
                if not red_rect_hit:  # Allow shooting only if the blue rectangle has not been hit
                    shot_x = blue_rect_x + blue_rect_width // 2 - shooter_width // 2
                    shot_y = blue_rect_y + blue_rect_height
                    bullets.append((shot_x, shot_y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and rect_x > 0:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT] and rect_x < width - rect_width:
        rect_x += rect_speed
    if keys[pygame.K_UP] and rect_y > 0:
        rect_y -= rect_speed
    if keys[pygame.K_DOWN] and rect_y < height - rect_height:
        rect_y += rect_speed
    if keys[pygame.K_a] and blue_rect_x > 0:
        blue_rect_x -= blue_rect_speed
    if keys[pygame.K_d] and blue_rect_x < width - blue_rect_width:
        blue_rect_x += blue_rect_speed
    if keys[pygame.K_w] and blue_rect_y > 0:
        blue_rect_y -= blue_rect_speed
    if keys[pygame.K_s] and blue_rect_y < height - blue_rect_height:
        blue_rect_y += blue_rect_speed


    # Update bullets positions
    for i in range(len(bullets)):
        bullets[i] = (bullets[i][0], bullets[i][1] - shooter_speed)

    # Remove bullets that are out of the screen
    bullets = [(x, y) for x, y in bullets if y > 0]

    # Check for collision with blue rectangle
    for bullet in bullets.copy():
        bullet_x, bullet_y = bullet
        if (
            not blue_rect_hit
            and not red_rect_hit
            and bullet_x < blue_rect_x + blue_rect_width
            and bullet_x + shooter_width > blue_rect_x
            and bullet_y < blue_rect_y + blue_rect_height
            and bullet_y + shooter_height > blue_rect_y
        ):
            bullets.remove(bullet)
            blue_rect_hit = True
            red_wins_message = False

    # Draw everything
    screen.fill(black)
    
    # Draw blue rectangle only if it's not hit
    if not blue_rect_hit:
        pygame.draw.rect(screen, blue, (blue_rect_x, blue_rect_y, blue_rect_width, blue_rect_height))
    
    pygame.draw.rect(screen, red, (rect_x, rect_y, rect_width, rect_height))

    for bullet in bullets:
        pygame.draw.rect(screen, white, (bullet[0], bullet[1], shooter_width, shooter_height))

    # Display "Red Wins" message if blue rectangle is hit
    if blue_rect_hit and not red_wins_message:
        red_wins_text = font.render("Red Wins", True, white)
        screen.blit(red_wins_text, (width // 2 - red_wins_text.get_width() // 2, height // 2 - red_wins_text.get_height() // 2))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # Reset the game or perform any desired action when space is pressed
            blue_rect_hit = False
            red_wins_message = True
            bullets = []

    pygame.display.flip()

    pygame.time.Clock().tick(60)
