import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 1800, 900

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Falling Biscrok with Fried Image")

# Set up colors
MINT_GREEN = (152, 251, 152)  # Soft mint green
BLACK = (0, 0, 0)

# Falling object properties
object_size = 50  # Size of the Biscrok image
gravity = 0.2  # Gravity constant

# Score counter
score = 0

# Font for score display
font = pygame.font.SysFont("Arial", 80)  # Larger font for score

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load images
biscrok_img = pygame.image.load("biscrok.png")
biscrok_img = pygame.transform.scale(biscrok_img, (object_size, object_size))  # Scale the Biscrok image

fried_img_original = pygame.image.load("fried.png")  # Load the original high-res image
fried_size = 60  # Initial size of the fried image


def create_object():
    """Create a new falling object with random properties."""
    angle = random.uniform(0, 360)  # Initial rotation angle
    angular_speed = random.uniform(-5, 5)  # Rotation speed
    x = random.randint(0, WIDTH - object_size)  # Initial x position
    y = 0  # Start at the top
    vx = random.uniform(-2, 2)  # Horizontal speed
    vy = random.uniform(2, 5)  # Initial vertical speed
    return {"x": x, "y": y, "vx": vx, "vy": vy, "angle": angle, "angular_speed": angular_speed}


# Main game loop
def main():
    global fried_size, score

    # Initialize falling objects list
    falling_objects = []

    # Fried position
    fried_x, fried_y = WIDTH // 2, HEIGHT // 2
    fried_speed = 10

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit game
                    running = False

        # Get key states for fried movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            fried_y -= fried_speed
        if keys[pygame.K_DOWN]:
            fried_y += fried_speed
        if keys[pygame.K_LEFT]:
            fried_x -= fried_speed
        if keys[pygame.K_RIGHT]:
            fried_x += fried_speed

        # Prevent fried from moving off the screen
        fried_x = max(0 + fried_size // 2, min(WIDTH - fried_size // 2, fried_x))
        fried_y = max(0 + fried_size // 2, min(HEIGHT - fried_size // 2, fried_y))

        # Add new objects randomly
        if random.randint(1, 20) == 1:
            falling_objects.append(create_object())

        # Update falling objects
        for obj in falling_objects:
            obj["x"] += obj["vx"]
            obj["y"] += obj["vy"]
            obj["vy"] += gravity  # Apply gravity
            obj["angle"] += obj["angular_speed"]

        # Check for collisions with fried
        for obj in falling_objects[:]:
            obj_center_x = obj["x"] + object_size // 2
            obj_center_y = obj["y"] + object_size // 2
            distance_x = abs(fried_x - obj_center_x)
            distance_y = abs(fried_y - obj_center_y)
            if distance_x < fried_size // 2 + object_size // 2 and distance_y < fried_size // 2 + object_size // 2:
                falling_objects.remove(obj)
                score += 1
                fried_size += 5  # Make fried grow

        # Remove objects that fall off the screen
        falling_objects = [obj for obj in falling_objects if obj["y"] < HEIGHT]

        # Draw everything
        screen.fill(MINT_GREEN)

        # Draw the fried image (rescale for every frame)
        fried_img = pygame.transform.smoothscale(fried_img_original, (fried_size, fried_size))
        fried_rect = fried_img.get_rect(center=(fried_x, fried_y))
        screen.blit(fried_img, fried_rect.topleft)

        # Draw falling objects with rotation
        for obj in falling_objects:
            rotated_image = pygame.transform.rotate(biscrok_img, obj["angle"])
            rect = rotated_image.get_rect(center=(obj["x"] + object_size // 2, obj["y"] + object_size // 2))
            screen.blit(rotated_image, rect.topleft)

        # Display score
        score_text = font.render(f"{score}", True, BLACK)  # Only the number, in black
        score_rect = score_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))  # Position at bottom-right
        screen.blit(score_text, score_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
