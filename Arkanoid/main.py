import pygame
from random import randrange as rnd

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 144
PLATFORM_WIDTH, PLATFORM_HEIGHT = 150, 35
PLATFORM_SPEED = 7.5
BALL_RADIUS = 20
BALL_SPEED = 3
BLOCK_WIDTH, BLOCK_HEIGHT = 100, 50
BLOCK_COLS, BLOCK_ROWS = 8, 4
BLOCK_PADDING_X, BLOCK_PADDING_Y = 120, 70
BLOCK_START_X, BLOCK_START_Y = 130, 10
BG_IMAGE = 'bg.jpeg'

class BrickBreaker:
    def __init__(self):
        pygame.init()
        self.sc = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Brick Breaker")
        self.clock = pygame.time.Clock()

        # Platform settings
        self.platform = pygame.Rect(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10, PLATFORM_WIDTH, PLATFORM_HEIGHT)

        # Ball settings
        ball_rect = int(BALL_RADIUS * 2 ** 0.5)
        self.ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
        self.dx, self.dy = 1, -1

        # Blocks settings
        self.block_list = []
        self.color_list = []
        self.create_blocks()

        # Load background image
        try:
            self.img = pygame.image.load(BG_IMAGE).convert()
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.img = None

        self.fps = FPS

    def create_blocks(self):
        """Create blocks dynamically."""
        for i in range(BLOCK_COLS):
            for j in range(BLOCK_ROWS):
                block = pygame.Rect(
                    BLOCK_START_X + BLOCK_PADDING_X * i,
                    BLOCK_START_Y + BLOCK_PADDING_Y * j,
                    BLOCK_WIDTH,
                    BLOCK_HEIGHT
                )
                self.block_list.append(block)
                self.color_list.append((rnd(30, 256), rnd(30, 256), rnd(30, 256)))

    def detect_touch(self, dx, dy, ball, rect):
        """Detect collision and adjust ball direction."""
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

    def handle_input(self):
        """Handle user input for platform movement."""
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.platform.left > 0:
            self.platform.left -= PLATFORM_SPEED
        if key[pygame.K_RIGHT] and self.platform.right < WIDTH:
            self.platform.right += PLATFORM_SPEED

    def draw_objects(self):
        """Draw all game objects."""
        if self.img:
            self.sc.blit(self.img, (0, 0))
        else:
            self.sc.fill((0, 0, 0))  # Fallback to black background

        [pygame.draw.rect(self.sc, self.color_list[color], block) for color, block in enumerate(self.block_list)]
        pygame.draw.rect(self.sc, pygame.Color('darkorange'), self.platform)
        pygame.draw.circle(self.sc, pygame.Color('white'), self.ball.center, BALL_RADIUS)

    def update_ball(self):
        """Update ball position and handle collisions."""
        self.ball.x += BALL_SPEED * self.dx
        self.ball.y += BALL_SPEED * self.dy

        # Wall collision
        if self.ball.centerx < BALL_RADIUS or self.ball.centerx > WIDTH - BALL_RADIUS:
            self.dx = -self.dx
        if self.ball.centery < BALL_RADIUS:
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

    def check_game_over(self):
        """Check for game over or win conditions."""
        if self.ball.bottom > HEIGHT:
            print('Game Over')
            return True
        elif not len(self.block_list):
            print('WIN!!!')
            return True
        return False

    def start(self):
        """Main game loop."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.handle_input()
            self.update_ball()
            self.draw_objects()

            if self.check_game_over():
                break

            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = BrickBreaker()
    game.start()