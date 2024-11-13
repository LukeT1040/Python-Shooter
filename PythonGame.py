import pygame
import random
import sys
import math

# Initialize pygame
pygame.init()

# Screen bounds and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup the screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Framerate setup
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 30)

# Shop System Function
def shop(player, score, lives):
    running = True
    options = ["Speed +1 (Cost: 10)", "Damage +1 (Cost: 10)", "Lives +1 (Cost: 15)", "Exit Shop"]
    selection = 0
    font = pygame.font.SysFont("Arial", 25)

    while running:
        SCREEN.fill(WHITE)

        # Draw shop items
        title = font.render("SHOP", True, BLACK)
        SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        for i, option in enumerate(options):
            color = BLACK if i != selection else (255, 0, 0)
            text = font.render(option, True, color)
            SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 + i * 40))

        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selection == 0 and score >= 10:  # Speed upgrade
                        player.speed += 1
                        score -= 10
                    elif selection == 1 and score >= 10:  # Damage upgrade
                        player.bullet_damage += 1
                        score -= 10
                    elif selection == 2 and score >= 15 and lives < 3:  # Lives upgrade
                        lives += 1
                        score -= 15
                    elif selection == 3:  # Exit shop
                        running = False

    return score, lives

def main_menu():
    running = True
    options = ["Start Game", "Instructions", "Quit"]
    selection = 0
    menu_font = pygame.font.SysFont("Arial", 40)

    while running:
        SCREEN.fill(WHITE)

        # Title
        title = menu_font.render("Main Menu", True, BLACK)
        SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # Options
        for i, option in enumerate(options):
            color = BLACK if i != selection else (255, 0, 0)
            text = menu_font.render(option, True, color)
            SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 60))

        pygame.display.flip()

        # Handle input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selection == 0:  # Start Game
                        running = False
                    elif selection == 1:  # Instructions
                        instructions()
                    elif selection == 2:  # Quit
                        pygame.quit()
                        sys.exit()

