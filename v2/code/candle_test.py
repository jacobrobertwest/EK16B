import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
pygame.display.set_caption("Flickering Candle")

# Load or create the flame image
flame_image = pygame.Surface((50, 100), pygame.SRCALPHA)
pygame.draw.ellipse(flame_image, (255, 200, 100), [10, 0, 30, 60])
pygame.draw.ellipse(flame_image, (255, 255, 150), [15, 10, 20, 50])

screen.blit(flame_image, (175, 150))

# Create the mask from the flame image
flame_mask = pygame.mask.from_surface(flame_image)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Flicker effect: randomly adjust the brightness and/or shape
    flicker_intensity = random.uniform(0.6, 1)
    flicker_offset = random.randint(-2, 2)
    print(f"{flicker_intensity}, {flicker_offset}")

    # Adjust the flame's position slightly
    offset_flame_image = pygame.transform.scale(
        flame_image,
        (int(50 + flicker_offset), int(100 + flicker_offset))
    )

    # Apply the flicker effect by blending the flame with different brightness
    flickered_flame = offset_flame_image.copy()
    rgba = (int(flicker_intensity * 255), int(flicker_intensity * 200), int(flicker_intensity * 100),255)
    flickered_flame.fill(rgba, special_flags=pygame.BLEND_RGBA_MULT)
    print(rgba)
    # Clear the screen and draw the flickering flame
    screen.fill((0, 0, 0))
    screen.blit(flickered_flame, (175, 150))

    # Update the display
    pygame.display.update()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
