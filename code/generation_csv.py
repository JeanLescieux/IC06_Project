import random
import csv

# Constantes
TILESIZE = 64
GRID_WIDTH = 20  # Largeur de la carte en nombre de tiles
GRID_HEIGHT = 20  # Hauteur de la carte en nombre de tiles
ROOM_WIDTH = 5  # Largeur d'une salle en tiles
ROOM_HEIGHT = 5  # Hauteur d'une salle en tiles

# Fonction pour créer une salle dans la grille
def create_room(grid, start_x, start_y, room_type):
    for y in range(start_y, start_y + ROOM_HEIGHT):
        for x in range(start_x, start_x + ROOM_WIDTH):
            if x == start_x or x == start_x + ROOM_WIDTH - 1 or y == start_y or y == start_y + ROOM_HEIGHT - 1:
                grid[y][x] = '1'  # Boundary (mur)
            else:
                grid[y][x] = '0'  # Floor (sol)

# Générer les fichiers CSV pour boundary, grass, objects, entities
def generate_and_save_csv():
    # Générer la grille pour boundary, grass, objects, entities
    boundary_grid = [['-1' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    grass_grid = [['-1' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    object_grid = [['-1' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    entities_grid = [['-1' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Générer les salles
    for i in range(3):  # Créer 3 salles aléatoires
        start_x = random.randint(0, GRID_WIDTH - ROOM_WIDTH - 1)
        start_y = random.randint(0, GRID_HEIGHT - ROOM_HEIGHT - 1)
        create_room(boundary_grid, start_x, start_y, room_type='normal')
    
    # Placer des éléments spécifiques dans les salles
    player_x, player_y = random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3)
    entities_grid[player_y][player_x] = '394'  # Joueur
    
    for _ in range(5):  # Ajouter 5 ennemis
        enemy_x, enemy_y = random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3)
        entities_grid[enemy_y][enemy_x] = random.choice(['390', '391', '392'])  # Différents types d'ennemis
    
    # Ajouter de l'herbe dans des endroits aléatoires
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if random.random() < 0.05 and grass_grid[y][x] == '-1':  # 5% de chance d'ajouter de l'herbe
                grass_grid[y][x] = '0'  # Indicateur de tile herbe
    
    # Ajouter des objets aléatoires
    for _ in range(10):  # Ajouter 10 objets
        obj_x, obj_y = random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3)
        object_grid[obj_y][obj_x] = str(random.randint(0, 3))  # Différents objets
    
    # Sauvegarder les fichiers CSV
    save_csv(boundary_grid, '../map/map_FloorBlocks.csv')
    save_csv(grass_grid, '../map/map_Grass.csv')
    save_csv(object_grid, '../map/map_Objects.csv')
    save_csv(entities_grid, '../map/map_Entities.csv')

# Fonction pour sauvegarder les fichiers CSV
def save_csv(grid, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(grid)

