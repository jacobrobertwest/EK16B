import pygame
import random
import math
import colorsys

index = [0, 0, 0]
text_color = (255, 255, 255)
background_color = (0, 0, 0)


def init_polygon(width, height, n):
    delta_angle = 360 / n
    r = width / 2 - 10
    polygon = []

    for i in range(0, n):
        angle = (180 + i * delta_angle) * math.pi / 180
        color = colorsys.hsv_to_rgb((i * delta_angle) / 360, 0.8, 1)
        polygon.append(((width / 2 + r * math.sin(angle),
                         height / 2 + r * math.cos(angle)),
                        (int(255), int(255), int(255))))
    return polygon


def random_point_index(mode, polygon):
    global index

    # Random corner point selection
    if mode == 0:
        index[0] = random.randint(0, len(polygon) - 1)

    # Cornerpoints cannot be chosen twice in a row
    elif mode == 1:
        index[2] = index[1]
        index[1] = index[0]
        dst1 = abs(index[1] - index[2])

        while True:
            index[0] = random.randint(0, len(polygon) - 1)
            dst = abs(index[0] - index[1])
            if dst1 != 0 and dst == 0:
                continue
            else:
                break

    # If a cornerpoint is chosen twice, the next selected point must not be a direct neighbor.
    elif mode == 2:
        index[2] = index[1]
        index[1] = index[0]
        dst1 = abs(index[1] - index[2])

        while True:
            index[0] = random.randint(0, len(polygon) - 1)
            dst = abs(index[0] - index[1])
            if dst1 == 0 and (dst == 1 or dst == len(polygon) - 1):
                continue
            else:
                break

    return index[0]


def mark_pixel(surface, position, pixel_color):
    color = surface.get_at(position)
    surface.set_at(position, (min(color[0] + pixel_color[0] / 10, 255),
                              min(color[1] + pixel_color[1] / 10, 255),
                              min(color[2] + pixel_color[2] / 10, 255)))


def main(mode, width, height, n, r):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill(background_color)
    pygame.display.set_caption('Chaos Game')

    run = True

    if mode > 2:
        print("Not defined mode")
        run = False
        pygame.quit()

    polygon = init_polygon(width, height, n)
    step = 1

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        x, y = (0, 0)
        for i in range(0, width * height):
            i = random_point_index(mode, polygon)
            x += (polygon[i][0][0] - x) * r
            y += (polygon[i][0][1] - y) * r

            mark_pixel(screen, (int(x), int(y)), polygon[i][1])
            step += 1
            font = pygame.font.Font(None, 24)
            text = font.render("%d " % (step), True, text_color, background_color)
            screen.blit(text, (10, 10))
            pygame.display.update()


if __name__ == "__main__":
# Random cornerpoint selection
    main(0, 300, 300, 3, 0.5)
