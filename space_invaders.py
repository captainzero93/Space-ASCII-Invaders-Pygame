import pygame
import sys
import random
import numpy as np

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)

# ASCII Art
PLAYER_ASCII = [
    "  ^  ",
    " /|\\ ",
    "/_|_\\"
]

ALIEN_ASCII_1 = [
    " /o\\ ",
    "<___>",
    " | | "
]

ALIEN_ASCII_2 = [
    " \\o/ ",
    "<___>",
    " | | "
]

BULLET_ASCII = "|"
ALIEN_BULLET_ASCII = "v"

# Sound generation functions
def generate_beep(frequency=440, duration=0.1):
    """Generate a simple beep sound"""
    sample_rate = 22050
    n_samples = int(round(duration * sample_rate))
    
    # Generate sine wave
    buf = np.sin(2 * np.pi * np.arange(n_samples) * frequency / sample_rate)
    
    # Apply envelope to prevent clicking
    envelope = np.ones(n_samples)
    fade_len = int(sample_rate * 0.01)  # 10ms fade
    envelope[:fade_len] = np.linspace(0, 1, fade_len)
    envelope[-fade_len:] = np.linspace(1, 0, fade_len)
    buf = buf * envelope
    
    # Convert to 16-bit integer
    buf = (buf * 32767).astype(np.int16)
    
    # Make stereo
    buf = np.column_stack((buf, buf))
    
    return pygame.sndarray.make_sound(buf)

def generate_shoot_sound():
    """Generate a shooting sound (descending tone)"""
    sample_rate = 22050
    duration = 0.15
    n_samples = int(round(duration * sample_rate))
    
    # Descending frequency from 800 to 200 Hz
    frequencies = np.linspace(800, 200, n_samples)
    phase = np.cumsum(2 * np.pi * frequencies / sample_rate)
    buf = np.sin(phase) * 0.3
    
    # Apply envelope
    envelope = np.linspace(1, 0, n_samples)
    buf = buf * envelope
    
    # Convert to 16-bit integer
    buf = (buf * 32767).astype(np.int16)
    buf = np.column_stack((buf, buf))
    
    return pygame.sndarray.make_sound(buf)

def generate_alien_shoot_sound():
    """Generate an alien shooting sound (ascending tone)"""
    sample_rate = 22050
    duration = 0.15
    n_samples = int(round(duration * sample_rate))
    
    # Ascending frequency from 200 to 600 Hz
    frequencies = np.linspace(200, 600, n_samples)
    phase = np.cumsum(2 * np.pi * frequencies / sample_rate)
    buf = np.sin(phase) * 0.25
    
    # Apply envelope
    envelope = np.linspace(1, 0, n_samples)
    buf = buf * envelope
    
    # Convert to 16-bit integer
    buf = (buf * 32767).astype(np.int16)
    buf = np.column_stack((buf, buf))
    
    return pygame.sndarray.make_sound(buf)

