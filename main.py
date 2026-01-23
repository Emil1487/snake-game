import random
import pygame as pg

FPS = 30
W, H = 1000, 800

BLACK = (0, 0, 0)
RED = (227, 32, 32)
DARK_RED = (209, 32, 32)
WHITE = (255, 255, 255)
DARK_GREEN = (51, 181, 70)
GREEN = (56, 199, 78)
BLUE = (25, 12, 194)
DARK_BLUE = (14, 7, 110)

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

sc = pg.display.set_mode((W, H))
pg.display.set_caption("Snake")
clock = pg.time.Clock()

bg = pg.image.load("images/background.png")


def apple_rand(occupied, exclude=None):
    attempts = 0
    while attempts < 100:
        attempts += 1
        x, y = random.randint(0, 24) * 40, random.randint(0, 19) * 40
        pos = (x, y)
        if pos not in occupied and pos != exclude:
            return pos
    return -40, -40


def check_click_on_button(button):
    if button.button_rect.collidepoint(pg.mouse.get_pos()):
        return True
    return None


def direct(self, d):
    if d == "right" and self.direction != "left":
        self.surf = pg.transform.rotate(pg.image.load(f'images/{head.color}_head.png'), -90)
        self.surf = pg.transform.scale_by(self.surf, 2)
        return 'right'
    elif d == "left" and self.direction != "right":
        self.surf = pg.transform.rotate(pg.image.load(self.image), 90)
        self.surf = pg.transform.scale_by(self.surf, 2)
        return "left"
    elif d == "down" and self.direction != "up":
        self.surf = pg.transform.rotate(pg.image.load(self.image), 180)
        self.surf = pg.transform.scale_by(self.surf, 2)
        return 'down'
    elif d == "up" and self.direction != "down":
        self.surf = pg.image.load(self.image)
        self.surf = pg.transform.scale_by(self.surf, 2)
        return "up"
    return self.direction


class Head:
    def __init__(self, score="0", color="green", cords=(520, 400)):
        self.color = color
        self.image = f'images/{self.color}_head.png'
        self.surf = pg.image.load(f'images/{self.color}_head.png')
        self.surf = pg.transform.scale_by(self.surf, 2)
        self.cords = cords
        self.old_cords = cords
        self.stop = False
        self.direction = "right"
        self.surf = pg.transform.rotate(self.surf, -90)
        self.stop = 0
        self.old_dir = self.direction
        self.score = score

    def move(self):
        self.old_cords = self.cords
        if self.direction == "right":
            self.cords = (self.cords[0] + 40, self.cords[1])
        elif self.direction == "left":
            self.cords = (self.cords[0] - 40, self.cords[1])
        elif self.direction == "up":
            self.cords = (self.cords[0], self.cords[1] - 40)
        elif self.direction == "down":
            self.cords = (self.cords[0], self.cords[1] + 40)

        if self.cords[0] >= W or self.cords[0] < 0 or self.cords[1] >= H or self.cords[1] < 0:
            self.los()

    def direct(self, d):
        self.direction = direct(self, d)

    def los(self):
        self.stop = 1

    def draw(self, screen):
        screen.blit(self.surf, self.cords)


