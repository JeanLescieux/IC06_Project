import random
import csv
from settings import WIDTH, HEIGTH, TILESIZE

# Constants for generation
GRID_WIDTH = WIDTH // TILESIZE
GRID_HEIGHT = HEIGTH // TILESIZE
MIN_ROOM_SIZE = 5
MAX_ROOM_SIZE = 10
ROOM_MARGIN = 1

# Tile types
BOUNDARY = '395'
WALKABLE = '-1'
WALL = '1'
FLOOR = '0'

# Partition class
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
        """Split the partition."""
        if self.left or self.right:
            return False

        if self.width > MIN_ROOM_SIZE * 2 and self.height > MIN_ROOM_SIZE * 2:
            if self.width > self.height:
                split_line = random.randint(MIN_ROOM_SIZE + ROOM_MARGIN, self.width - MIN_ROOM_SIZE - ROOM_MARGIN)
                self.left = RoomPartition(self.x, self.y, split_line, self.height)
                self.right = RoomPartition(self.x + split_line, self.y, self.width - split_line, self.height)
            else:
                split_line = random.randint(MIN_ROOM_SIZE + ROOM_MARGIN, self.height - MIN_ROOM_SIZE - ROOM_MARGIN)
                self.left = RoomPartition(self.x, self.y, self.width, split_line)
                self.right = RoomPartition(self.x, self.y + split_line, self.width, self.height - split_line)
            return True
        return False

    def create_room(self):
        """Create a room in the partition."""
        room_width = random.randint(MIN_ROOM_SIZE, min(self.width - 2 * ROOM_MARGIN, MAX_ROOM_SIZE))
        room_height = random.randint(MIN_ROOM_SIZE, min(self.height - 2 * ROOM_MARGIN, MAX_ROOM_SIZE))
        room_x = random.randint(self.x + ROOM_MARGIN, self.x + self.width - room_width - ROOM_MARGIN)
        room_y = random.randint(self.y + ROOM_MARGIN, self.y + self.height - room_height - ROOM_MARGIN)
        self.room = (room_x, room_y, room_width, room_height)

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
    boundary_grid = [[BOUNDARY for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    floor_grid = [[WALKABLE for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    # Define outer boundaries
    for x in range(GRID_WIDTH):
        boundary_grid[0][x] = BOUNDARY
        boundary_grid[GRID_HEIGHT - 1][x] = BOUNDARY
    for y in range(GRID_HEIGHT):
        boundary_grid[y][0] = BOUNDARY
        boundary_grid[y][GRID_WIDTH - 1] = BOUNDARY

    # Generate BSP partitions
    root = RoomPartition(1, 1, GRID_WIDTH - 2, GRID_HEIGHT - 2)
    partitions = [root]
    for _ in range(10):
        new_partitions = []
        for partition in partitions:
            if partition.split():
                new_partitions.append(partition.left)
                new_partitions.append(partition.right)
        partitions.extend(new_partitions)

    # Create rooms
    rooms = []
    for partition in partitions:
        partition.create_room()
        if partition.room:
            create_room(boundary_grid, partition.room)
            rooms.append(partition.room)

    # Connect rooms
    connect_rooms(boundary_grid, root)

    # Place player in the center of the first room
    if rooms:
        player_x = rooms[0][0] + rooms[0][2] // 2
        player_y = rooms[0][1] + rooms[0][3] // 2
        boundary_grid[player_y][player_x] = FLOOR  # Place player in walkable space

    # Save CSV files
    save_csv(boundary_grid, '../map/map_FloorBlocks.csv')
    save_csv(floor_grid, '../map/map_Floor.csv')

def save_csv(grid, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(grid)

generate_and_save_csv()
