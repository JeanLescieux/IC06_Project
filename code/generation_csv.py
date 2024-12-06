import random
import csv

# Constants for generation
GRID_WIDTH = 60
GRID_HEIGHT = 60
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 10
ROOM_MARGIN = 1

# Tile types (aligned with level.py logic)
BOUNDARY = '395'  # Boundary (walls, water, etc.)
WALKABLE = '-1'   # Empty space
WALL = '1'        # Wall tile
FLOOR = '0'       # Walkable floor tile
DOOR = '99'     # Door tile 

class RoomPartition:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room = None
        self.left = None
        self.right = None

    def split(self):
        """Split the partition into two."""
        if self.left or self.right:
            return False

        # Ensure that there is enough space for a valid split
        if self.width > MIN_ROOM_SIZE * 2 + ROOM_MARGIN and self.height > MIN_ROOM_SIZE * 2 + ROOM_MARGIN:
            if self.width > self.height:
                max_split = self.width - MIN_ROOM_SIZE - ROOM_MARGIN
                if max_split > MIN_ROOM_SIZE + ROOM_MARGIN:
                    split_line = random.randint(MIN_ROOM_SIZE + ROOM_MARGIN, max_split)
                    self.left = RoomPartition(self.x, self.y, split_line, self.height)
                    self.right = RoomPartition(self.x + split_line, self.y, self.width - split_line, self.height)
                else:
                    return False  # Skip if there isn't enough width for a valid split
            else:
                max_split = self.height - MIN_ROOM_SIZE - ROOM_MARGIN
                if max_split > MIN_ROOM_SIZE + ROOM_MARGIN:
                    split_line = random.randint(MIN_ROOM_SIZE + ROOM_MARGIN, max_split)
                    self.left = RoomPartition(self.x, self.y, self.width, split_line)
                    self.right = RoomPartition(self.x, self.y + split_line, self.width, self.height - split_line)
                else:
                    return False  # Skip if there isn't enough height for a valid split
            return True

        return False  # If the partition is too small, don't split


    def create_room(self):
        """Create a room within this partition."""
        available_width = self.width - 2 * ROOM_MARGIN
        available_height = self.height - 2 * ROOM_MARGIN

        # Ensure there is enough space for the room
        if available_width >= MIN_ROOM_SIZE and available_height >= MIN_ROOM_SIZE:
            room_width = random.randint(MIN_ROOM_SIZE, min(available_width, MAX_ROOM_SIZE))
            room_height = random.randint(MIN_ROOM_SIZE, min(available_height, MAX_ROOM_SIZE))
            room_x = random.randint(self.x + ROOM_MARGIN, self.x + self.width - room_width - ROOM_MARGIN)
            room_y = random.randint(self.y + ROOM_MARGIN, self.y + self.height - room_height - ROOM_MARGIN)
            self.room = (room_x, room_y, room_width, room_height)
        else:
            # Skip creating a room if there is not enough space
            self.room = None


def create_corridor(grid, x1, y1, x2, y2):
    """Create a corridor between two rooms."""
    if random.choice([True, False]):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[y1][x] = FLOOR
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[y][x2] = FLOOR
    else:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            grid[y][x1] = FLOOR
        for x in range(min(x1, x2), max(x1, x2) + 1):
            grid[y2][x] = FLOOR

def create_room(grid, room):
    """Place a room in the grid."""
    room_x, room_y, room_width, room_height = room
    for y in range(room_y, room_y + room_height):
        for x in range(room_x, room_x + room_width):
            grid[y][x] = FLOOR

