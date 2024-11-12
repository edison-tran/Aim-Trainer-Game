import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 1000,800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30 
LIVES = 10
TOP_BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("timesnewroman", 24)

class Target:
    MAX_SIZE = 30
    GROTWH_RATE = 0.2
    COLOUR = "red"
    COLOUR_2 = "white"
    # self will refer to the target, x & y will refer to the position that will place this target on the board
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROTWH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROTWH_RATE
        else:
            self.size -= self.GROTWH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.COLOUR_2, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOUR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.COLOUR_2, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size
    
def draw(win, targets):
    win.fill("grey")

    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:2d}:{seconds:02d}:{milli:02d}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "white", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_lable = LABEL_FONT.render(f"Speed: {speed} targets/s", 1 , "black")
    hits_lable = LABEL_FONT.render(f"Hits: {targets_pressed} targets/s", 1, "black")
    lives_lable = LABEL_FONT.render(f"Lives: {LIVES - misses} targets/s", 1, "black")

    win.blit(time_label, (5,5))
    win.blit(speed_lable, (200,5))
    win.blit(hits_lable, (500,5))
    win.blit(lives_lable, (750,5))

def endgame(win, elapsed_time, targets_pressed, clicks):
    win.fill("grey")
    time_lable = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_lable = LABEL_FONT.render(f"Speed: {speed} targets/s", 1 , "black")
    hits_lable = LABEL_FONT.render(f"Hits: {targets_pressed} targets/s", 1, "black")
    try:
        accuracy = round(targets_pressed / clicks * 100, 1)
    except ZeroDivisionError:
        accuracy = 0.0

    accuracy_lable = LABEL_FONT.render(f"Accuracy: {accuracy} targets/s", 1, "black")

    win.blit(time_lable, (get_middle(time_lable),250))
    win.blit(speed_lable, (get_middle(speed_lable),350))
    win.blit(hits_lable, (get_middle(hits_lable),450))
    win.blit(accuracy_lable, (get_middle(accuracy_lable),550))
    
    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return WIDTH/2 - surface.get_width()/2
def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(144)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        for target in targets:
                target.update()  

                if target.size <= 0:
                    targets.remove(target)
                    misses += 1 

                if click and target.collide(*mouse_position):
                    targets.remove(target)
                    targets_pressed += 1
        if misses >= LIVES:
                endgame(WIN,elapsed_time, targets_pressed,clicks)
        
        draw(WIN,targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()
if __name__ == "__main__":
    main()