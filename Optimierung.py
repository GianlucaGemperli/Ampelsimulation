import pygame
import random
import time
import constants as c
import numpy as np

pygame.init()

clock = pygame.time.Clock()

# Bildschirm und Farben einrichten
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
Backcolour = pygame.color.Color('#31a342')
pygame.display.set_caption('Ampelsimulation')

# Strasse laden
Strasse = pygame.image.load("Strasse.png")

# Auto-Klasse
class Car:
    def __init__(self, name, x, y, speed=1.745, scale=(100, 200), angle=90, moving_up=False, moving_left=False, moving_down=False, moving_right=False):
        self.name = name
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load("car.png")
        self.image = pygame.transform.scale(self.image, scale)
        self.angle = angle
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.moving_up = moving_up
        self.moving_left = moving_left
        self.moving_down = moving_down
        self.moving_right = moving_right
        self.waiting = False
        self.wait_start_time = 0
        self.wait_after_green = False
        self.extra_wait_time = 0  # Zusätzliche Wartezeit
        self.stop_timer = 0  # Timer für die Stillstandszeit
        self.is_stopped = False  # Status, ob das Auto stoppt

    def move(self, traffic_lights, cars):
        for light in traffic_lights:
            if light.is_car_stopped(self):
                self.is_stopped = True  # Auto bleibt stehen
                self.stop_timer += clock.get_time() / 1000.0  # Zeit seit dem letzten Frame zur Stillstandszeit hinzufügen
                return  # Auto bleibt stehen, wenn die Ampel rot ist oder gelb ist

        # Reset the stop timer if the car is not stopped
        if self.is_stopped:
            self.is_stopped = False

        # Abstand zu anderen Autos überprüfen
        for other_car in cars:
            if other_car != self:
                if self.moving_up and other_car.y < self.y and abs(other_car.x - self.x) < 20 and abs(other_car.y - self.y) < 80:
                    return  # Verhindert Bewegung nach oben
                elif self.moving_down and other_car.y > self.y and abs(other_car.x - self.x) < 20 and abs(other_car.y - self.y) < 80:
                    return  # Verhindert Bewegung nach unten
                elif self.moving_left and other_car.x < self.x and abs(other_car.y - self.y) < 20 and abs(other_car.x - self.x) < 80:
                    return  # Verhindert Bewegung nach links
                elif self.moving_right and other_car.x > self.x and abs(other_car.y - self.y) < 20 and abs(other_car.x - self.x) < 80:
                    return  # Verhindert Bewegung nach rechts

        # Bewegung des Autos
        if self.moving_up:
            self.y -= self.speed
        elif self.moving_left:
            self.x -= self.speed
        elif self.moving_down:
            self.y += self.speed
        elif self.moving_right:
            self.x += self.speed
        else:
            self.x += self.speed
        if not self.moving_up and self.x >= 276 and self.y == 250:
            self.moving_up = True
            self.angle += 90

        if self.x <= 275 and self.y == 210 and not self.moving_up:
            self.angle -= 90
            self.moving_up = True

        if self.x == 220 and self.y >= 208 and not self.moving_left:
            self.angle -= 90
            self.moving_left = True
            self.moving_down = False

        if self.x == 219 and self.y >= 298 and not self.moving_left:
            self.angle += 90
            self.moving_right = True
            self.moving_down = False

        self.rect.topleft = (self.x, self.y)

    def get_stop_time(self):
        return self.stop_timer

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)

# Ampel-Klasse
class TrafficLight:
    def __init__(self, x, y, car_names=None):
        self.x = x
        self.y = y
        self.current_state = 'red'  # Standardmässig rot
        self.colors = {
            'red': pygame.color.Color('red'),
            'yellow': pygame.color.Color('yellow'),
            'green': pygame.color.Color('green')
        }
        self.car_names = car_names if car_names is not None else []  # Liste der gesteuerten Autos
        self.is_pedestrian_traffic_light = False  # Flag für Fussgängerampeln

    def set_state(self, state):
        self.current_state = state

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.color.Color("black"), (self.x - 7, self.y - 10, 14, 40))
        if self.current_state == 'red':
            pygame.draw.circle(screen, self.colors['red'], (self.x, self.y), 5)
        elif self.current_state == 'yellow':
            pygame.draw.circle(screen, self.colors['yellow'], (self.x, self.y + 10), 5)
        elif self.current_state == 'green':
            pygame.draw.circle(screen, self.colors['green'], (self.x, self.y + 20), 5)

    def is_car_stopped(self, car):
        if car.name in self.car_names and (self.current_state == 'red' or self.current_state == 'yellow') and self.x - 70 <= car.x <= self.x + 30 and self.y - 100 <= car.y <= self.y + 100:
            return True
        return False