def generate_move_sound():
    """Generate alien movement sound (low beep)"""
    return generate_beep(frequency=150, duration=0.05)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.speed = 5
        self.ascii_art = PLAYER_ASCII
        
    def move_left(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = 0
            
    def move_right(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
    def draw(self, screen, font):
        y_offset = 0
        for line in self.ascii_art:
            text = font.render(line, True, GREEN)
            screen.blit(text, (self.x, self.y + y_offset))
            y_offset += 15

class Bullet:
    def __init__(self, x, y, speed=-8):
        self.x = x
        self.y = y
        self.speed = speed
        self.active = True
        self.width = 10
        self.height = 15
        
    def update(self):
        self.y += self.speed
        if self.y < 0 or self.y > SCREEN_HEIGHT:
            self.active = False
            
    def draw(self, screen, font):
        if self.speed < 0:
            text = font.render(BULLET_ASCII, True, CYAN)
        else:
            text = font.render(ALIEN_BULLET_ASCII, True, RED)
        screen.blit(text, (self.x, self.y))

class Alien:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 40
        self.alive = True
        self.ascii_art = ALIEN_ASCII_1
        self.animation_counter = 0
        
    def update_animation(self):
        self.animation_counter += 1
        if self.animation_counter % 30 < 15:
            self.ascii_art = ALIEN_ASCII_1
        else:
            self.ascii_art = ALIEN_ASCII_2
            
    def draw(self, screen, font):
        if not self.alive:
            return
        y_offset = 0
        for line in self.ascii_art:
            text = font.render(line, True, WHITE)
            screen.blit(text, (self.x, self.y + y_offset))
            y_offset += 15

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ASCII Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.score_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        
        # Generate sounds
        self.shoot_sound = generate_shoot_sound()
        self.alien_shoot_sound = generate_alien_shoot_sound()
        self.move_sound = generate_move_sound()
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.bullets = []
        self.alien_bullets = []
        self.aliens = []
        self.alien_direction = 1
        self.alien_speed = 1
        self.alien_move_down = False
        self.score = 0
        self.game_over = False
        self.you_win = False
        self.shoot_cooldown = 0
        self.alien_shoot_timer = 0
        self.move_sound_timer = 0
        
        self.create_aliens()
        
    def create_aliens(self):
        self.aliens = []
        rows = 3
        cols = 7
        spacing_x = 100
        spacing_y = 80
        offset_x = 50
        offset_y = 30
        
        for row in range(rows):
            for col in range(cols):
                x = offset_x + col * spacing_x
                y = offset_y + row * spacing_y
                self.aliens.append(Alien(x, y))
                
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = 20
            
    def shoot(self):
        bullet = Bullet(self.player.x + 20, self.player.y)
        self.bullets.append(bullet)
        self.shoot_sound.play()
        
    def alien_shoot(self):
        # Find aliens in the bottom row that are alive
        bottom_aliens = []
        for alien in self.aliens:
            if alien.alive:
                # Check if there's no alien below this one
                is_bottom = True
                for other in self.aliens:
                    if other.alive and other.x == alien.x and other.y > alien.y:
                        is_bottom = False
                        break
                if is_bottom:
                    bottom_aliens.append(alien)
        
        if bottom_aliens and random.random() < 0.02:
            shooter = random.choice(bottom_aliens)
            bullet = Bullet(shooter.x + 20, shooter.y + 40, speed=6)
            self.alien_bullets.append(bullet)
            self.alien_shoot_sound.play()
            
    def update_aliens(self):
        # Update animation
        for alien in self.aliens:
            alien.update_animation()
        
        # Play movement sound periodically
        self.move_sound_timer += 1
        alive_count = sum(1 for alien in self.aliens if alien.alive)
        # Speed up the sound as fewer aliens remain
        sound_interval = max(10, 30 - (21 - alive_count))
        
        if self.move_sound_timer >= sound_interval:
            self.move_sound.play()
            self.move_sound_timer = 0
        
        # Move aliens
        move_down = False
        for alien in self.aliens:
            if alien.alive:
                alien.x += self.alien_direction * self.alien_speed
                
                # Check if any alien hit the edge
                if alien.x <= 0 or alien.x >= SCREEN_WIDTH - alien.width:
                    move_down = True
        
        if move_down:
            self.alien_direction *= -1
            for alien in self.aliens:
                if alien.alive:
                    alien.y += 20
                    
                    # Check if aliens reached the player
                    if alien.y >= self.player.y:
                        self.game_over = True
        
        # Increase speed as aliens are destroyed
        if alive_count > 0:
            self.alien_speed = 1 + (21 - alive_count) * 0.15
            
    def update_bullets(self):
        # Update player bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
                
        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update()
            if not bullet.active:
                self.alien_bullets.remove(bullet)
                
    def check_collisions(self):
        # Player bullets hitting aliens
        for bullet in self.bullets[:]:
            for alien in self.aliens:
                if alien.alive and bullet.active:
                    if (alien.x < bullet.x < alien.x + alien.width and
                        alien.y < bullet.y < alien.y + alien.height):
                        alien.alive = False
                        bullet.active = False
                        self.score += 10
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        break
        
        # Alien bullets hitting player
        for bullet in self.alien_bullets[:]:
            if bullet.active:
                if (self.player.x < bullet.x < self.player.x + self.player.width and
                    self.player.y < bullet.y < self.player.y + self.player.height):
                    self.game_over = True
        
        # Check if all aliens are destroyed
        if all(not alien.alive for alien in self.aliens):
            self.you_win = True
            
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw player
        self.player.draw(self.screen, self.font)
        
        # Draw aliens
        for alien in self.aliens:
            alien.draw(self.screen, self.font)
            
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen, self.font)
            
        for bullet in self.alien_bullets:
            bullet.draw(self.screen, self.font)
            
        # Draw score
        score_text = self.score_font.render(f"Score: {self.score}", True, GREEN)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over or win message
        if self.game_over:
            game_over_text = self.score_font.render("GAME OVER - Press R to Restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        elif self.you_win:
            win_text = self.score_font.render("YOU WIN! - Press R to Restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(win_text, text_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.you_win):
                        self.__init__()
                        
            if not self.game_over and not self.you_win:
                self.handle_input()
                self.update_aliens()
                self.update_bullets()
                self.alien_shoot()
                self.check_collisions()
                
                if self.shoot_cooldown > 0:
                    self.shoot_cooldown -= 1
                    
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
