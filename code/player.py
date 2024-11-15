import pygame
from settings import *
from debug import debug
from enemy import Enemy

ATTACK_RADIUS = 25  # Rayon d'attaque en pixels
WEAPON_DISPLAY_TIME = 200  # Durée d'affichage de l'image de l'arme en millisecondes
SHIELD_DURATION = 3000  # Durée du bouclier en millisecondes

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.original_image = pygame.transform.scale(pygame.image.load('../graphics/test/player.png').convert_alpha(), (16, 16))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
        self.attack_direction = pygame.math.Vector2(0, -1)
        self.health = 100
        self.attack_damage = 10
        self.attack_cooldown = 500
        self.last_attack_time = 0
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 2
        self.space_held = False
        self.alert = 0

        self.obstacle_sprites = obstacle_sprites

        # Image et position de l'arme
        self.weapon_image = pygame.transform.scale(pygame.image.load('../graphics/test/attack.png').convert_alpha(), (16, 16))
        self.weapon_rect = self.weapon_image.get_rect()
        self.weapon_visible = False
        self.weapon_display_time = 0

        # Bouclier
        self.shield_active = False
        self.shield_timer = 0  # Chronomètre du bouclier
        self.shield_image = pygame.image.load('../graphics/test/shield.png').convert_alpha()  # Image du bouclier
        self.shield_rect = self.rect.inflate(40, 40)  # Ajustez la taille du bouclier

    def input(self):
        keys = pygame.key.get_pressed()

        # Activer/désactiver le bouclier avec "B" seulement si le bouclier n'est pas déjà actif
        if keys[pygame.K_b] and not self.shield_active:
            self.shield_active = True
            self.shield_timer = pygame.time.get_ticks()  # Démarre le chronomètre du bouclier
        elif not keys[pygame.K_b] and self.shield_active:
            self.shield_active = False  # Désactive dès qu'on relâche "B"

        # Gérer l'attaque
        if keys[pygame.K_SPACE] and not self.space_held and not self.shield_active:
            self.attack()
            self.space_held = True
        elif not keys[pygame.K_SPACE]:
            self.space_held = False

        # Gérer le mouvement seulement si le bouclier n'est pas actif
        if not self.shield_active:
            self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

            # Mettre à jour la direction d'attaque si le joueur se déplace
            if self.direction.magnitude() != 0:
                self.attack_direction = self.direction.normalize()

    def update(self):
        # Gérer la durée du bouclier
        if self.shield_active and pygame.time.get_ticks() - self.shield_timer >= SHIELD_DURATION:
            self.shield_active = False  # Désactive le bouclier après la durée

        self.input()
        self.move(self.speed)
        self.update_orientation()
        debug(f'Player Health: {self.health}', y=10, x=10)
        debug(f'Alert Level: {self.alert}', y=80, x=10)

    def move(self, speed):
        if not self.shield_active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.hitbox.y += self.direction.y * speed
            self.collision('vertical')
            self.rect.center = self.hitbox.center
    def update_orientation(self):
        if self.direction.magnitude() != 0:
            angle = self.direction.angle_to(pygame.math.Vector2(0, -1))
            self.image = pygame.transform.rotate(self.original_image, angle)
            self.rect = self.image.get_rect(center=self.rect.center)
    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            if self.direction.magnitude() != 0:
                self.attack_direction = self.direction.normalize()
            
            self.weapon_visible = True
            self.weapon_display_time = current_time
            offset = self.attack_direction * ATTACK_RADIUS
            self.weapon_rect.center = self.rect.center + offset
            
            debug(f'Attack Direction: {self.attack_direction}', y=10, x=10)
            
            for sprite in self.obstacle_sprites:
                if isinstance(sprite, Enemy):
                    player_center = pygame.math.Vector2(self.rect.center)
                    enemy_center = pygame.math.Vector2(sprite.rect.center)
                    distance = player_center.distance_to(enemy_center)
                    
                    if distance <= ATTACK_RADIUS:
                        direction_to_enemy = (enemy_center - player_center).normalize()
                        
                        # Calculer le produit scalaire entre la direction de l'attaque et la direction de l'ennemi
                        dot_product = self.attack_direction.dot(sprite.direction)
                        
                        # Si le produit scalaire est proche de 1, l'attaque vient de devant l'ennemi
                            
                        if hasattr(sprite, 'last_non_zero_direction') and self.attack_direction.dot(sprite.last_non_zero_direction) > 0.0:
                            # Dégâts doublés
                            sprite.receive_damage(self.attack_damage * 10)
                        else:
                            # L'attaque vient de côté, dégâts réduits ou modifiés
                            sprite.receive_damage(self.attack_damage)


    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite.hitbox.colliderect(self.hitbox) and sprite != self:
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def draw_weapon(self, screen, offset):
        if self.weapon_visible:
            # Calculer la position dynamique de l'arme en fonction de la position actuelle du joueur
            weapon_offset = self.attack_direction * ATTACK_RADIUS
            self.weapon_rect.center = self.rect.center + weapon_offset

            # Appliquer le décalage pour suivre la caméra
            if not isinstance(offset, pygame.math.Vector2):
                offset = pygame.math.Vector2(offset)
            
            # Afficher l'arme avec la position ajustée
            screen.blit(self.weapon_image, self.weapon_rect.topleft - offset)
            
            # Cacher l'arme après un certain temps
            if pygame.time.get_ticks() - self.weapon_display_time > WEAPON_DISPLAY_TIME:
                self.weapon_visible = False

    def draw_shield(self, screen, offset):
        if self.shield_active:
            # Position du bouclier (centre du joueur)
            shield_pos = self.rect.center

            # Appliquer le décalage pour la caméra
            if not isinstance(offset, pygame.math.Vector2):
                offset = pygame.math.Vector2(offset)

            # Afficher le bouclier avec la position ajustée
            screen.blit(self.shield_image, shield_pos - offset)


