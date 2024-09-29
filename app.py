#Importing all the modules
import pygame
import os
import random
import sys
pygame.init()
pygame.display.set_caption("Malorum")
def animation(screen, folder=None, x=0, y=0, scl=3):
    frames = []
    for frame in sorted(os.listdir(folder)):
        img = pygame.image.load(os.path.join(folder, frame))
        scale = pygame.transform.scale(img, (img.get_width() * scl, img.get_height() * scl))
        frames.append(scale)
    def draw(frame_index):
        frame_index %= len(frames)
        screen.blit(frames[frame_index], (x, y))
    return draw, len(frames)
def bgloader(path):
    return pygame.image.load(path)
def text(screen, text, position, font_size=30, color=(0, 0, 0), align_center=False):
    font = pygame.font.Font("Oswald-SemiBold.ttf", font_size)
    surface = font.render(text, True, color)
    surfrect = surface.get_rect()
    if align_center:
        surfrect.midtop = (screen.get_width()//2, position[1])
    else:
        surfrect.topleft = position
    screen.blit(surface, surfrect.topleft)
    return surface, surfrect
def option(screen, items, font_size=40, gap=20):
    font = pygame.font.Font("Oswald-SemiBold.ttf", font_size)
    buttons = []
    screen_rect = screen.get_rect()
    total_height = len(items) * (font_size + gap)
    start_y = (screen_rect.height - total_height) // 2
    for index, item in enumerate(items):
        text = font.render(item, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_rect.centerx, start_y + index * (font_size + gap))
        screen.blit(text, text_rect)
        buttons.append((item, text_rect))

    return buttons

def win(screen):
    background = bgloader("img/Background/cavelight.png")
    background = pygame.transform.scale(background, screen.get_size())
    clock = pygame.time.Clock()
    running = True
    win_message = "Defeated Mooie successfully, Goodbye"
    display_duration = 3000
    start_time = pygame.time.get_ticks()
    while running:
        screen.blit(background, (0, 0))
        current_time = pygame.time.get_ticks()
        text(screen, win_message, position=(screen.get_width() // 2, screen.get_height() // 2 - 50), font_size=50, color=(0, 0, 0), align_center=True)
        if current_time - start_time > display_duration:
            running = False
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()


    
def main(screen, name):
    running = True
    background = bgloader("img/Background/cavelight.png")
    background = pygame.transform.scale(background, screen.get_size())
    draw_idle_knight, total_idle_knight_frames = animation(screen, f"img/Knight/Idle", 1000, 500, scl=3.5)
    draw_attack_knight, total_attack_knight_frames = animation(screen, f"img/Knight/Attack", 1000, 500, scl=3.5)
    draw_hurt_knight, total_hurt_knight_frames = animation(screen, f"img/Knight/Hurt", 1000, 500, scl=3.5)
    
    draw_idle_monster, total_idle_monster_frames = animation(screen, f"img/{name}", 30, 270, scl=0.8)
    draw_death_monster, total_death_monster_frames = animation(screen, "img/Ghost Death/", 20, 280, scl=0.8 )
    
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_monster_animation = draw_idle_monster
    total_monster_frames = total_idle_monster_frames
    attack_in_progress = False
    monster_hp = 200
    maxattack = 8
    attack = 0
    clock = pygame.time.Clock()
    frame_index_knight = 0
    frame_index_monster = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    monster_dead = False
    knight_health = 100
    monster_attack_punches = random.sample(range(1, maxattack + 1),5)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos) and not monster_dead:
                        if item == "Attack" and not attack_in_progress:
                            current_knight_animation = draw_attack_knight
                            total_knight_frames = total_attack_knight_frames
                            frame_index_knight = 0  
                            attack_in_progress = True 
                            attack += 1
                            monster_hp -= 25  
                            if attack in monster_attack_punches:
                                current_knight_animation = draw_hurt_knight
                                total_attack_knight_frames = total_hurt_knight_frames
                                current_monster_animation = draw_idle_monster
                                total_monster_frames = total_idle_monster_frames
                                frame_index_monster = 0
                                knight_health -= 10
                            if monster_hp > 0 and attack not in monster_attack_punches:
                                current_monster_animation = draw_idle_monster
                                total_monster_frames = total_idle_monster_frames
                                frame_index_monster = 0  
                            elif monster_hp <= 0:
                                defeat_time = pygame.time.get_ticks()
                                current_monster_animation = draw_death_monster
                                total_monster_frames = total_death_monster_frames
                                frame_index_monster = 0
                                monster_dead = True
        screen.blit(background, (0, 0))
        if pygame.time.get_ticks() - start_time > 2000:
            text(screen, "You encountered a Mooie", position=(500, 200), align_center=True)
            if pygame.time.get_ticks() - start_time > 4000:
                options = ["Attack"]
                buttons = option(screen, options, gap=10, font_size=30)
        current_knight_animation(frame_index_knight)
        frame_index_knight = (frame_index_knight + 1) % total_knight_frames
        if attack_in_progress and frame_index_knight == 0:
            current_knight_animation = draw_idle_knight
            total_knight_frames = total_idle_knight_frames
            frame_index_knight = 0
            attack_in_progress = False
            if not monster_dead:
                current_monster_animation = draw_idle_monster
                total_monster_frames = total_idle_monster_frames
        current_monster_animation(frame_index_monster)
        if not monster_dead:
            frame_index_monster = (frame_index_monster + 1) % total_monster_frames
        else:
            frame_index_monster = min(frame_index_monster + 1, total_monster_frames - 1)
        pygame.display.flip()
        if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 500:
            pygame.display.flip()
            break
        clock.tick(10)
screen = pygame.display.set_mode((1366, 736))
names = ['Ghost 1', 'Ghost 2', 'Ghost 3', 'Ghost 4', 'Ghost 5', 'Ghost 6', 'Ghost 7']
for x in names:
    main(screen, x)
win(screen)

