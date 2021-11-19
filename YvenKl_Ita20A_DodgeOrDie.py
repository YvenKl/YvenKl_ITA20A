import pygame
from pygame.version import PygameVersion
import os
from random import randint
import sys
#Yven Kl Ita20A
class Settings:
    window_width = 750
    window_height = 950
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "Dodge or die"
    player_vel = 5
    min_asteroid_vel = 2
    max_asteroid_vel = 4
    points = 1
    lives = 3
    nof_asteroids = 5
    level_indicator = 1

class Background(object):
    def __init__(self, filename="background.jpg") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))
        main_font = pygame.font.SysFont("comicsans", 50) #Schriftart von der Font
        lives_label = main_font.render(f"Points: {Settings.points}", 1, (255, 0, 0)) #Farben der Fonts
        point_label = main_font.render(f"Lives: {Settings.lives}", 1, (255, 0, 0))
        level_label = main_font.render(f"Difficulty: {Settings.level_indicator}", 1, (255, 0, 0))
        screen.blit(level_label, (10, Settings.window_height - point_label.get_height() - 10)) #Koordinaten der Fonts
        screen.blit(lives_label, (10, 10))
        screen.blit(point_label, (Settings.window_width - point_label.get_width() - 10, 10))

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "player_ship.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.top = Settings.window_height * 0.8    #Spawnpoint des Players (Unten mittig)
        self.rect.left = Settings.window_width/2 - self.rect.width/2    #Spawnpoint des Players (Unten mittig)
        self.x = x
        self.y = y


    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left - Settings.player_vel > 0:  # links movement
            self.rect.left -= Settings.player_vel
        if keys[pygame.K_RIGHT] and self.rect.left + Settings.player_vel + self.get_width() < Settings.window_width:  # rechts movement
            self.rect.left += Settings.player_vel
        if keys[pygame.K_UP] and self.rect.top - Settings.player_vel > 0:  # nach oben movement
            self.rect.top -= Settings.player_vel
        if keys[pygame.K_DOWN] and self.rect.top + Settings.player_vel + self.get_height() + 15 < Settings.window_height:  # nach unten movement
            self.rect.top += Settings.player_vel



    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, "Asteroid_Brown.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = randint(50, Settings.window_width-50)
        self.rect.top = 0
        self.speed_h = randint(0, 0)
        self.speed_v = randint(Settings.min_asteroid_vel, Settings.max_asteroid_vel)
        scale_ratio = randint(2, 8) / 4
        self.image = pygame.transform.scale(self.image, ( #Hier wird die größe per zufall erstellt
        int(self.image.get_rect().width * scale_ratio),
        int(self.image.get_rect().height * scale_ratio)))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip((self.speed_h, self.speed_v))
        if self.rect.bottom + self.speed_v > Settings.window_height:  #Asteroiden werden unten gekillt und der wird Score angehoben
            self.kill()
            Settings.points += 1
        self.rect.move_ip((self.speed_h, self.speed_v))



class Game(object):
    def __init__(self) -> None:
        super().__init__()
        # Position Fenster
        os.environ['SDL_VIDEO_WINDOW_POS'] = "50,30"

        # PyGame-Vorbereitungen
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.playership = pygame.sprite.Group()
        self.asteroid = pygame.sprite.Group()

    def groupcollide(self):
        pygame.sprite.groupcollide(self.playership, self.asteroid, True, False, pygame.sprite.collide_rect) #Standart rect collision



    def run(self):
        self.start()
        # Hauptprogrammschleife
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            self.groupcollide()

        pygame.quit()

    def draw(self):
        self.background.draw(self.screen)
        self.playership.draw(self.screen)
        self.asteroid.draw(self.screen)
        pygame.display.flip()


    def update(self):
        self.playership.update()
        self.asteroid.update()
        self.playership.update()
        if len(self.asteroid.sprites()) < Settings.nof_asteroids:   #Asteroiden werden kontinuirlich gespawnt wenn welche gekillt werden, anhand der number of asteroides
            self.asteroid.add(Asteroid())
        if len(self.playership.sprites()) < 1:                #Wenn der Spieler mit einem Asteroid kollidiert respawnt er am Startpunkt und der rest der Asteroiden despawnen
            self.playership.add(PlayerShip(0,0))
            for astroids in self.asteroid.sprites():
                astroids.remove(self.asteroid)
            if Settings.lives > 1:                              #Leben werden abgezogen bis die 0 erreicht wird, danach wird das Spiel beendet
                Settings.lives -= 1

            else:
                pygame.quit()

        if Settings.points == 40 and Settings.level_indicator == 1:     #Hier werden verschiedene Schwierigkeiten festgelegt
            Settings.min_asteroid_vel += 1                              #Desto höher der Score, desto höher die Schwierigkeit
            Settings.max_asteroid_vel += 1                              #Die Geschwindigkeit und die NumberofAsteroids werden erhöht
            Settings.level_indicator = 2                                #Anhand des Indicators wird alles was hier steht maximal nur einmal pro Spiel ausgeführt

        if Settings.points == 60 and Settings.level_indicator == 2:
            Settings.nof_asteroids += 1
            Settings.level_indicator = 3

        if Settings.points == 100 and Settings.level_indicator == 3:
            Settings.min_asteroid_vel += 1
            Settings.max_asteroid_vel += 2
            Settings.level_indicator = 4

        if Settings.points == 130 and Settings.level_indicator == 4:
            Settings.nof_asteroids += 2
            Settings.level_indicator = 5


    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def start(self):
        self.background = Background()
        self.playership.add(PlayerShip(1, 1))       #Syntax, dass der Spieler an der Startposition spawnt
        for a in range(Settings.nof_asteroids):
            self.asteroid.add(Asteroid())



if __name__ == "__main__":
    game = Game()
    game.run()
