from pygame import Surface, font

from game.constants import Colors

font.init()

fonts = {}
for i, size in enumerate([28, 32, 60]):
    fonts[i] = font.Font("assets/pixeloid-font/PixeloidMono-1G8ae.ttf", size)


def render_text(
    screen: Surface,
    text: str,
    size: int = 0,
    grid_x: int = 0,
    grid_y: int = 0,
    text_align: str = "center",
) -> None:
    text = fonts[size].render(text, True, Colors.UI)

    center = screen.get_width() / 32 * grid_x, screen.get_height() / 20 * grid_y

    if text_align == "left":
        text_rect = text.get_rect(midleft=center)
    elif text_align == "right":
        text_rect = text.get_rect(midright=center)
    else:
        text_rect = text.get_rect(center=center)

    screen.blit(text, text_rect)