# Hauptschleife
def main():
    cars = []
    car_spawn_rates = {
        "Car1": 0.0001504,
        "Car2": 0.0019052,
        "Car3": 0.0002529,
        "Car4": 0.00452,
        "Car5": 0.0006222,
        "Car6": 0.0009333
    }

    # Erstellen von mehreren Ampeln
    traffic_lights = [
        TrafficLight(x=250, y=80, car_names=["Car5", "Car6"]),  # Ampel 1
        TrafficLight(x=80, y=280, car_names=["Car1"]),  # Ampel 2
        TrafficLight(x=80, y=320, car_names=["Car2"]),  # Ampel 3
        TrafficLight(x=460, y=230, car_names=["Car4", "Car3"])  # Ampel 4
    ]

    # Phasen der Ampeln
    phases = [
        {"duration": 40, "green": [2, 3], "yellow": [], "red": [0, 1]},
        {"duration": 3, "yellow": [2, 3], "red": [0, 1]},
        {"duration": 12, "green": [1], "yellow": [], "red": [0, 2, 3]},
        {"duration": 3, "yellow": [1], "red": [0, 2, 3]},
        {"duration": 12, "green": [0], "yellow": [], "red": [1, 2, 3]},
        {"duration": 3, "yellow": [0], "red": [1, 2, 3]},
        {"duration": 9, "green": [], "yellow": [], "red": [0, 1, 2, 3]}
    ]

    phase_index = 0
    phase_start_time = time.time()

    best_phases = phases[:]
    best_stop_time = float('inf')  # Unendlich setzen als Startwert

    trial_iterations = 0  # Zählt die Anzahl der Versuche

    running = True
    while running:
        screen.fill(Backcolour)
        screen.blit(Strasse, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time()
        elapsed_time = current_time - phase_start_time

        if elapsed_time >= phases[phase_index]["duration"]:
            phase_index = (phase_index + 1) % len(phases)
            phase_start_time = current_time

            for i, traffic_light in enumerate(traffic_lights):
                if i in phases[phase_index].get("green", []):
                    traffic_light.set_state('green')
                elif i in phases[phase_index].get("yellow", []):
                    traffic_light.set_state('yellow')
                else:
                    traffic_light.set_state('red')

        # Autos spawnen
        for car_name, spawn_rate in car_spawn_rates.items():
            if np.random.binomial(1, spawn_rate):
                new_car = None
                if car_name == "Car1":
                    new_car = Car(name="Car1", x=-1000, y=250, scale=(60, 60), angle=-90)
                elif car_name == "Car2":
                    new_car = Car(name="Car2", x=-1000, y=297, scale=(60, 60), angle=-90, moving_up=False)
                elif car_name == "Car3":
                    new_car = Car(name="Car3", x=1560, y=210, scale=(60, 60), angle=90, moving_left=True)
                elif car_name == "Car4":
                    new_car = Car(name="Car4", x=1560, y=209, scale=(60, 60), angle=90, moving_left=True)
                elif car_name == "Car5":
                    new_car = Car(name="Car5", x=220, y=-1000, scale=(60, 60), angle=180, moving_down=True)
                elif car_name == "Car6":
                    new_car = Car(name="Car6", x=219, y=-1000, scale=(60, 60), angle=180, moving_down=True)

                # Zusätzliche Wartezeit basierend auf bereits vorhandenen Autos
                if new_car:
                    new_car.extra_wait_time = len(cars)
                    cars.append(new_car)

        # Autos und Ampeln zeichnen
        for car in cars:
            car.move(traffic_lights, cars)
            car.draw(screen)

        for light in traffic_lights:
            light.draw(screen)

        # Gesamtstopptimer aktualisieren
        total_stop_time = sum(car.get_stop_time() for car in cars)

        # Gesamtstopptimer anzeigen
        font = pygame.font.Font(None, 36)
        timer_text = font.render(f"Total Stop Time: {total_stop_time:.1f}s", True, (255, 255, 255))
        screen.blit(timer_text, (10, c.SCREEN_HEIGHT - 50))  # Position am unteren Bildschirmrand

        # Prüfen, ob die aktuelle Konfiguration besser ist
        if total_stop_time < best_stop_time:
            best_stop_time = total_stop_time
            best_phases = phases[:]  # Beste Phasenkonfiguration speichern

        # Nächsten Versuch starten (z.B. alle 1800 Frames oder wenn eine bestimmte Anzahl von Iterationen erreicht ist)
        if trial_iterations % 1800 == 0:
            # Zufällig neue Phasen generieren
            phases = [
                {"duration": random.randint(10, 50), "green": [2, 3], "red": [0, 1]},
                {"duration": random.randint(4, 30), "green": [1], "red": [0, 2, 3]},
                {"duration": random.randint(4, 30), "green": [0], "red": [1, 2, 3]},
            ]
            print(f"Neue Phasen ausprobiert: {phases}, Beste Zeit: {best_stop_time:.1f}s")

        trial_iterations += 1
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    print(f"Beste Phaseneinstellungen: {best_phases}, mit einer Gesamtstopzeit von: {best_stop_time:.1f}s")

if __name__ == "__main__":
    main()
