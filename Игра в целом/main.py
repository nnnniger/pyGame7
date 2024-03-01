from map import *

import pygame

pygame.init()
pygame.key.set_repeat(200, 70)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Перемещение героя. Новый уровень')
clock = pygame.time.Clock()


def start_game():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    coords_y = 125
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        coords_y += 5
        intro_rect.top = coords_y
        intro_rect.x = 111
        coords_y += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj_sprite):
        obj_sprite.rect.x += self.dx
        obj_sprite.rect.y += self.dy

    def update(self, tracker_obj):
        self.dx = -(tracker_obj.rect.x + tracker_obj.rect.w // 2 - WIDTH // 2)
        self.dy = -(tracker_obj.rect.y + tracker_obj.rect.h // 2 - HEIGHT // 2)


start_game()

player, all_x, all_y = generate_levels(level)
camera = Camera()
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move(0, -1, tiles_group)
            if event.key == pygame.K_DOWN:
                player.move(0, 1, tiles_group)
            if event.key == pygame.K_LEFT:
                player.move(-1, 0, tiles_group)
            if event.key == pygame.K_RIGHT:
                player.move(1, 0, tiles_group)

    camera.update(player)
    for elem in all_sprites:
        camera.apply(elem)

    all_sprites.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
