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

# Auto-Klasse
class Car:
    def __init__(self, x, y, width=50, height=30, color=(0, 0, 255), speed=5):
        """Initialisiert das Auto mit Position, Größe, Farbe und Geschwindigkeit."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self):
        """Bewegt das Auto nach rechts. Wenn es den Bildschirm verlässt, startet es neu."""
        self.x += self.speed
        if self.x > c.SCREEN_WIDTH:
            self.x = -self.width  # Auto erscheint auf der linken Seite wieder

    def draw(self, screen):
        """Zeichnet das Auto auf dem Bildschirm."""
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))



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

    # Bildschirm aktualisieren
    pygame.display.update()

    # Framerate begrenzen
    clock.tick(60)

pygame.quit()