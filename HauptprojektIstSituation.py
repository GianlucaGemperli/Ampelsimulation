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

    def move(self, traffic_lights, cars):
        for light in traffic_lights:
            if light.is_car_stopped(self):
                self.waiting = True
                self.wait_start_time = time.time()
                return  # Auto bleibt stehen, wenn die Ampel rot ist oder gelb ist

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

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, rotated_rect.topleft)

# Fussgänger-Klasse
class Fussgaenger:
    def __init__(self, x, y, target_x, target_y, speed=0.3):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.color = pygame.color.Color("blue")
        self.radius = 5
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.is_stopped = False  # Flag, um die Bewegung zu stoppen, wenn die Ampel rot ist

    def move(self, traffic_lights):
        if self.is_stopped:
            return  # Fussgänger bleibt stehen, wenn Ampel rot ist

        if self.x < self.target_x:
            self.x += self.speed
        elif self.x > self.target_x:
            self.x -= self.speed

        if self.y < self.target_y:
            self.y += self.speed
        elif self.y > self.target_y:
            self.y -= self.speed

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def stop_if_red_light(self, traffic_lights):
        # Fussgängerampel 5 (Ampel an (330, 120)) oder Fussgängerampel 6 (Ampel an (400, 360))
        relevant_traffic_lights = [traffic_lights[4], traffic_lights[5]]

        for light in relevant_traffic_lights:
            if light.current_state == 'red':
                if (self.x, self.y) == (215, 120) or (self.x, self.y) == (400, 215):
                    self.is_stopped = True
                    return

        self.is_stopped = False

# Funktion zum zufälligen Erstellen eines Fussgängers
def spawn_fussgaenger():
    spawn_point = random.choice([(215, 120, 330, 120), (400, 215, 400, 360)])
    return Fussgaenger(x=spawn_point[0], y=spawn_point[1], target_x=spawn_point[2], target_y=spawn_point[3])

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

    def check_for_pedestrians(self, fussgaenger_list):
        if self.is_pedestrian_traffic_light:
            for fussgaenger in fussgaenger_list:
                if ((fussgaenger.x, fussgaenger.y) == (215, 120) or (fussgaenger.x, fussgaenger.y) == (400, 215)):
                    return True  # Fussgänger steht auf einem der Punkte
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
        TrafficLight(x=460, y=230, car_names=["Car4", "Car3"]),  # Ampel 4
        TrafficLight(x=330, y=120),  # Fussgängerampel 1
        TrafficLight(x=400, y=360)   # Fussgängerampel 2
    ]

    # Fussgängerampeln markieren
    traffic_lights[4].is_pedestrian_traffic_light = True
    traffic_lights[5].is_pedestrian_traffic_light = True

    # Liste für Fussgänger
    fussgaenger_list = []

    # Phasen der Ampeln
    phases = [
        {"duration": 40, "green": [2, 3], "yellow": [], "red": [0, 1], "pedestrian_phase": False},
        {"duration": 3, "yellow": [2, 3], "red": [0, 1]},
        {"duration": 12, "green": [1], "yellow": [], "red": [0, 2, 3], "pedestrian_phase": False},
        {"duration": 3, "yellow": [1], "red": [0, 2, 3]},
        {"duration": 12, "green": [0], "yellow": [], "red": [1, 2, 3], "pedestrian_phase": False},
        {"duration": 3, "yellow": [0], "red": [1, 2, 3]},
        {"duration": 9, "green": [], "yellow": [], "red": [0, 1, 2, 3], "pedestrian_phase": True}
    ]

    phase_index = 0
    phase_start_time = time.time()

    # Fussgänger-Spawn-Zeit
    SPAWN_INTERVAL = 40  # 40 Sekunden zwischen den Fussgängern
    last_spawn_time = time.time()

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

        # Fussgängerampeln steuern
        if phases[phase_index].get("pedestrian_phase", False):
            for light in traffic_lights[4:]:
                light.set_state('green')  # Fussgängerampeln auf Grün schalten
        else:
            for light in traffic_lights[4:]:
                light.set_state('red')  # Fussgängerampeln auf Rot schalten

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

        # Fußgänger spawnen und bewegen
        if current_time - last_spawn_time >= SPAWN_INTERVAL and len(fussgaenger_list) < 4:
            fussgaenger_list.append(spawn_fussgaenger())
            last_spawn_time = current_time

        for fussgaenger in fussgaenger_list[:]:
            fussgaenger.stop_if_red_light(traffic_lights)
            fussgaenger.move(traffic_lights)
            fussgaenger.draw(screen)
            if abs(fussgaenger.x - fussgaenger.target_x) < 1 and abs(fussgaenger.y - fussgaenger.target_y) < 1:
                fussgaenger_list.remove(fussgaenger)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
