import pygame, random, time
from entities.helicopter import Helicopter
from entities.parachute import MilitaryMan
from entities.cannon import Cannon
from entities.bullet import Bullet

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))  # Set display mode before image convert
clock = pygame.time.Clock()

# Load and scale background image after display mode set
background_img = pygame.image.load("assets/background.png").convert()
background_img = pygame.transform.scale(background_img, (800, 600))

game_over_sound = pygame.mixer.Sound("assets/gameover.mp3")
game_over_sound.set_volume(0.7)
pygame.mixer.music.load("assets/bgv.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop indefinitely

blast_sound = pygame.mixer.Sound("assets/blast.mp3")  # or blast.wav if you have that file
blast_sound.set_volume(0.7)  # adjust volume as needed


fire_sound = pygame.mixer.Sound("assets/fire.mp3")
loose_sound = pygame.mixer.Sound("assets/loose.mp3")

cannon = Cannon(400, 550)  # Fixed base position
bullet_speed = 15

helicopters = []
military_men = []
bullets = []
bursts = []

score = 0
missed = 0
GAME_OVER_LIMIT = 10
game_over = False
game_over_sound_played = False

game_start_time = time.time()
drop_chance = 0.001  # start very low to slow drops initially
max_drop_chance = 0.02
drop_increase_interval = 30  # seconds
drop_increase_amount = 0.003  # increase this much every interval




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

def draw_burst(surface, x, y):
    pygame.draw.circle(surface, (255, 255, 0), (x, y), 18)

font = pygame.font.SysFont(None, 36)

running = True
while running:
    screen.blit(background_img, (0, 0))

    # Calculate elapsed time in seconds since game start
    elapsed = time.time() - game_start_time

    # Calculate how many 30-second intervals have passed
    intervals = int(elapsed // drop_increase_interval)

    # Update drop chance accordingly
    drop_chance = min(0.001 + intervals * drop_increase_amount, max_drop_chance)


    if game_over:
        final_score_surf = font.render(f"Final Score: {score}", True, (255, 255, 255))
        screen.blit(final_score_surf, (280, 280))

        over_font = pygame.font.SysFont(None, 80)
        over_surf = over_font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(over_surf, (240, 220))
        restart_font = pygame.font.SysFont(None, 40)
        restart_surf = restart_font.render("Press 'R' to restart", True, (255, 255, 255))
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
                score = 0
                missed = 0
                game_over = False
                helicopters.clear()
                military_men.clear()
                bullets.clear()
                bursts.clear()
                game_over_sound_played = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_UP]:
        cannon.move_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_DOWN]:
        cannon.move_right()

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

    # Update helicopters
    for heli in helicopters[:]:
        heli.move()
        heli.draw(screen)

        if heli.spawn_cooldown > 0:
            heli.spawn_cooldown -= 1
            drop = None
        else:
            if random.random() < drop_chance:
                heli.spawn_cooldown = 80
                drop = (heli.x + heli.width//2, heli.y + heli.height)
            else:
                drop = None

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

    # Bursts
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
                blast_sound.play()
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

    # Update and draw bullets
    for bullet in bullets[:]:
        bullet.update()
        pygame.draw.circle(screen, bullet.color, bullet.get_pos(), bullet.radius)
        if bullet.is_offscreen(800, 600):
            bullets.remove(bullet)

    cannon.draw(screen)

    # Draw score and missed
    score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
    missed_surf = font.render(f"Missed: {missed}/{GAME_OVER_LIMIT}", True, (255, 0, 0))
    screen.blit(score_surf, (16, 10))
    screen.blit(missed_surf, (650, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
