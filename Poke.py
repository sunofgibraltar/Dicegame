import pygame
import random
import math
import time
from pygame import gfxdraw

# Inisialisasi pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dadu Kocok Premium")

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GOLD = (255, 215, 0)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
PURPLE = (128, 0, 128)
COLORS = [RED, BLUE, GREEN, GOLD, PURPLE]

# Font
font_large = pygame.font.SysFont('Arial', 72, bold=True)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Efek partikel
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed = random.uniform(2, 8)
        self.angle = random.uniform(0, 2 * math.pi)
        self.life = random.randint(20, 40)
        self.decay = random.uniform(0.8, 0.95)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= 0.95
        self.size *= self.decay
        self.life -= 1
        
    def draw(self, surface):
        alpha = min(255, self.life * 6)
        color = (*self.color[:3], alpha)
        pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), max(1, int(self.size)), color)

# Kelas Dadu
class Dice:
    def __init__(self, x, y, size=100):
        self.x = x
        self.y = y
        self.size = size
        self.value = 1
        self.rolling = False
        self.roll_time = 0
        self.roll_duration = 2000  # 2 detik
        self.angle = 0
        self.target_angle = 0
        self.particles = []
        self.color = random.choice(COLORS)
        
    def roll(self):
        self.rolling = True
        self.roll_time = pygame.time.get_ticks()
        self.value = random.randint(1, 6)
        self.target_angle = random.uniform(0, 2 * math.pi)
        self.color = random.choice(COLORS)
        
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.rolling:
            progress = (current_time - self.roll_time) / self.roll_duration
            self.angle = self.angle * 0.9 + self.target_angle * 0.1
            
            # Buat partikel saat mengocok
            if random.random() < 0.3:
                px = self.x + random.randint(-self.size//2, self.size//2)
                py = self.y + random.randint(-self.size//2, self.size//2)
                self.particles.append(Particle(px, py, (*self.color, 150)))
            
            if progress >= 1:
                self.rolling = False
                # Ledakan partikel saat selesai
                for _ in range(50):
                    px = self.x + random.randint(-self.size//2, self.size//2)
                    py = self.y + random.randint(-self.size//2, self.size//2)
                    self.particles.append(Particle(px, py, (*self.color, 200)))
        
        # Update partikel
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        # Gambar partikel
        for particle in self.particles:
            particle.draw(surface)
        
        # Gambar dadu
        dice_rect = pygame.Rect(0, 0, self.size, self.size)
        dice_rect.center = (self.x, self.y)
        
        # Rotasi dadu
        dice_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(dice_surface, self.color, (0, 0, self.size, self.size), border_radius=15)
        pygame.draw.rect(dice_surface, WHITE, (0, 0, self.size, self.size), 3, border_radius=15)
        
        # Gambar titik-titik dadu
        dot_color = WHITE
        dot_size = self.size // 10
        
        if self.value in [1, 3, 5]:
            # Titik tengah
            pygame.draw.circle(dice_surface, dot_color, (self.size//2, self.size//2), dot_size)
        
        if self.value in [2, 3, 4, 5, 6]:
            # Titik kiri atas dan kanan bawah
            pygame.draw.circle(dice_surface, dot_color, (self.size//4, self.size//4), dot_size)
            pygame.draw.circle(dice_surface, dot_color, (3*self.size//4, 3*self.size//4), dot_size)
        
        if self.value in [4, 5, 6]:
            # Titik kanan atas dan kiri bawah
            pygame.draw.circle(dice_surface, dot_color, (3*self.size//4, self.size//4), dot_size)
            pygame.draw.circle(dice_surface, dot_color, (self.size//4, 3*self.size//4), dot_size)
        
        if self.value == 6:
            # Titik tengah kiri dan kanan
            pygame.draw.circle(dice_surface, dot_color, (self.size//4, self.size//2), dot_size)
            pygame.draw.circle(dice_surface, dot_color, (3*self.size//4, self.size//2), dot_size)
        
        # Rotasi permukaan dadu
        rotated_dice = pygame.transform.rotate(dice_surface, math.degrees(self.angle))
        rotated_rect = rotated_dice.get_rect(center=dice_rect.center)
        surface.blit(rotated_dice, rotated_rect.topleft)

# Buat dadu
dice = Dice(WIDTH // 2, HEIGHT // 2, 150)

# Tombol
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 100, 200, 60)
button_color = (50, 150, 255)
button_text = font_medium.render("Kocok Dadu", True, WHITE)
button_text_rect = button_text.get_rect(center=button_rect.center)

# Animasi background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.speed = random.uniform(0.1, 0.5)
        self.color = random.choice([(255, 255, 255), (200, 200, 255), (255, 255, 200)])
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

stars = [Star() for _ in range(100)]

# Efek teks
text_alpha = 0
text_surface = None

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)
    
    # Update bintang
    for star in stars:
        star.update()
        star.draw(screen)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos) and not dice.rolling:
                dice.roll()
                text_alpha = 0
    
    # Update dadu
    dice.update()
    dice.draw(screen)
    
    # Gambar tombol
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=10)
    screen.blit(button_text, button_text_rect)
    
    # Efek teks hasil
    if not dice.rolling and dice.value > 0:
        if text_alpha < 255:
            text_alpha = min(255, text_alpha + 5)
        
        text_value = font_large.render(str(dice.value), True, (*WHITE, text_alpha))
        text_value_rect = text_value.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        # Buat surface dengan alpha
        text_surface = pygame.Surface((text_value_rect.width, text_value_rect.height), pygame.SRCALPHA)
        text_surface.blit(text_value, (0, 0))
        screen.blit(text_surface, text_value_rect)
    
    # Petunjuk
    if not dice.rolling:
        hint_text = font_small.render("Klik tombol untuk mengocok dadu", True, WHITE)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()