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

def generate_and_save_csv():
    """Generate the map using BSP and save it to CSV files."""
    boundary_grid = [[BOUNDARY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    floor_grid = [[WALKABLE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Set outer boundaries
    for x in range(GRID_WIDTH):
        boundary_grid[0][x] = BOUNDARY
        boundary_grid[GRID_HEIGHT - 1][x] = BOUNDARY
    for y in range(GRID_HEIGHT):
        boundary_grid[y][0] = BOUNDARY
        boundary_grid[y][GRID_WIDTH - 1] = BOUNDARY

    # Generate BSP partitions
    root = RoomPartition(1, 1, GRID_WIDTH - 2, GRID_HEIGHT - 2)
    partitions = [root]
    for _ in range(10):  # Adjust the number of splits
        new_partitions = []
        for partition in partitions:
            if partition.split():
                new_partitions.append(partition.left)
                new_partitions.append(partition.right)
        partitions.extend(new_partitions)

    # Create rooms in each partition
    rooms = []
    for partition in partitions:
        partition.create_room()
        if partition.room:
            create_room(boundary_grid, partition.room)
            rooms.append(partition.room)

    # Connect rooms with corridors
    connect_rooms(boundary_grid, root)

    if rooms:
        # Parcourir toute la grille pour trouver 3 murs consécutifs
        for y in range(2, len(boundary_grid)):  # Commence à y=2 pour éviter d'accéder à des indices négatifs pour les lignes au-dessus
            for x in range(len(boundary_grid[0]) - 2):  # S'assurer qu'il reste au moins 2 cases à droite
                if (
                    boundary_grid[y][x] == '395' and
                    boundary_grid[y][x + 1] == '395' and
                    boundary_grid[y][x + 2] == '395'
                ):
                    print(f"Valid wall for door at y={y}, x={x}, x+1={x+1}, x+2={x+2}")

                    # Remplacer ces murs par une porte
                    boundary_grid[y][x] = '99'
                    boundary_grid[y][x + 1] = '99'
                    boundary_grid[y][x + 2] = '99'

                    # Remplacer également les deux lignes au-dessus
                    for offset in range(1, 3):
                        boundary_grid[y - offset][x] = '99'
                        boundary_grid[y - offset][x + 1] = '99'
                        boundary_grid[y - offset][x + 2] = '99'

                    # Stop après avoir placé une porte
                    break
            else:
                continue  # Continue dans la boucle principale si aucune porte n'a été placée
            break





    # Save CSV files
    save_csv(boundary_grid, '../map/map_FloorBlocks.csv')
    save_csv(floor_grid, '../map/map_Floor.csv')
    

def save_csv(grid, filename):
    """Save the generated map to a CSV file."""
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(grid)

# Call the function to generate and save the CSV files
generate_and_save_csv()
