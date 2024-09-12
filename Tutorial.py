import pygame

# Farben definieren
SCHWARZ = (0, 0, 0)
WEISS = (255, 255, 255)
GRÜN = (255, 255, 255)
BRAUN = (165, 42, 42)

# Fenster initialisieren
pygame.init()
fenster_breite = 800
fenster_hoehe = 600
fenster = pygame.display.set_mode((fenster_breite, fenster_hoehe))
pygame.display.set_caption("Meine schöne Straße")

# Hauptprogramm-Schleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrund füllen
    fenster.fill(GRÜN)  # Grüner Hintergrund für einen Wald

    # Straße zeichnen
    pygame.draw.rect(fenster, SCHWARZ, (50, 250, 700, 100))  # Straßenfläche

    # Fahrbahnmarkierungen
    for i in range(100, 700, 5):
        pygame.draw.line(fenster, WEISS, (i, 275), (i+25, 275))

    # Straßenrand
    pygame.draw.line(fenster, BRAUN, (50, 250), (50, 350))  # Linke Seite
    pygame.draw.line(fenster, BRAUN, (750, 250), (750, 350))  # Rechte Seite


    # Fenster aktualisieren
    pygame.display.update()

pygame.quit()