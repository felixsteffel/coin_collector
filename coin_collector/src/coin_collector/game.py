import pygame
from .config import load_level

PLAYER_SIZE = 30
PLAYER_SPEED = 4  # px pro Frame

def rect_from_xywh(x, y, w, h) -> pygame.Rect:
    return pygame.Rect(int(x), int(y), int(w), int(h))

def run_game(level_path: str, fps: int = 60, debug: bool = False) -> None:
    lvl = load_level(level_path)

    pygame.init()
    screen = pygame.display.set_mode((lvl.width, lvl.height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    player = pygame.Rect(lvl.player_start.x, lvl.player_start.y, PLAYER_SIZE, PLAYER_SIZE)
    coins = [pygame.Rect(c.x - c.r, c.y - c.r, c.r*2, c.r*2) for c in lvl.coins]
    walls = [rect_from_xywh(w.x, w.y, w.w, w.h) for w in lvl.walls]
    score = 0
    running = True

    while running:
        dt_ms = clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            # Optional: Screenshot mit F12

        # Bewegung
        keys = pygame.key.get_pressed()
        vx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        vy = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])
        # Normierung für diagonale Bewegungen (einfach)
        if vx and vy:
            vx *= 0.7071
            vy *= 0.7071

        # Versuchsbewegung & einfache Kollisionsauflösung (separat pro Achse)
        # X-Achse
        player.x += int(vx * PLAYER_SPEED)
        for w in walls:
            if player.colliderect(w):
                if vx > 0:
                    player.right = w.left
                elif vx < 0:
                    player.left = w.right
        # Y-Achse
        player.y += int(vy * PLAYER_SPEED)
        for w in walls:
            if player.colliderect(w):
                if vy > 0:
                    player.bottom = w.top
                elif vy < 0:
                    player.top = w.bottom

        # Coins einsammeln
        remaining = []
        for c in coins:
            if player.colliderect(c):
                score += 1
            else:
                remaining.append(c)
        coins = remaining

        # Zeichnen
        screen.fill((25, 25, 28))
        # Wände
        for w in walls:
            pygame.draw.rect(screen, (90, 90, 100), w, border_radius=4)
        # Coins
        for c in coins:
            pygame.draw.ellipse(screen, (255, 215, 0), c)
        # Spieler
        pygame.draw.rect(screen, (100, 200, 255), player, border_radius=6)

        # HUD
        text = f"Score: {score} / {score + len(coins)}"
        if debug:
            text += f"  | FPS: {int(clock.get_fps())}"
        img = font.render(text, True, (240, 240, 240))
        screen.blit(img, (10, 8))

        # Gewinn?
        if not coins:
            pygame.display.set_caption("Alle Münzen eingesammelt! ESC zum Beenden.")
        pygame.display.flip()

    pygame.quit()