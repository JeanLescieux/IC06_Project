import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre (par exemple, 800x600)
TAILLE_TILE = 40
largeur_carte = 20
hauteur_carte = 15
taille_fenetre = (800, 600)
screen = pygame.display.set_mode(taille_fenetre)
pygame.display.set_caption("Labyrinthe Plus Grand avec Défilement")

# Définition des couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
GRIS = (100, 100, 100)
VERT = (0, 255, 0)

# Définition de la carte (20x20)
carte = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

]

# Initialisation de la matrice de visibilité
visibility = [[False for _ in range(largeur_carte)] for _ in range(hauteur_carte)]

# Position initiale du personnage (en pixels)
pos_x, pos_y = 1 * TAILLE_TILE + TAILLE_TILE // 2, 1 * TAILLE_TILE + TAILLE_TILE // 2

# Vitesse de déplacement (pixels par image)
vitesse = 4  # Augmenté pour compenser le plus grand labyrinthe

# Créer une surface de visibilité avec transparence
visibility_surface = pygame.Surface(taille_fenetre, pygame.SRCALPHA)
visibility_surface.fill((0, 0, 0, 255))  # Noir complètement opaque

# Fonction pour mettre à jour la visibilité
def update_visibility(pos_x, pos_y, TAILLE_TILE, largeur_carte, hauteur_carte, visibility):
    grille_x = pos_x // TAILLE_TILE
    grille_y = pos_y // TAILLE_TILE
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = grille_x + dx, grille_y + dy
            if 0 <= nx < largeur_carte and 0 <= ny < hauteur_carte:
                visibility[ny][nx] = True

# Fonction pour dessiner la couche de visibilité
def draw_visibility(visibility, TAILLE_TILE, largeur_carte, hauteur_carte, visibility_surface):
    visibility_surface.fill((0, 0, 0, 255))  # Remplir la surface avec noir opaque
    for y in range(hauteur_carte):
        for x in range(largeur_carte):
            if visibility[y][x]:
                rect = pygame.Rect(x * TAILLE_TILE, y * TAILLE_TILE, TAILLE_TILE, TAILLE_TILE)
                pygame.draw.rect(visibility_surface, (0, 0, 0, 0), rect)  # Rendre la case complètement transparente

# Fonction pour vérifier si une position est dans un mur
def est_mur(x, y, TAILLE_TILE, largeur_carte, hauteur_carte, carte):
    grille_x = x // TAILLE_TILE
    grille_y = y // TAILLE_TILE
    if grille_x < 0 or grille_x >= largeur_carte or grille_y < 0 or grille_y >= hauteur_carte:
        return True
    return carte[grille_y][grille_x] == 1

# Boucle principale
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Gestion des touches pressées
    touches = pygame.key.get_pressed()

    # Stocker les positions potentielles
    nouvelle_x, nouvelle_y = pos_x, pos_y

    if touches[pygame.K_LEFT]:
        nouvelle_x -= vitesse
    if touches[pygame.K_RIGHT]:
        nouvelle_x += vitesse
    if touches[pygame.K_UP]:
        nouvelle_y -= vitesse
    if touches[pygame.K_DOWN]:
        nouvelle_y += vitesse

    # Vérifier la collision pour le déplacement en X
    if not est_mur(nouvelle_x, pos_y, TAILLE_TILE, largeur_carte, hauteur_carte, carte):
        pos_x = nouvelle_x
    # Vérifier la collision pour le déplacement en Y
    if not est_mur(pos_x, nouvelle_y, TAILLE_TILE, largeur_carte, hauteur_carte, carte):
        pos_y = nouvelle_y

    # Mettre à jour la visibilité
    update_visibility(pos_x, pos_y, TAILLE_TILE, largeur_carte, hauteur_carte, visibility)

    # Calculer la fenêtre de vue (scrolling)
    vue_x = pos_x - taille_fenetre[0] // 2
    vue_y = pos_y - taille_fenetre[1] // 2

    # Limiter le scrolling pour ne pas dépasser les limites du labyrinthe
    vue_x = max(0, min(vue_x, largeur_carte * TAILLE_TILE - taille_fenetre[0]))
    vue_y = max(0, min(vue_y, hauteur_carte * TAILLE_TILE - taille_fenetre[1]))

    # Dessiner la carte
    for y in range(hauteur_carte):
        for x in range(largeur_carte):
            rect = pygame.Rect(x * TAILLE_TILE - vue_x, y * TAILLE_TILE - vue_y, TAILLE_TILE, TAILLE_TILE)
            if carte[y][x] == 1:
                pygame.draw.rect(screen, GRIS, rect)
            else:
                pygame.draw.rect(screen, BLANC, rect)
            pygame.draw.rect(screen, NOIR, rect, 1)  # Grille

    # Dessiner le personnage (un point vert)
    rayon_personnage = 10  # Augmenté pour une meilleure visibilité
    pygame.draw.circle(screen, VERT, (pos_x - vue_x, pos_y - vue_y), rayon_personnage)

    # Dessiner la couche de visibilité
    draw_visibility(visibility, TAILLE_TILE, largeur_carte, hauteur_carte, visibility_surface)
    screen.blit(visibility_surface, (0, 0))

    # Actualisation de l'affichage
    pygame.display.flip()
    screen.fill(NOIR)
    clock.tick(60)  # Limite à 60 images par seconde
