import pygame
import random
import sys

# אתחול Pygame
pygame.init()

# הגדרות מסך קבועות
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_subplots()[0] if hasattr(pygame, 'set_subplots') else pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("תפוס את התפוחים!")

# צבעים (RGB)
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (34, 139, 34)
BLUE = (50, 153, 213)

# הגדרות שחקן (הסל)
basket_width = 100
basket_height = 20
basket_x = (SCREEN_WIDTH - basket_width) // 2
basket_y = SCREEN_HEIGHT - basket_height - 10
basket_speed = 8

# הגדרות תפוח
apple_size = 30
apple_x = random.randint(0, SCREEN_WIDTH - apple_size)
apple_y = -apple_size
apple_speed = 5

# ניקוד ופסילות
score = 0
lives = 3
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

# לולאת המשחק המרכזית
running = True
while running:
    # 1. ניהול אירועים (Events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. קלט מהמקלדת לתנועת הסל
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < SCREEN_WIDTH - basket_width:
        basket_x += basket_speed

    # 3. עדכון מיקום התפוח
    apple_y += apple_speed

    # בדיקה אם התפוח נגע ברצפה (פספוס)
    if apple_y > SCREEN_HEIGHT:
        lives -= 1
        apple_x = random.randint(0, SCREEN_WIDTH - apple_size)
        apple_y = -apple_size
        if lives <= 0:
            running = False  # המשחק נגמר

    # 4. זיהוי התנגשות (אם הסל תפס את התפוח)
    basket_rect = pygame.Rect(basket_x, basket_y, basket_width, basket_height)
    apple_rect = pygame.Rect(apple_x, apple_y, apple_size, apple_size)

    if basket_rect.colliderect(apple_rect):
        score += 1
        apple_x = random.randint(0, SCREEN_WIDTH - apple_size)
        apple_y = -apple_size
        # העלאת מהירות הדרגתית כדי לאתגר את השחקן
        if score % 5 == 0:
            apple_speed += 1

    # 5. ציור על המסך
    screen.fill(BLUE)  # רקע כחול

    # ציור הסל (מלבן ירוק) והתפוח (מלבן אדום)
    pygame.draw.rect(screen, GREEN, basket_rect)
    pygame.draw.rect(screen, RED, apple_rect)

    # הצגת ניקוד וחיים
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    # עדכון המסך
    pygame.display.flip()
    clock.tick(60)  # הגבלת המשחק ל-60 פריימים בשנייה

# סגירת המשחק
pygame.quit()
sys.exit()
