import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße und Farbeinstellungen
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Auto Bewegung")

# Farben
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Auto-Eigenschaften
car_width, car_height = 40, 20
car_x, car_y = 0, 290
car_speed = 2

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bildschirm füllen
    window.fill(WHITE)

    # Wenn das Auto die Koordinate (200, 300) erreicht, ändert es die Richtung nach links
    if car_x < 200:
        car_x += car_speed
    else:
        car_y -= car_speed

    # Zeichne das Auto (als Rechteck)
    pygame.draw.rect(window, BLUE, (car_x, car_y, car_width, car_height))

    # Bildschirm aktualisieren
    pygame.display.flip()

    # Frame-Rate einstellen
    pygame.time.Clock().tick(60)