class Body:
    def __init__(self, cords):
        self.image = f'images/{head.color}_body.png'
        self.direction = ""
        self.cords = cords
        self.surf = pg.image.load(f'images/{head.color}_body.png')
        self.surf = pg.transform.scale_by(self.surf, 2)
        self.direction_to = self.direction
        self.direction_curr = "right"

    def move(self, new_cords):
        self.cords = new_cords

    def direct(self, d):
        self.direction = direct(self, d)

    def find_dir(self, index):
        if self.cords[0] < body_parts[index - 1].cords[0]:
            self.surf = pg.transform.rotate(self.surf, -90)
        elif self.cords[0] > body_parts[index - 1].cords[0]:
            self.surf = pg.transform.rotate(self.surf, 90)
        elif self.cords[1] < body_parts[index - 1].cords[1]:
            self.surf = pg.transform.rotate(self.surf, 180)
        elif self.cords[1] > body_parts[index - 1].cords[1]:
            pass

    def draw(self, screen, index):
        if self == body_parts[-1]:
            self.surf = pg.image.load(f'images/{head.color}_end.png')
            self.image = f'images/{head.color}_end.png'
            self.surf = pg.transform.scale_by(self.surf, 2)
            self.find_dir(index)
            screen.blit(self.surf, self.cords)
            return
        if self != body_parts[-1]:
            self.surf = pg.image.load(f'images/{head.color}_body.png')
            self.image = f'images/{head.color}_body.png'
            self.surf = pg.transform.scale_by(self.surf, 2)
            self.find_dir(index)

        if (body_parts[index - 1].cords[0] != body_parts[index + 1].cords[0] and body_parts[index - 1].cords[1] !=
                body_parts[index + 1].cords[1]):
            self.surf = pg.image.load(f'images/{head.color}_corner.png')
            self.image = f'images/{head.color}_corner.png'
            self.surf = pg.transform.scale_by(self.surf, 2)

            if self.cords[0] > body_parts[index - 1].cords[0] and self.cords[1] == body_parts[index - 1].cords[1]:
                if self.cords[1] < body_parts[index + 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, 90)
                elif self.cords[1] > body_parts[index + 1].cords[1]:
                    pass

            elif self.cords[0] < body_parts[index - 1].cords[0] and self.cords[1] == body_parts[index - 1].cords[1]:
                if self.cords[1] < body_parts[index + 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, -180)
                elif self.cords[1] > body_parts[index + 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, -90)

            elif self.cords[0] < body_parts[index + 1].cords[0] and self.cords[1] == body_parts[index + 1].cords[1]:
                if self.cords[1] < body_parts[index - 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, 180)
                elif self.cords[1] > body_parts[index - 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, -90)

            elif self.cords[0] > body_parts[index + 1].cords[0] and self.cords[1] == body_parts[index + 1].cords[1]:
                if self.cords[1] < body_parts[index - 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, 90)
                elif self.cords[1] > body_parts[index - 1].cords[1]:
                    self.surf = pg.transform.rotate(self.surf, 0)

        screen.blit(self.surf, self.cords)


class Apples:
    def __init__(self):
        occupied = [elem.cords for elem in body_parts] + [a.cords for a in apples]
        self.cords = apple_rand(occupied)
        self.surf = pg.image.load('images/apple.png')
        self.surf = pg.transform.scale_by(self.surf, 2)

    def draw(self, screen):
        screen.blit(self.surf, self.cords)


class Text:
    def __init__(self, text, score, text_size, text_color, text_pos):
        self.text = text
        self.text_color = text_color
        self.color = text_color
        self.score = score
        self.bg_surf = pg.Surface((W, H), pg.SRCALPHA)
        pg.draw.rect(self.bg_surf, (*BLACK, 128), (0, 0, W, H))
        self.font = pg.font.SysFont(None, text_size)
        self.text_surf = self.font.render(score, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=text_pos)

    def draw(self, screen):
        self.text_surf = self.font.render(f"{self.text} {self.score}", True, self.text_color)
        screen.blit(self.text_surf, self.text_rect)

    def max(self):
        if int(self.score) < int(head.score):
            self.score = head.score


