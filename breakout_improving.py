import pygame
import sys
import math
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
LIGHT_BLUE = (100, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
PADDLE_SPEED = 8
BALL_SIZE = 10
BALL_SPEED = 6
BLOCK_WIDTH = 18
BLOCK_HEIGHT = 12
BLOCK_PADDING = 1

class Ball:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.dx = float(BALL_SPEED)
        self.dy = float(-BALL_SPEED)
        self.size = BALL_SIZE
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        
        # Bounce off walls
        if self.x <= self.size or self.x >= SCREEN_WIDTH - self.size:
            self.dx = -self.dx
        if self.y <= self.size:
            self.dy = -self.dy
            
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, 
                          self.size * 2, self.size * 2)

class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        
    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.destroyed = False
        
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, LIGHT_BLUE, (self.x, self.y, self.width, self.height), 2)
            
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout - IMPROVING")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game objects
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.blocks = []
        self.start_time = time.time()
        self.completion_time = 0
        self.game_over = False
        self.game_won = False
        
        self.create_improving_blocks()
        
    def create_improving_blocks(self):
        # Letter patterns (1 = block, 0 = empty)
        # Each letter is 5 rows, variable width
        
        patterns = {
            'i': [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
                [1, 1, 1]
            ],
            'm': [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1]
            ],
            'p': [
                [1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 1, 1, 1],
                [1, 0, 0, 0],
                [1, 0, 0, 0]
            ],
            'r': [
                [1, 1, 1, 1],
                [1, 0, 0, 1],
                [1, 1, 1, 0],
                [1, 0, 1, 0],
                [1, 0, 0, 1]
            ],
            'o': [
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [1, 0, 0, 1],
                [0, 1, 1, 0]
            ],
            'v': [
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0]
            ],
            'n': [
                [1, 0, 0, 0, 1],
                [1, 1, 0, 0, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 0, 1, 1],
                [1, 0, 0, 0, 1]
            ],
            'g': [
                [0, 1, 1, 1],
                [1, 0, 0, 0],
                [1, 0, 1, 1],
                [1, 0, 0, 1],
                [0, 1, 1, 1]
            ]
        }
        
        # Word "improving"
        word = "improving"
        start_x = 80
        start_y = 80
        
        current_x = start_x
        
        for letter in word:
            if letter in patterns:
                pattern = patterns[letter]
                
                for row in range(len(pattern)):
                    for col in range(len(pattern[row])):
                        if pattern[row][col] == 1:
                            block_x = current_x + col * (BLOCK_WIDTH + BLOCK_PADDING)
                            block_y = start_y + row * (BLOCK_HEIGHT + BLOCK_PADDING)
                            self.blocks.append(Block(block_x, block_y))
                
                # Move to next letter position
                current_x += (len(pattern[0]) + 1) * (BLOCK_WIDTH + BLOCK_PADDING)
    
    def handle_collisions(self):
        ball_rect = self.ball.get_rect()
        
        # Paddle collision
        paddle_rect = self.paddle.get_rect()
        if ball_rect.colliderect(paddle_rect) and self.ball.dy > 0:
            # Calculate bounce angle based on where ball hits paddle
            hit_pos = (self.ball.x - (self.paddle.x + self.paddle.width/2)) / (self.paddle.width/2)
            angle = hit_pos * math.pi/4  # Max 45 degrees
            speed = math.sqrt(self.ball.dx**2 + self.ball.dy**2)
            self.ball.dx = speed * math.sin(angle)
            self.ball.dy = -speed * math.cos(angle)
        
        # Block collisions
        for block in self.blocks:
            if not block.destroyed and ball_rect.colliderect(block.get_rect()):
                block.destroyed = True
                
                # Simple bounce (reverse y direction)
                self.ball.dy = -self.ball.dy
                break
    
    def update(self):
        if not self.game_over and not self.game_won:
            keys = pygame.key.get_pressed()
            self.paddle.update(keys)
            self.ball.update()
            self.handle_collisions()
            
            # Check if ball fell off screen
            if self.ball.y > SCREEN_HEIGHT:
                self.game_over = True
                
            # Check if all blocks destroyed
            if all(block.destroyed for block in self.blocks):
                self.completion_time = time.time() - self.start_time
                self.game_won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.paddle.draw(self.screen)
        if not self.game_over:
            self.ball.draw(self.screen)
            
        for block in self.blocks:
            block.draw(self.screen)
        
        # Draw UI
        current_time = time.time() - self.start_time
        time_text = self.font.render(f"Time: {current_time:.1f}s", True, WHITE)
        self.screen.blit(time_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
            
        if self.game_won:
            win_text = self.font.render("YOU WIN! IMPROVING achieved!", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
            
            time_text = self.font.render(f"Completion time: {self.completion_time:.1f} seconds", True, WHITE)
            time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            self.screen.blit(time_text, time_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(restart_text, restart_rect)
        
        # Instructions
        if not self.game_over and not self.game_won:
            instr_text = self.small_font.render("Use LEFT/RIGHT arrows to move paddle", True, WHITE)
            self.screen.blit(instr_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
    
    def restart(self):
        self.paddle = Paddle(SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.blocks = []
        self.start_time = time.time()
        self.completion_time = 0
        self.game_over = False
        self.game_won = False
        self.create_improving_blocks()
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.game_won):
                        self.restart()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()