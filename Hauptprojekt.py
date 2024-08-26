import pygame
import constants as c
import time

pygame.init()

clock = pygame.time.Clock()

# Bildschirm und Farben einrichten
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
Backcolour = pygame.color.Color('#31a342')
pygame.display.set_caption('Ampelsimulation')

Strasse = pygame.image.load("Strasse.png")

# Ampelposition und Farben
ampel_pos = (200, 300)
colors = {
    "green": pygame.color.Color('green'),
    "yellow": pygame.color.Color('yellow'),
    "red": pygame.color.Color('red')
}

# Ampelzustand und Timer
ampel_state = "green"
last_switch_time = time.time()

# Funktion zum Zeichnen der Ampel
def draw_traffic_light(screen, color, position):
    pygame.draw.rect(screen, pygame.color.Color('black'), (*position, 14, 50))  # Hintergrund für Ampel
    if color == "red":
        pygame.draw.circle(screen, colors['red'], (position[0] + 7, position[1] + 15), 5)
    elif color == "yellow":
        pygame.draw.circle(screen, colors['yellow'], (position[0] + 7, position[1] + 30), 5)
    elif color == "green":
        pygame.draw.circle(screen, colors['green'], (position[0] + 7, position[1] + 45), 5)

# Hauptschleife
running = True
while running:
    # Ereignisschleife
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrundbild zeichnen
    screen.fill(Backcolour)
    screen.blit(Strasse, (0, 0))

    # Zeitberechnung
    current_time = time.time()
    elapsed_time = current_time - last_switch_time

    # Ampelzustand aktualisieren
    if ampel_state == "green" and elapsed_time >= 40:
        ampel_state = "yellow"
        last_switch_time = current_time
    elif ampel_state == "yellow" and elapsed_time >= 2:
        ampel_state = "red"
        last_switch_time = current_time
    elif ampel_state == "red" and elapsed_time >= 12:
        ampel_state = "green"
        last_switch_time = current_time

    # Ampel zeichnen
    draw_traffic_light(screen, ampel_state, ampel_pos)

    # Bildschirm aktualisieren
    pygame.display.update()

    # Framerate begrenzen
    clock.tick(60)

pygame.quit()