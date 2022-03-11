import pygame
import pygame.freetype
import random
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

pygame.init()

clock = pygame.time.Clock()
clock.tick(60)

pygame.display.set_caption("Shooting Range")
icon = pygame.image.load('target.png')
pygame.display.set_icon(icon)
BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def create_surface_with_text(text, font_size, text_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()


class UIElement(pygame.sprite.Sprite):

    def __init__(self, center_position, text, font_size, text_rgb, action=None):
        super().__init__()

        self.mouse_over = False


        default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb)


        highlighted_image = create_surface_with_text(text=text, font_size=font_size * 1.2, text_rgb=text_rgb)


        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]
        self.action = action

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

gun = pygame.image.load('gun3.png')
gun = pygame.transform.scale(gun,(70,70))

class Reticle(pygame.sprite.Sprite):
    def __init__(self):
       super().__init__()
       self.image = gun
       self.rect = self.image.get_rect()
       self.gunshot = pygame.mixer.Sound("gun-gunshot-01.wav")
    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(reticle,target_group,True)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('target_colored_outline.png')
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]

reticle = Reticle()
reticle_group = pygame.sprite.Group()

target_group = pygame.sprite.Group()

def create():
    for target in range(20):
        new_target = Target(random.randrange(0, 1800), random.randrange(0, 800))
        target_group.add(new_target)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1

def main():
    pygame.init()

    screen = pygame.display.set_mode((1800, 950))

    # create a ui element
    quit_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        text_rgb=WHITE,
        text="Hello World",
        action=GameState.QUIT
    )

    # main loop
    while True:
        pygame.init()

        screen = pygame.display.set_mode((1800, 950))
        game_state = GameState.TITLE

        while True:
            if game_state == GameState.TITLE:
                game_state = title_screen(screen)

            if game_state == GameState.NEWGAME:
                game_state = play_level(screen)

            if game_state == GameState.QUIT:
                pygame.quit()
                return

def title_screen(screen):
    start_btn = UIElement(
        center_position=(300, 700),
        font_size=30,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(300, 800),
        font_size=30,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )
    title_text = UIElement(
        center_position=(600, 100),
        font_size=50,
        text_rgb=WHITE,
        text="Welcome to the Shooting Range!"
    )

    buttons = [start_btn, quit_btn, title_text]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        background = pygame.image.load("shootingRange.jpg")
        background = pygame.transform.scale(background, (1800,950))
        screen.blit(background, (0,0))

        pygame.mouse.set_visible(True)
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

def play_level(screen):
    return_btn = UIElement(
        center_position=(140, 900),
        font_size=20,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )
    create()
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                reticle.shoot()
        concretebg = pygame.image.load("BG_concrete.png")
        concretebg = pygame.transform.scale(concretebg, (1800, 950))
        screen.blit(concretebg, (0, 0))

        pygame.mouse.set_visible(False)
        reticle_group.add(reticle)
        target_group.draw(screen)
        reticle_group.draw(screen)
        reticle_group.update()

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(screen)

        pygame.display.flip()
        pygame.display.update()

# call main when the script is run
if __name__ == "__main__":
    main()
