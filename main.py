import pygame
import random
import math
import sys
import os

# --- PERFORMANS VE GÖRSEL AYARLAR ---
FPS = 0 
BG_COLOR = (2, 2, 10)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 220, 255)
NEON_PURPLE = (180, 0, 255)
NEON_GREEN = (40, 255, 120)
GOLD = (255, 215, 0)

# Rekor dosyası (İsmini sabit tutuyoruz ki silinmesin)
REKOR_DOSYASI = "rekor_verisi.txt"

def rekoru_oku():
    if not os.path.exists(REKOR_DOSYASI):
        return 0
    try:
        with open(REKOR_DOSYASI, "r") as f:
            content = f.read().strip()
            return int(float(content)) if content else 0
    except:
        return 0

def rekoru_kaydet(yeni_rekor):
    try:
        with open(REKOR_DOSYASI, "w") as f:
            f.write(str(int(yeni_rekor)))
    except:
        pass

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock()
        # Yazı tiplerini büyüttük ki rahat görünsün
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.yuksek_skor = rekoru_oku()
        self.state = "START"
        self.reset()

    def reset(self):
        self.player_pos = pygame.math.Vector2(self.WIDTH // 2, self.HEIGHT // 2)
        self.player_vel = pygame.math.Vector2(0, 0)
        self.platforms = [pygame.math.Vector2(random.randint(100, self.WIDTH-100), self.HEIGHT - (i * 180)) for i in range(15)]
        self.score = 0
        self.is_hooked = False
        self.hook_target = None
        self.bh_y = self.HEIGHT + 500 

    def update(self, dt):
        if self.state != "PLAYING": return
        
        # Fizik
        self.player_vel.y += 0.45 * dt
        
        # Kenarlardan sekme
        if self.player_pos.x <= 20:
            self.player_vel.x = abs(self.player_vel.x) + 5
            self.player_pos.x = 21
        elif self.player_pos.x >= self.WIDTH - 20:
            self.player_vel.x = -abs(self.player_vel.x) - 5
            self.player_pos.x = self.WIDTH - 21

        # Kontrol (Hook/Çengel)
        if pygame.mouse.get_pressed()[0]:
            if not self.is_hooked:
                closest, m_dist = None, 600
                for p in self.platforms:
                    d = self.player_pos.distance_to(p)
                    if d < m_dist and p.y < self.player_pos.y:
                        m_dist, closest = d, p
                if closest: 
                    self.hook_target, self.is_hooked = closest, True
            if self.is_hooked:
                pull = (self.hook_target - self.player_pos).normalize() * (2.2 * dt)
                self.player_vel += pull
        else:
            self.is_hooked = False

        self.player_vel *= 0.98
        self.player_pos += self.player_vel * dt

        # --- KAMERA VE METRE SAYACI ---
        cam_margin_top = self.HEIGHT * 0.4
        cam_margin_bottom = self.HEIGHT * 0.7
        
        diff = 0
        if self.player_pos.y < cam_margin_top:
            diff = cam_margin_top - self.player_pos.y
        elif self.player_pos.y > cam_margin_bottom:
            diff = cam_margin_bottom - self.player_pos.y

        if diff != 0:
            self.player_pos.y += diff
            self.bh_y += diff
            for p in self.platforms: 
                p.y += diff
            
            # Skor sadece yukarı (pozitif diff) giderken artar
            if diff > 0:
                self.score += int(diff // 5) # Hassasiyeti artırmak için 5'e böldük

        # Rekor anlık kontrol
        if self.score > self.yuksek_skor:
            self.yuksek_skor = self.score

        # Platform üretimi
        if self.platforms[0].y > self.HEIGHT + 400:
            self.platforms.pop(0)
            self.platforms.append(pygame.math.Vector2(random.randint(50, self.WIDTH-50), self.platforms[-1].y - 180))

        # Kara Delik Hareketi
        self.bh_y -= (2.2 + (self.score / 2000)) * dt
        
        # Ölüm durumu
        if self.player_pos.y > self.bh_y:
            rekoru_kaydet(self.yuksek_skor)
            self.state = "GAMEOVER"

    def draw(self):
        self.screen.fill(BG_COLOR)

        # Kara Delik Girdabı
        for i in range(10):
            r = int(self.WIDTH + 300 - (i * 60))
            if r > 0:
                pygame.draw.ellipse(self.screen, (max(0, 50-i*5), 0, max(0, 100-i*10)), 
                                    (-150, int(self.bh_y + i*15), self.WIDTH + 300, r // 2), 2)

        # Platformlar
        for p in self.platforms:
            pygame.draw.circle(self.screen, NEON_GREEN, (int(p.x), int(p.y)), 12)
            pygame.draw.circle(self.screen, WHITE, (int(p.x), int(p.y)), 14, 1)

        # Çengel İpi
        if self.is_hooked and self.hook_target:
            pygame.draw.line(self.screen, NEON_BLUE, (int(self.player_pos.x), int(self.player_pos.y)), 
                             (int(self.hook_target.x), int(self.hook_target.y)), 3)

        # Karakter
        pygame.draw.circle(self.screen, WHITE, (int(self.player_pos.x), int(self.player_pos.y)), 15)
        pygame.draw.circle(self.screen, NEON_BLUE, (int(self.player_pos.x), int(self.player_pos.y)), 18, 3)

        # --- UI (METRE VE REKOR) ---
        score_surf = self.font.render(f"METRE: {self.score}", True, WHITE)
        rekor_surf = self.font.render(f"REKOR: {self.yuksek_skor}", True, GOLD)
        fps_surf = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (0, 255, 0))
        
        self.screen.blit(score_surf, (40, 50))
        self.screen.blit(rekor_surf, (40, 100))
        self.screen.blit(fps_surf, (self.WIDTH - 150, 50))

        if self.state != "PLAYING":
            txt = "BAŞLAMAK İÇİN DOKUN" if self.state == "START" else "YENİLDİN! TEKRAR DOKUN"
            surf = self.font.render(txt, True, WHITE)
            rect = surf.get_rect(center=(self.WIDTH//2, self.HEIGHT//2))
            self.screen.blit(surf, rect)

        pygame.display.flip()

    def run(self):
        while True:
            # Delta Time (dt)
            tick = self.clock.tick(FPS)
            dt = tick * 0.06 
            # dt çok büyürse (lag olursa) fizik patlamasın diye sınırlıyoruz
            dt = min(dt, 2.0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    rekoru_kaydet(self.yuksek_skor)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state != "PLAYING":
                        self.reset()
                        self.state = "PLAYING"
            
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    Game().run()