class Button:
    def __init__(self, text, text_size, text_color, button_color, button_pos, button_color_2):
        self.bg_surf = pg.Surface((W, H), pg.SRCALPHA)
        pg.draw.rect(self.bg_surf, (*BLACK, 128), (0, 0, W, H))
        self.button_color = button_color
        self.button_color_2 = button_color_2
        self.current_color = button_color
        self.text_color = text_color
        self.font = pg.font.SysFont(None, text_size)
        self.text_surf = self.font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect(center=button_pos)
        self.button_surf = pg.Surface((self.text_surf.get_width() + 50, self.text_surf.get_height() + 50))
        self.button_rect = self.button_surf.get_rect(center=button_pos)
        self.button_surf.fill(self.current_color)
        pg.draw.rect(self.button_surf, BLACK, (0, 0, self.button_rect.width, self.button_rect.height), 3)

    def draw(self, screen):
        self.button_surf.fill(self.current_color)
        pg.draw.rect(self.button_surf, BLACK, (0, 0, self.button_rect.width, self.button_rect.height), 3)
        screen.blit(self.button_surf, self.button_rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_hovered(self):
        return self.button_rect.collidepoint(pg.mouse.get_pos())

    def update_color(self):
        if self.is_hovered():
            self.current_color = self.button_color_2
        else:
            self.current_color = self.button_color


sc.blit(bg, (0, 0))
pg.display.update()
flag_play = True


def main():
    cnt = 0
    head.stop = 0
    key_pressed = ''
    while True:
        clock.tick(FPS)
        cnt += 1

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

        if head.stop:
            los()
            return

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            key_pressed = "left"
        elif keys[pg.K_RIGHT]:
            key_pressed = "right"
        elif keys[pg.K_UP]:
            key_pressed = "up"
        elif keys[pg.K_DOWN]:
            key_pressed = "down"

        if cnt >= 5:
            if key_pressed == "left":
                head.direct("left")
            elif key_pressed == "right":
                head.direct("right")
            elif key_pressed == "up":
                head.direct("up")
            elif key_pressed == "down":
                head.direct("down")
            old_positions = [elem.cords for elem in body_parts]
            head.move()
            for i in range(1, len(body_parts)):
                body_parts[i].move(old_positions[i - 1])

            cnt = 0

        for apple in apples:
            if head.cords == apple.cords:
                last_part = body_parts[-1]
                body_parts.append(Body(last_part.cords))
                occupied = [elem.cords for elem in body_parts] + [a.cords for a in apples]
                apple.cords = apple_rand(occupied)
                head.score = str(int(head.score) + 1)

        text_score.score = head.score

        for part in body_parts[1:]:
            if head.cords == part.cords:
                head.los()

        sc.blit(bg, (0, 0))
        for ind in range(1, len(body_parts)):
            body_parts[ind].draw(sc, ind)
        head.draw(sc)
        for elem in apples:
            elem.draw(sc)
        for elem in text_lst[1:]:
            elem.draw(sc)
        text_high.max()
        pg.display.update()


def los():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if my_button.is_hovered():
                    return text_score
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                return text_score

        for elem in buttons:
            elem.update_color()

        sc.blit(bg, (0, 0))
        for ind in range(1, len(body_parts)):
            body_parts[ind].draw(sc, ind)
        head.draw(sc)
        head.draw(sc)
        for elem in apples:
            elem.draw(sc)
        sc.blit(my_button.bg_surf, (0, 0))
        my_button.draw(sc)
        for elem in text_lst[1:]:
            elem.draw(sc)
        pg.display.update()
        clock.tick(FPS)


def main_ui():
    color_of_snake = "green"
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.is_hovered():
                    return color_of_snake
                if color_blue_button.is_hovered():
                    color_of_snake = "blue"
                if color_green_button.is_hovered():
                    color_of_snake = "green"
                if color_red_button.is_hovered():
                    color_of_snake = "red"
            elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                return color_of_snake

        for elem in buttons:
            elem.update_color()

        sc.blit(bg, (0, 0))
        for elem in buttons[1:]:
            elem.draw(sc)
        text_choose_color.draw(sc)
        pg.display.update()
        clock.tick(FPS)


score_high = 0
head = Head("0")
text_score = Text("Score:", head.score, 32, WHITE, (20, 20))
text_high = Text("Highest score:", "0", 32, WHITE, (W - 180, 20))
text_choose_color = Text("Choose snake color:", "", 50, WHITE, (W // 2 - 165, H // 2 - 120))

text_lst = [text_choose_color, text_high, text_score]
my_button = Button("You lost, press R to reset", 80, BLACK, RED, (W // 2, H // 2), DARK_RED)
start_button = Button("Press to start", 80, BLACK, GREEN, (W // 2, H // 2 + 100), DARK_GREEN)
color_blue_button = Button(".", 1, BLUE, BLUE, (W // 2 - 100, H // 2 - 50), DARK_BLUE)
color_green_button = Button(".", 1, GREEN, GREEN, (W // 2, H // 2 - 50), DARK_GREEN)
color_red_button = Button(".", 1, RED, RED, (W // 2 + 100, H // 2 - 50), DARK_RED)
buttons = [my_button, start_button, color_blue_button, color_green_button, color_red_button]
start = True
while flag_play:
    if score_high < int(text_score.score):
        score_high = int(head.score)
    head = Head("0")
    body_parts = [head, Body((480, 400)), Body((440, 400)), Body((400, 400))]
    apples = []
    text_high.score = str(score_high)
    for _ in range(10):
        apples.append(Apples())

    if start:
        color_of_snake_main = main_ui()
        start = False
        head = Head("0", color_of_snake_main)
        body_parts = [head, Body((480, 400)), Body((440, 400)), Body((400, 400))]
        apples = [Apples() for _ in range(10)]
        text_high.score = str(score_high)
        main()
    else:
        head = Head("0", color_of_snake_main)
        body_parts = [head, Body((480, 400)), Body((440, 400)), Body((400, 400))]
        apples = [Apples() for _ in range(10)]
        text_high.score = str(score_high)
        main()

exit()
