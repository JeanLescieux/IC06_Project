import pygame
import random
from settings import *
from debug import debug
from tile import Tile
from key import Key


# Variable globale alert (à définir dans votre script principal)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, player, has_key=False):
        super().__init__(groups)
        self.original_image = pygame.transform.scale(pygame.image.load('../graphics/test/squid.png').convert_alpha(),(16,16))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.health = 20

        self.has_key = has_key  # Cet ennemi possède une clé ?

        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 1
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.obstacle_sprites = obstacle_sprites
        self.player = player

        self.change_direction_timer = 0
        self.change_interval = 1000  # Temps entre chaque changement de direction (en ms)
        self.pause_time = 1000  # Pause de 1 seconde entre les changements de direction
        self.last_direction_change_time = 0  # Temps du dernier changement de direction
        self.attack_radius = 25
        self.vision_radius = 120

        self.large_vision_radius = 500  # Plus grand que le champ de vision normal
        self.large_vision_angle = 360

        self.attack_damage = 10
        self.vision_angle = 90  # Angle de vision en degrés

        self.weapon_image = pygame.transform.scale(pygame.image.load('../graphics/test/attack.png').convert_alpha(),(16,16))
        self.weapon_rect = self.weapon_image.get_rect()
        self.weapon_visible = False
        self.weapon_display_duration = 200
        self.weapon_display_start = 0
        self.chasing_player = False
        self.alert = False

        # Temps depuis la détection du joueur
        self.detection_time = None

    def display_weapon(self, screen, offset):
        """ Affiche l'image de l'arme temporairement si l'ennemi attaque. """
        current_time = pygame.time.get_ticks()
        if self.weapon_visible:
            if current_time - self.weapon_display_start > self.weapon_display_duration:
                self.weapon_visible = False
            else:
                offset_pos = self.rect.center + (self.direction * self.attack_radius) - offset
                screen.blit(self.weapon_image, offset_pos)

    def get_random_direction(self):
        directions = [
            pygame.math.Vector2(1, 0),
            pygame.math.Vector2(-1, 0),
            pygame.math.Vector2(0, 1),
            pygame.math.Vector2(0, -1),
        ]
        self.direction = random.choice(directions)

    def update_orientation(self):
        if self.direction.magnitude() != 0:
            angle = self.direction.angle_to(pygame.math.Vector2(0, -1))
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
    
    def is_player_in_line_of_sight(self, player_center, large=False):
        """ Vérifie si le joueur est dans le champ de vision. 
            Le paramètre `large` permet d'utiliser le champ de vision élargi.
        """
        max_distance = self.large_vision_radius if large else self.vision_radius
        angle_of_view = self.large_vision_angle if large else self.vision_angle

        # Reste du code pour le champ de vision (comme avant)
        direction_vector = pygame.math.Vector2(player_center) - pygame.math.Vector2(self.rect.center)
        distance_to_player = direction_vector.length()

        if distance_to_player > max_distance or self.direction.length() == 0:
            return False

        enemy_direction = self.direction.normalize()
        angle_to_player = enemy_direction.angle_to(direction_vector.normalize())

        if abs(angle_to_player) > angle_of_view / 2:
            if large == False:
                return False

        # Vérification des obstacles entre l'ennemi et le joueur (comme avant)
        for sprite in self.obstacle_sprites:
            if isinstance(sprite, Tile) and sprite.hitbox.clipline(self.rect.center, player_center):
                return False

        return True

    def move(self):
        
        # 1. Vérification de la direction actuelle pour éviter un déplacement constant vers le haut
        if self.direction.magnitude() != 0:
            self.last_non_zero_direction = self.direction.normalize()
        elif self.chasing_player:
            # Maintenir la dernière direction de poursuite si l'ennemi est en mode poursuite
            self.direction = self.last_non_zero_direction
        else:
            # Si aucune direction n'est définie, rester immobile
            self.direction = pygame.math.Vector2(0, 0)

        player_center = pygame.math.Vector2(self.player.rect.center)
        enemy_center = pygame.math.Vector2(self.rect.center)
        distance = player_center.distance_to(enemy_center)

        # 2. Détection du joueur dans le champ de vision
        if distance <= self.vision_radius and self.is_player_in_line_of_sight(player_center):
            self.chasing_player = True
            if self.detection_time is None:
                self.detection_time = pygame.time.get_ticks()

        # 3. Arrêt de la poursuite si le joueur sort du champ de vision large
        elif self.chasing_player and not self.is_player_in_line_of_sight(player_center, large=True):
            self.chasing_player = False
            self.detection_time = None

        # 4. Comportement de poursuite si le joueur est détecté
        if self.chasing_player:
            # Mise à jour de la direction vers le joueur
            self.direction = (player_center - enemy_center).normalize()
            debug('En Poursuite!', y=60, x=10)

            # Vérifier si le joueur est en alerte après 2 secondes de poursuite
            if pygame.time.get_ticks() - self.detection_time >= 2000 and not self.alert:
                self.player.alert += 1
                self.alert = True
        else:
            # 5. Comportement de patrouille aléatoire si le joueur n'est pas poursuivi
            current_time = pygame.time.get_ticks()
            if current_time - self.last_direction_change_time >= self.pause_time:
                if self.direction == pygame.math.Vector2(0, 0):
                    self.get_random_direction()  # Changer vers une direction aléatoire
                    self.last_direction_change_time = current_time
                    self.pause_time = 2000  # Temps entre deux changements de direction
                else:
                    self.direction = pygame.math.Vector2(0, 0)  # Pause aléatoire
                    self.last_direction_change_time = current_time
                    self.pause_time = 1000  # Durée de la pause

        # 6. Normaliser la direction avant d'appliquer le déplacement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # 7. Calcul du facteur de vitesse en fonction de l'alerte du joueur
        alert_bonus = self.player.alert  # Multiplier par un facteur (ajuster selon la rapidité désirée)

        # 8. Appliquer le bonus d'alerte en fonction de la direction de l'ennemi
        self.hitbox.x += (self.direction.x * self.speed + alert_bonus*0.2 * self.direction.x)
        if self.check_collision('horizontal'):
            self.hitbox.x -= (self.direction.x * self.speed + alert_bonus*0.2 * self.direction.x)
            if not self.chasing_player:
                self.get_random_direction()

        self.hitbox.y += (self.direction.y * self.speed + alert_bonus*0.2 * self.direction.y)
        if self.check_collision('vertical'):
            self.hitbox.y -= (self.direction.y * self.speed + alert_bonus*0.2 * self.direction.y)
            if not self.chasing_player:
                self.get_random_direction()
        # Mise à jour de la position réelle
        self.rect.center = self.hitbox.center

        # Affichage de la santé de l'ennemi pour le debug
        debug(f'Enemy Health: {self.health}', y=40, x=10)


        
    def check_collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox) and sprite != self:
                return True
        return False

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            player_center = pygame.math.Vector2(self.player.rect.center)
            enemy_center = pygame.math.Vector2(self.rect.center)

            distance = player_center.distance_to(enemy_center)
            direction_to_player = (player_center - enemy_center).normalize()
            if distance <= self.attack_radius and self.direction.dot(direction_to_player) > 0.7:
                self.weapon_visible = True
                self.weapon_display_start = current_time
                self.player.health -= self.attack_damage
                debug(f'Player Health: {self.player.health}', y=10, x=10)

    def receive_damage(self, damage):
        self.health = max(self.health - damage, 0)
        if self.health <= 0:
            if self.has_key:
                # Faire apparaître la clé à la position de l'ennemi
                print('Key Dropped!')
                Key(self.rect.center, [self.groups()[0], self.obstacle_sprites])  # Ajuster le groupe si nécessaire
            self.kill()

    def update(self):
        self.move()
        self.update_orientation()
        self.attack()
