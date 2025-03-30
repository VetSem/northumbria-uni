import pygame
from random import randrange as rnd

class BrickBreaker:
    def __init__(self):
        pygame.init()
        
        self.WIDTH = 1200
        self.HEIGHT = 800
        self.fps = 144

        # Platform settings
        self.platform_w = 150
        self.platform_h = 35
        self.platform_speed = 7.5
        self.platform = pygame.Rect(self.WIDTH // 2 - self.platform_w // 2, self.HEIGHT - self.platform_h - 10, self.platform_w, self.platform_h)

        # Ball settings
        self.ball_radius = 20
        self.ball_speed = 3
        ball_rect = int(self.ball_radius * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(ball_rect, self.WIDTH - ball_rect), self.HEIGHT // 2, ball_rect, ball_rect)
        self.dx, self.dy = 1, -1

        # Blocks settings
        self.block_list = [pygame.Rect(130 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
        self.color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(40)]

        self.sc = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load('bg.jpeg').convert()

    def detect_touch(self, dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left

        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx

        return dx, dy

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.sc.blit(self.img, (0, 0))

            # Drawing world
            [pygame.draw.rect(self.sc, self.color_list[color], block) for color, block in enumerate(self.block_list)]
            pygame.draw.rect(self.sc, pygame.Color('darkorange'), self.platform)
            pygame.draw.circle(self.sc, pygame.Color('white'), self.ball.center, self.ball_radius)

            # Ball movement
            self.ball.x += self.ball_speed * self.dx
            self.ball.y += self.ball_speed * self.dy

            # Collision detection
            if self.ball.centerx < self.ball_radius or self.ball.centerx > self.WIDTH - self.ball_radius:
                self.dx = -self.dx
            if self.ball.centery < self.ball_radius:
                self.dy = -self.dy

            # Platform collision
            if self.ball.colliderect(self.platform) and self.dy > 0:
                self.dx, self.dy = self.detect_touch(self.dx, self.dy, self.ball, self.platform)

            # Block collision
            hit_index = self.ball.collidelist(self.block_list)
            if hit_index != -1:
                hit_rect = self.block_list.pop(hit_index)
                self.color_list.pop(hit_index)
                self.dx, self.dy = self.detect_touch(self.dx, self.dy, self.ball, hit_rect)
                self.fps += 2

            # Game over
            if self.ball.bottom > self.HEIGHT:
                print('Game Over')
                exit()
            elif not len(self.block_list):
                print('WIN!!!')
                exit()

            # Controls
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.platform.left > 0:
                self.platform.left -= self.platform_speed
            if key[pygame.K_RIGHT] and self.platform.right < self.WIDTH:
                self.platform.right += self.platform_speed

            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = BrickBreaker()
    game.start()
