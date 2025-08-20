import pygame, random
from entities.helicopter import Helicopter
from entities.parachute import MilitaryMan
from entities.cannon import Cannon
from entities.bullet import Bullet

pygame.init()

pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("assets/gameover.mp3")
game_over_sound.set_volume(0.7)
pygame.mixer.music.load("assets/bgv.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

cannon = Cannon(400, 550)  # fixed base position (x=400, y=550)
bullet_speed = 15

import time

# Background colors to cycle through
background_colors = [#(255, 255, 255),  # white
                     #(0, 128, 0),      # green
                     #(255, 255, 0).    # yellow
                     (0, 0, 255),      # blue
                     (128, 0, 128),    # purple
                     ]    

current_bg_index = 0
last_color_change_time = time.time()
color_change_interval = 3  # seconds

fire_sound = pygame.mixer.Sound("assets/fire.mp3")
loose_sound = pygame.mixer.Sound("assets/loose.mp3")

game_over_sound_played = False  # Global flag






screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
helicopters = []
military_men = []
bullets = []
bursts = []


score = 0
missed = 0
GAME_OVER_LIMIT = 10
game_over = False


def draw_cannon(surf, x, y):
    import pygame
    # Base platform
    pygame.draw.rect(surf, (100, 100, 100), (x - 30, y, 60, 10))
    pygame.draw.rect(surf, (50, 50, 50), (x - 20, y - 10, 40, 10))
    
    # Double line barrel pointing straight up
    pygame.draw.line(surf, (80, 80, 80), (x - 5, y), (x - 5, y - 50), 4)
    pygame.draw.line(surf, (80, 80, 80), (x + 5, y), (x + 5, y - 50), 4)



def draw_burst(surface, x, y):
    # Simple burst using a yellow circle
        pygame.draw.circle(surface, (255, 255, 0), (x, y), 18)

def random_green_shade():
    return (random.randint(0, 120), random.randint(100, 200), 0)

def random_rope_shade():
    shade = random.randint(100, 150)
    return (shade, shade, shade)

def random_yellow_shade():
    r = random.randint(150, 255)
    g = random.randint(150, 220)
    b = 0
    return (r, g, b)

def random_rotor_shade():
    shade = random.randint(20, 50)
    return (shade, shade, shade)


running = True
while running:
    screen.fill((10, 20, 40))
    # Change background color every 3 seconds
    current_time = time.time()
    if current_time - last_color_change_time > color_change_interval:
        current_bg_index = (current_bg_index + 1) % len(background_colors)
        last_color_change_time = current_time

    screen.fill(background_colors[current_bg_index])

    # Game Over logic and display
    if game_over:
        # Draw final score below the game over text
        final_score_surf = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_surf, (280, 280))

        over_font = pygame.font.SysFont(None, 80)
        over_surf = over_font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(over_surf, (240, 220))
        restart_font = pygame.font.SysFont(None, 40)
        score_font = pygame.font.SysFont(None, 36)
        restart_surf = restart_font.render("Press 'R' to restart", True, (255, 255, 255))
        final_score_surf = score_font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(restart_surf, (270, 320))
        if not game_over_sound_played:
            pygame.mixer.music.stop()
            game_over_sound.play()
            game_over_sound_played = True
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset everything for a new game
                score = 0
                missed = 0
                game_over = False
                helicopters.clear()
                military_men.clear()
                bullets.clear()
                bursts.clear()
        continue  # Skip rest of loop until game is restarted

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Cannon controls (rotate barrel)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_UP]:
            cannon.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
            cannon.move_right()

        # Shoot bullet when SPACE pressed, limit firing rate with cooldown
        if keys[pygame.K_SPACE]:    
            if not bullets or bullets[-1].y < cannon.y - 80:
                cx, cy = cannon.get_barrel_center()
                vx, vy = cannon.get_bullet_velocity(bullet_speed)
                new_bullet = Bullet(cx, cy, vx, vy, radius=4, color=(255, 0, 0))
                bullets.append(new_bullet)
                fire_sound.play()




    # Helicopter spawn
    if random.random() < 0.015:
        body_color = random_yellow_shade()
        rotor_color = random_rotor_shade()
        helicopters.append(Helicopter(800, body_color, rotor_color))

    # Update helicopters, possibly drop targets
    for heli in helicopters[:]:
        heli.move()
        heli.draw(screen)
        drop = heli.maybe_drop()
        if drop:
            man_color = random_green_shade()
            rope_color = random_rope_shade()
            military_men.append(MilitaryMan(drop[0], drop[1], man_color, rope_color))

    # Update military men
    for man in military_men[:]:
        man.move()
        man.draw(screen)
        if man.y > 600:
            military_men.remove(man)
            missed += 1
            loose_sound.play()
            if missed >= GAME_OVER_LIMIT:
                game_over = True


    

    # Bursts (timed display)
    for burst in bursts[:]:
        burst['frames'] -= 1
        draw_burst(screen, burst['x'], burst['y'])
        if burst['frames'] <= 0:
            bursts.remove(burst)

        # Collisions: bullet vs helicopter
    for bullet in bullets[:]:
        bullet_rect = bullet.get_rect()
        for heli in helicopters[:]:
            heli_rect = pygame.Rect(heli.x, heli.y, heli.width, heli.height)
            if bullet_rect.colliderect(heli_rect):
                bursts.append({'x': heli.x+30, 'y': heli.y+15, 'frames': 12})
                helicopters.remove(heli)
                bullets.remove(bullet)
                score += 5
                break

    # Collisions: bullet vs military men
    for bullet in bullets[:]:
        bullet_rect = bullet.get_rect()
        for man in military_men[:]:
            man_rect = pygame.Rect(man.x-8, man.y-8, 16, 16)
            if bullet_rect.colliderect(man_rect):
                bursts.append({'x': man.x, 'y': man.y, 'frames': 12})
                military_men.remove(man)
                bullets.remove(bullet)
                score += 1
                break


    for bullet in bullets[:]:
        bullet.update()
        pygame.draw.circle(screen, bullet.color, bullet.get_pos(), bullet.radius)
        if bullet.is_offscreen(800, 600):
            bullets.remove(bullet)


    cannon.draw(screen)
    # Draw the score and missed counter at the top
    font = pygame.font.SysFont(None, 36)
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    missed_surf = font.render(f"Missed: {missed}/{GAME_OVER_LIMIT}", True, (255, 0, 0))
    screen.blit(score_surf, (16, 10))
    screen.blit(missed_surf, (650, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