# Instructions Function
def instructions():
    running = True
    instructions_font = pygame.font.SysFont("Arial", 30)
    instructions_text = [
        "Use the arrow keys to move your player.",
        "Press SPACE to shoot bullets.",
        "Collect coins for points and shop upgrades.",
        "Defeat enemies and avoid their bullets.",
        "Press ESC to return to the main menu."
    ]

    while running:
        SCREEN.fill(WHITE)

        # Title
        title = instructions_font.render("Instructions", True, BLACK)
        SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        # Display instructions
        for i, line in enumerate(instructions_text):
            text = instructions_font.render(line, True, BLACK)
            SCREEN.blit(text, (50, 150 + i * 40))

        # Footer
        footer = instructions_font.render("Press ESC to return to the Main Menu", True, BLACK)
        SCREEN.blit(footer, (SCREEN_WIDTH // 2 - footer.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/standing-still.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.speed = 5
        self.bullet_damage = 1
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_damage)
        self.bullet_group.add(bullet)
        return bullet


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.image = pygame.image.load("assets/bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 20))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7
        self.damage = damage

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.image.load("assets/ufo_game_enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 3)
        self.health = 1 + level  # Enemy health increases with level

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        return bullet



class Boss(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.image.load("assets/boss2.png")
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, -100)
        self.health = 50 + level * 10
        self.speed = 2
        self.attack_timer = 0
        self.attack_rate = 100  # Frames between attacks
        self.level = level

    def update(self):
        # Move down into position, then oscillate
        if self.rect.top < 100:
            self.rect.y += self.speed
        else:
            self.rect.x += self.speed if random.random() > 0.5 else -self.speed

        # Change direction at edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed = -self.speed

        # Attack logic
        self.attack_timer += 1
        if self.attack_timer >= self.attack_rate:
            self.attack_timer = 0
            self.shoot()

    def shoot(self):
        # Boss fires a spread of bullets
        for angle in [-30, 0, 30]:
            bullet = BossBullet(self.rect.centerx, self.rect.bottom, angle)
             
            return bullet

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()


class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((0, 255, 0))  # Green bullets for the boss
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.angle = angle

    def update(self):
        # Move bullet in the specified angle
        self.rect.x += self.speed * math.sin(math.radians(self.angle))
        self.rect.y += self.speed * math.cos(math.radians(self.angle))
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# EnemyBullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laserBullet.png")
        self.image = pygame.transform.scale(self.image, (10, 20))
        self.image.fill((0, 0, 255))  # Blue bullet for enemies
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, SCREEN_WIDTH - 100)
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 100)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        if kind == "speed":
            self.image = pygame.image.load("assets/wingboots.gif")
            self.image = pygame.transform.scale(self.image, (60, 60))
        elif kind == "heal":
            self.image = pygame.image.load("assets/heart.png")
            self.image = pygame.transform.scale(self.image, (60, 60))
        self.kind = kind
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# Setup the level
def setup_level(level):
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    coins = pygame.sprite.Group()
    for _ in range(level * 3):
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    return player, all_sprites, coins



def show_achievement(text):
    achievement_font = pygame.font.SysFont("Arial", 30)
    achievement_text = achievement_font.render(text, True, (0, 255, 0))
    SCREEN.blit(achievement_text, (SCREEN_WIDTH // 2 - achievement_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 2 seconds

# Game loop
def main():
    high_score = 0

    # Load high score from a file
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0

    while True:  # Restart loop
        main_menu()
        level = 1
        score = 0
        lives = 3
        achievements = {
            "first_coin": False,
            "first_boss": False,
            "score_100": False
            }

        while lives > 0:  # Lives loop
            player, all_sprites, coins = setup_level(level)
            enemies = pygame.sprite.Group()
            spawn_timer = 0
            spawn_rate = 30

            running = True
            enemies_bullets = pygame.sprite.Group()
            power_ups = pygame.sprite.Group()

            if level % 5 == 0:  # Boss level logic
                boss = Boss(level)
                all_sprites.add(boss)
                boss_group = pygame.sprite.Group()
                boss_group.add(boss)
                boss_bullets = pygame.sprite.Group()
                attack_timer = 0
                attack_rate = 100

                while boss.alive() and lives > 0:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            with open("highscore.txt", "w") as f:
                                f.write(str(high_score))
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                bullet = player.shoot()
                                all_sprites.add(bullet)

                    # Update all sprites
                    all_sprites.update()
                    attack_timer += 1
                    if attack_timer >= attack_rate:
                        attack_timer = 0  # Reset the timer
                        # Boss fires bullets
                        for angle in [-30, 0, 30]:  # Spread of 3 bullets
                            bullet = BossBullet(boss.rect.centerx, boss.rect.bottom, angle)
                            boss_bullets.add(bullet)  # Add bullet to the boss_bullets group
                            all_sprites.add(bullet)   # Add to all_sprites so it's updated and drawn
                        
                    for bullet in boss_bullets:
                        bullet.update()
                        SCREEN.blit(bullet.image, bullet.rect)

                    # Boss shooting logic
                    for bullet in player.bullet_group:
                        if pygame.sprite.spritecollide(bullet, boss_group, False):
                            boss.take_damage(bullet.damage)
                            bullet.kill()

                    if pygame.sprite.spritecollide(player, boss_bullets, True):
                        lives -= 1

                    # Draw everything
                    SCREEN.fill(WHITE)
                    all_sprites.draw(SCREEN)
                    player.bullet_group.draw(SCREEN)

                    # Boss health bar
                    pygame.draw.rect(SCREEN, (255, 0, 0), (SCREEN_WIDTH // 2 - 150, 20, 300, 20))
                    pygame.draw.rect(SCREEN, (0, 255, 0), (SCREEN_WIDTH // 2 - 150, 20, 300 * (boss.health / (50 + level * 10)), 20))

                    # UI elements
                    score_text = font.render(f"Score: {score}", True, BLACK)
                    level_text = font.render(f"Level: {level}", True, BLACK)
                    lives_text = font.render(f"Lives: {lives}", True, BLACK)
                    SCREEN.blit(score_text, (10, 10))
                    SCREEN.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
                    SCREEN.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 50))

                    pygame.display.flip()
                    clock.tick(60)

                if not boss.alive():
                    
                    score += 50  # Bonus score for defeating boss
                    level += 1  # Advance level after defeating boss
                    
                

            else:  # Regular levels
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            with open("highscore.txt", "w") as f:
                                f.write(str(high_score))
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                bullet = player.shoot()
                                all_sprites.add(bullet)

                    # Update all sprites
                    all_sprites.update()

                    spawn_rate = max(15, 50 - level * 3)
                    spawn_timer += 1

                    if spawn_timer >= spawn_rate:
                        spawn_timer = 0
                        enemy = Enemy(level)
                        enemies.add(enemy)
                        all_sprites.add(enemy)

                    for enemy in enemies:
                        if random.random() < 0.02 + (level * 0.005):
                            bullet = enemy.shoot()
                            enemies_bullets.add(bullet)
                            all_sprites.add(bullet)

                    if random.random() < 0.01:
                        kind = random.choice(["speed", "heal"])
                        power_up = PowerUp(random.randint(0, SCREEN_WIDTH), -30, kind)
                        power_ups.add(power_up)
                        all_sprites.add(power_up)

                    power_up_collected = pygame.sprite.spritecollide(player, power_ups, True)
                    for power_up in power_up_collected:
                        if power_up.kind == "speed":
                            player.speed += 3
                        elif power_up.kind == "heal" and lives < 3:
                            lives += 1

                    coins_collected = pygame.sprite.spritecollide(player, coins, True)
                    for coin in coins_collected:
                        score += 1

                    if pygame.sprite.spritecollide(player, enemies_bullets, True):
                        lives -= 1
                        running = False

                    if pygame.sprite.spritecollide(player, enemies, False):
                        lives -= 1
                        running = False

                    for bullet in player.bullet_group:
                        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
                        for enemy in hit_enemies:
                            bullet.kill()
                            enemy.take_damage(bullet.damage)
                            if enemy.health <= 0:
                                score += 5

                    if len(coins) == 0:
                        level += 1
                        score, lives = shop(player, score, lives)
                        break

                    # Draw everything
                    SCREEN.fill(WHITE)
                    all_sprites.draw(SCREEN)
                    player.bullet_group.draw(SCREEN)
                    # Achievement: Collect first coin
                    if not achievements["first_coin"] and pygame.sprite.spritecollide(player, coins, True):
                        achievements["first_coin"] = True
                        show_achievement("Achievement Unlocked: First Coin!")

                    # Achievement: Score reaches 100
                    if not achievements["score_100"] and score >= 100:
                        achievements["score_100"] = True
                        show_achievement("Achievement Unlocked: Score 100!")

                    # Boss Level Achievements
                    if level % 5 == 0 and not achievements["first_boss"] and not boss.alive():
                        achievements["first_boss"] = True
                        show_achievement("Achievement Unlocked: First Boss Defeated!")
                    score_text = font.render(f"Score: {score}", True, BLACK)
                    level_text = font.render(f"Level: {level}", True, BLACK)
                    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
                    lives_text = font.render(f"Lives: {lives}", True, BLACK)

                    SCREEN.blit(score_text, (10, 10))
                    SCREEN.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))
                    SCREEN.blit(high_score_text, (10, 50))
                    SCREEN.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 50))

                    pygame.display.flip()
                    clock.tick(60)

        if score > high_score:
            high_score = score


if __name__ == "__main__":
    main()