def connect_rooms(grid, partition):
    """Connect rooms with corridors."""
    if partition.left and partition.right:
        left_room = partition.left.room
        right_room = partition.right.room
        if left_room and right_room:
            create_corridor(grid, left_room[0] + left_room[2] // 2, left_room[1] + left_room[3] // 2,
                            right_room[0] + right_room[2] // 2, right_room[1] + right_room[3] // 2)
    if partition.left:
        connect_rooms(grid, partition.left)
    if partition.right:
        connect_rooms(grid, partition.right)

def calculate_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def find_furthest_room(grid, spawn):
    walkable_positions = [(x, y) for y, row in enumerate(grid) for x, cell in enumerate(row) if cell == '0']
    furthest_position = None
    max_distance = -1

    for pos in walkable_positions:
        distance = calculate_distance(spawn, pos)
        if distance > max_distance:
            max_distance = distance
            furthest_position = pos

    return furthest_position

def place_doors(boundary_grid):
    """
    Place des portes (code '99') sur des murs ('395') situés à la limite haute
    d'une zone "walkable" (code '0') en respectant les critères définis.
    """
    # Parcours de la grille à partir de la troisième ligne pour éviter les indices négatifs
    for y in range(2, len(boundary_grid) - 1):  # On évite la première et la dernière ligne
        for x in range(0, len(boundary_grid[0]) - 2):  # On s'assure d'avoir au moins 3 cases horizontales

            # Vérification des conditions pour placer une porte
            if (
                # Trois cases murales consécutives
                boundary_grid[y][x] == '395' and
                boundary_grid[y][x + 1] == '395' and
                boundary_grid[y][x + 2] == '395' and

                # Une ligne en dessous doit être walkable
                boundary_grid[y + 1][x] == '0' and
                boundary_grid[y + 1][x + 1] == '0' and
                boundary_grid[y + 1][x + 2] == '0' and

                # Deux lignes au-dessus doivent être murales ou en dehors de la grille
                (y - 1 < 0 or (boundary_grid[y - 1][x] == '395' and 
                               boundary_grid[y - 1][x + 1] == '395' and 
                               boundary_grid[y - 1][x + 2] == '395'))
            ):
                # Débogage : Afficher les coordonnées des portes placées
                print(f"Valid door position at y={y}, x={x}-{x+2}")

                # Remplacer les murs par la porte (3x3)
                for offset_y in range(3):
                    boundary_grid[y - offset_y][x] = '99'
                    boundary_grid[y - offset_y][x + 1] = '99'
                    boundary_grid[y - offset_y][x + 2] = '99'

                # On place une seule porte pour éviter des conflits avec d'autres conditions
                return

def calculate_distance(point1, point2):
    """Calcule la distance de Manhattan entre deux points."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def get_rooms(boundary_grid):
    """Récupère toutes les pièces de la grille."""
    rooms = []
    for y, row in enumerate(boundary_grid):
        for x, cell in enumerate(row):
            if cell == FLOOR:
                # Identifier la pièce associée à cette case
                for room in rooms:
                    if (room[0] <= x < room[0] + room[2] and
                        room[1] <= y < room[1] + room[3]):
                        break
                else:
                    # Ajouter une nouvelle pièce
                    room_width, room_height = get_room_dimensions(boundary_grid, x, y)
                    rooms.append((x, y, room_width, room_height))
    return rooms

def get_room_dimensions(boundary_grid, start_x, start_y):
    """
    Calcule les dimensions (largeur, hauteur) de la pièce à partir d'une case donnée.
    """
    max_width = 0
    max_height = 0

    # Vérifie la hauteur de la pièce
    for y in range(start_y, len(boundary_grid)):
        if boundary_grid[y][start_x] != FLOOR:
            break
        max_height += 1

        # Vérifie la largeur pour chaque ligne de la pièce
        row_width = 0
        for x in range(start_x, len(boundary_grid[y])):
            if boundary_grid[y][x] != FLOOR:
                break
            row_width += 1

        # On considère la largeur minimale trouvée
        if max_width == 0:
            max_width = row_width
        else:
            max_width = min(max_width, row_width)

    return max_width, max_height


def place_objective(boundary_grid, spawn):
    """
    Place l'objectif (witch) au centre de la pièce la plus éloignée du spawn.
    """
    rooms = get_rooms(boundary_grid)
    furthest_room = None
    max_distance = -1

    # Identifier la pièce la plus éloignée
    for room in rooms:
        room_center = (room[0] + room[2] // 2, room[1] + room[3] // 2)
        distance = calculate_distance(spawn, room_center)
        if distance > max_distance:
            max_distance = distance
            furthest_room = room

    # Placer la witch au centre de cette pièce
    if furthest_room:
        center_x = furthest_room[0] + furthest_room[2] // 2
        center_y = furthest_room[1] + furthest_room[3] // 2

        if boundary_grid[center_y][center_x] == FLOOR:
            boundary_grid[center_y][center_x] = '2'  # Placer l'objectif
            print(f"Objectif placé au centre de la pièce : {(center_x, center_y)}")
        else:
            print(f"Erreur : Impossible de placer la witch au centre de la pièce {(center_x, center_y)}.")


def generate_and_save_csv():
    """
    Génère une grille de carte, y ajoute des portes, et sauvegarde les fichiers CSV.
    """
    # Génération initiale de la grille
    boundary_grid = [[BOUNDARY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    floor_grid = [[WALKABLE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    # Définir les limites extérieures
    for x in range(GRID_WIDTH):
        boundary_grid[0][x] = BOUNDARY
        boundary_grid[GRID_HEIGHT - 1][x] = BOUNDARY
    for y in range(GRID_HEIGHT):
        boundary_grid[y][0] = BOUNDARY
        boundary_grid[y][GRID_WIDTH - 1] = BOUNDARY

    # Génération des salles et des corridors
    root = RoomPartition(1, 1, GRID_WIDTH - 2, GRID_HEIGHT - 2)
    partitions = [root]
    for _ in range(10):  # Ajustez ce nombre pour contrôler le nombre de divisions
        new_partitions = []
        for partition in partitions:
            if partition.split():
                new_partitions.append(partition.left)
                new_partitions.append(partition.right)
        partitions.extend(new_partitions)

    # Création des salles dans chaque partition
    rooms = []
    for partition in partitions:
        partition.create_room()
        if partition.room:
            create_room(boundary_grid, partition.room)
            rooms.append(partition.room)

    # Connexion des salles par des corridors
    connect_rooms(boundary_grid, root)

    # Placement des portes
    place_doors(boundary_grid)

    # Placement de l'objectif
    spawn = None
    for y, row in enumerate(boundary_grid):
        for x, cell in enumerate(row):
            if cell == DOOR and y + 1 < len(boundary_grid) and boundary_grid[y + 1][x] == FLOOR:
                spawn = (x, y + 1)
                print(f"Spawn trouvé à {spawn}")
                break
        if spawn:
            break
    if spawn:
        place_objective(boundary_grid, spawn)
    else:
        print("Impossible de trouver un spawn pour placer l'objectif.")

    # Sauvegarde des grilles dans des fichiers CSV
    save_csv(boundary_grid, '../map/map_FloorBlocks.csv')
    save_csv(floor_grid, '../map/map_Floor.csv')

    

def save_csv(grid, filename):
    """Save the generated map to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(grid)

# Call the function to generate and save the CSV files
generate_and_save_csv()
