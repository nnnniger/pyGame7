from lib_load_image import *
import pygame

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

FPS = 50
WIDTH = 500
HEIGHT = 500
STEP = 50
CELL_SIZE = 50

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

level = load_levels(input('Пожалуйста, введите имя файла с картой(желательно 1.txt): '))
for i in range(len(level)):
    level[i] = list(level[i])


class Tile(pygame.sprite.Sprite):
    def __init__(self, obj, x, y, tile_type):
        self.tile_images_and_sprites = {'box': load_image(name='box.png'),
                                        'empty': load_image(name='grass.png'),

                                        }
        super().__init__(tiles_group, all_sprites)
        self.image = self.tile_images_and_sprites[obj]
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.tile_type = tile_type
        self.rect = self.image.get_rect().move(CELL_SIZE * x, CELL_SIZE * y)
        self.rect.x = x * CELL_SIZE
        self.rect.y = y * CELL_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(player_group, all_sprites)
        self.image = load_image(name='mar.png')
        self.rect = self.image.get_rect()
        self.rect.x = x * CELL_SIZE + 15
        self.rect.y = y * CELL_SIZE + 5

    def move(self, dx, dy, tiles_group):
        self.rect.x += dx * 50
        self.rect.y += dy * 50

        for i in pygame.sprite.spritecollide(self, tiles_group, False):
            tile_type = getattr(i, 'tile_type', None)
            if tile_type == 'wall':
                self.rect.x -= dx * 50
                self.rect.y -= dy * 50
            else:
                if dx == -1:
                    move_block_left()
                elif dx == 1:
                    move_block_right()
                elif dy == -1:
                    move_block_up()
                elif dy == 1:
                    move_block_down()


def move_block_left():
    left = []
    for elem in tiles_group:
        left.append([elem.rect.x, elem])
    max_cord = max(map(lambda x: x[0], left))
    for elem in left:
        if elem[1].rect.x == max_cord:
            elem[1].rect.x -= CELL_SIZE * len(level[0])


def move_block_right():
    right = []
    for elem in tiles_group:
        right.append([elem.rect.x, elem])
    min_cord = min(map(lambda x: x[0], right))
    for elem in right:
        if elem[1].rect.x == min_cord:
            elem[1].rect.x += CELL_SIZE * len(level[0])


def move_block_up():
    up = []
    for elem in tiles_group:
        up.append([elem.rect.y, elem])
    max_cord = max(map(lambda x: x[0], up))
    for elem in up:
        if elem[1].rect.y == max_cord:
            elem[1].rect.y -= CELL_SIZE * len(level)


def move_block_down():
    down = []
    for elem in tiles_group:
        down.append([elem.rect.y, elem])
    min_cord = min(map(lambda x: x[0], down))
    for elem in down:
        if elem[1].rect.y == min_cord:
            elem[1].rect.y += CELL_SIZE * len(level)


def generate_levels(level):
    player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, 'empty')
            elif level[y][x] == "@":
                Tile('empty', x, y, 'empty')
                player = Player(x, y)
            elif level[y][x] == "#":
                Tile('box', x, y, 'wall')
    return player, x, y
