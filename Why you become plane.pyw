import pygame
import sys
import random
import os

pygame.init()
FPS=10
window_size = (900, 700)

screen = pygame.display.set_mode(window_size)

current_time = pygame.time.get_ticks()

subdirectory = "Images"
filename = "explosion.png"
image_path = os.path.join(subdirectory, filename)

#screen_fill = screen.fill((104, 50, 39))
explosion_image = pygame.image.load("images\Bomb.png")

player_pos = (50, 100)
player_vel = (2.5, 3)
#player_vel = (-2.5, 1)
clock = pygame.time.Clock()

GroundHits = 0

# config
position_monitor = False
pause_on_click = False
zoom_cap = False
zoom = False

font = pygame.font.Font(None, 36)

# Set the change back time (in milliseconds)
change_back_time1 = 2000
change_back_time2 = 1000
change_back_start_time = 0
image_changed = False
is_plane = False
is_explode = False
pause_state = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if (player_pos[0] < mouse_pos[0] < player_pos[0] + explosion_image.get_width()) and (player_pos[1] < mouse_pos[1] < player_pos[1] + explosion_image.get_height()):
                if pause_on_click:
                    pause_state = not pause_state
                    if pause_state:
                        player_vel = (random.randint(0, 0), random.randint(0, 0))
                    else:
                        player_vel = (random.randint(-5, 5), random.randint(-5, 5))  
                elif zoom_cap:
                    #player_vel = (random.randint(-20, 20), random.randint(-20, 20))
                    if abs(player_vel[0]) < 100 and abs(player_vel[1]) < 100:
                     player_vel = (player_vel[0] + random.randint(1, 20), player_vel[1] + random.randint(1, 20))
                    else:
                     player_vel = (random.randint(-5, 5), random.randint(-5, 5))
                elif zoom:
                    max_velocity = 100
                    increment = random.randint(1, 20)
                    if player_vel[0] + increment > max_velocity:
                     player_vel = (max_velocity, player_vel[1])
                    else:
                     player_vel = (player_vel[0] + increment, player_vel[1])
                    if player_vel[1] + increment > max_velocity:
                     player_vel = (player_vel[0], max_velocity)
                    else:
                       player_vel = (player_vel[0], player_vel[1] + increment)
                else:
                     player_vel = (random.randint(-5, 5), random.randint(-5, 5))


    if player_pos[0] < 0 or player_pos[0] + explosion_image.get_width() > window_size[0]:
        player_vel = (player_vel[0], -player_vel[1])
#Plane
    if player_pos[0] < 0 or player_pos[0] + explosion_image.get_width() > window_size[0]:
        explosion_image = pygame.image.load("images\plane.png")
        player_vel = (-player_vel[0], -player_vel[1])
        image_changed = True
        is_plane = True
        change_back_start_time = current_time
    
#    elif player_pos[1] < 0:
#       player_vel = (player_vel[0], -player_vel[1])
#
#    player_pos = (player_pos[0] + player_vel[0],
#                     player_pos[1] + player_vel[1])
#    mirrored_image = pygame.transform.flip("images\plane.png", False, True)
#Explosion
    if player_pos[1] + explosion_image.get_height() > window_size[1]:
        explosion_image = pygame.image.load("images\explosion.png")
        player_vel = (player_vel[0], -player_vel[1])
        GroundHits += 1
        # screen_fill = screen.fill ((255, 255, 255))
        image_changed = True
        is_explode = True
        change_back_start_time = current_time

    elif player_pos[1] < 0:
        player_vel = (player_vel[0], -player_vel[1])

    player_pos = (player_pos[0] + player_vel[0],
                     player_pos[1] + player_vel[1])

    screen.fill((104, 50, 39))

    screen.blit(explosion_image, player_pos)

    # Check config to change
    if position_monitor:
        y = 10
        Position_Counter = font.render(
        "Position: (" + str(player_pos[0]) + ", " + str(player_pos[1]) + ")", True, (250, 250, 255))
        screen.blit(Position_Counter, (10, y))
        y += 30
        Velocity_Counter = font.render(
        "Velocity: (" + str(player_vel[0]) + ", " + str(player_vel[1]) + ")", True, (250, 250, 255))
        screen.blit(Velocity_Counter, (10, y))
        y += 30
        Hits_Counter = font.render(
        "Ground Hits: " + str(GroundHits), True, (250, 250, 255))
        screen.blit(Hits_Counter, (10, y))

    else:
        y = 10
        Velocity_Counter = font.render(
        "Velocity: (" + str(player_vel[0]) + ", " + str(player_vel[1]) + ")", True, (250, 250, 255))
        screen.blit(Velocity_Counter, (10, y))
        y += 30
        Hits_Counter = font.render(
        "Ground Hits: " + str(GroundHits), True, (250, 250, 255))
        screen.blit(Hits_Counter, (10, y))

    if image_changed and is_explode:
       if current_time - change_back_start_time >= change_back_time1:
            explosion_image = pygame.image.load("images\\bomb.png")
            # screen_fill = screen.fill ((217, 37, 18))
            is_explode = False
            image_changed = False

    if image_changed and is_plane:
        #if player_pos[0] < 0 or player_pos[0] + explosion_image.get_width() > window_size[0]:
            #player_vel = (-player_vel[0], player_vel[1])
        if current_time - change_back_start_time >= change_back_time2:
            explosion_image = pygame.image.load("images\\bomb.png")
        # screen_fill = screen.fill ((104, 50, 39))
            is_plane = False
            image_changed = False

    pygame.display.flip()

    current_time = pygame.time.get_ticks()

    clock.tick(60)
