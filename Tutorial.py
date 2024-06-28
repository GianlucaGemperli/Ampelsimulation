import pygame
import time

# Pygame initialisieren
pygame.init()

# Bildschirmabmessungen
width, height = 200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Ampel Auto Schenkon --> Städtli bzw. umgekehrt')

# Farben definieren
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Funktion, um einen Kreis zu zeichnen
def draw_circle(color, position):
    pygame.draw.circle(screen, color, position, 50)

# Hauptprogramm
def main():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Hintergrundfarbe
        screen.fill(BLACK)

        # Ampelkreise zeichnen
        draw_circle(RED, (width // 2, 100))
        draw_circle(YELLOW, (width // 2, 300))
        draw_circle(GREEN, (width // 2, 500))

        # Kreise ansteuern
        # Rot an
        draw_circle(RED, (width // 2, 100))
        pygame.display.update()
        time.sleep(3)

        # Gelb an
        draw_circle(BLACK, (width // 2, 100))  # Rot aus
        draw_circle(YELLOW, (width // 2, 300))  # Gelb an
        pygame.display.update()
        time.sleep(1)

        # Grün an
        draw_circle(BLACK, (width // 2, 300))  # Gelb aus
        draw_circle(GREEN, (width // 2, 500))  # Grün an
        pygame.display.update()
        time.sleep(3)

        # Gelb an
        draw_circle(BLACK, (width // 2, 500))  # Grün aus
        draw_circle(YELLOW, (width // 2, 300))  # Gelb an
        pygame.display.update()
        time.sleep(1)

        # Rot an (zurück zum Anfang)
        draw_circle(BLACK, (width // 2, 300))  # Gelb aus
        draw_circle(RED, (width // 2, 100))  # Rot an

        pygame.display.update()
        time.sleep(3)

    pygame.quit()

if __name__ == "__main__":
    main()