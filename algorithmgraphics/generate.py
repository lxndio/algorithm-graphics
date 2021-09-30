import cairo
from math import pi

def draw_centered_text(cr, x, y, width, height, fontSize, text, fixyoffset=None):
    cr.set_font_size(fontSize)

    extents = cr.text_extents(text)
    xc = (x + width/2) - (extents.width/2 + extents.x_bearing)
    yc = (y + height/2) - (extents.height/2 + extents.y_bearing)

    if not fixyoffset:
        cr.move_to(xc, yc)
    else:
        cr.move_to(xc, y + fixyoffset)
    
    cr.show_text(text)
    cr.stroke()

def draw_arrow(cr, x, y, text):
    cr.set_line_width(2)
    cr.set_font_size(20)

    cr.move_to(x, y)
    cr.line_to(x + 5, y + 10)
    cr.line_to(x - 5, y + 10)
    cr.fill()
    cr.move_to(x, y + 10)
    cr.line_to(x, y + 30)
    cr.stroke()

    draw_centered_text(cr, x - 10, y + 30, 20, 30, 20, text)

def draw_bracket(cr, x1, x2, y, text):
    cr.set_line_width(2)
    cr.set_font_size(20)

    cr.arc(x1 + 10, y, 10, 180*(pi/180), 270*(pi/180))
    cr.line_to((x1 + x2)/2 - 10, y - 10)
    cr.stroke()
    cr.arc((x1 + x2)/2 - 10, y - 20, 10, 0, 90*(pi/180))
    cr.move_to((x1 + x2)/2 + 10, y - 10)
    cr.line_to(x2 - 10, y - 10)
    cr.stroke()
    cr.arc((x1 + x2)/2 + 10, y - 20, 10, 90*(pi/180), 180*(pi/180))
    cr.stroke()
    cr.arc(x2 - 10, y, 10, 270*(pi/180), 0)
    cr.stroke()

    draw_centered_text(cr, (x1 + x2)/2 - 20, y - 45, 40, 20, 20, text)

def draw_char_list(cr, x, y, chars, highlight=[], numbers=True, numbers_offset=0, dots_left=False, dots_right=False, arrows=[], brackets=[], frame=True):
    """
    Draw a string as a list of characters, one beside the other.

    :param cr: the Cairo context
    :param x: x coordinate of the upper left corner
    :param y: y coordinate of the upper left corner
    :param chars: the characters to draw
    :param highlight: a list of character positions to be highlighted
    :param numbers: either `True` or `False` to enable or disable printing positions every five characters or a list of positions to print
    :param numbers_offset: set which position number to start with
    :param dots_left: puts dots at the beginning of the string excerpt
    :param dots_right: puts dots at the end of the string excerpt
    :param arrows: a list of position and text tuples to place arrows at with corresponding descriptions
    :param brackets: a list of tuples to draw brackets: (start pos., end pos. height level, description)
    :param frame: whether to draw a frame around each character or not
    """

    if dots_left:
        cr.set_line_width(2)
        cr.move_to(x - 25, y)
        cr.line_to(x, y)
        cr.line_to(x, y + 50)
        cr.line_to(x - 25, y + 50)
        cr.stroke()
        cr.arc(x - 20, y + 25, 3, 0, 2*pi)
        cr.fill()
        cr.arc(x - 30, y + 25, 3, 0, 2*pi)
        cr.fill()
        cr.arc(x - 40, y + 25, 3, 0, 2*pi)
        cr.fill()
    
    if dots_right:
        cr.set_line_width(2)
        cr.move_to(x + 50*len(chars) + 25, y)
        cr.line_to(x + 50*len(chars), y)
        cr.line_to(x + 50*len(chars), y + 50)
        cr.line_to(x + 50*len(chars) + 25, y + 50)
        cr.stroke()
        cr.arc(x + 50*len(chars) + 20, y + 25, 3, 0, 2*pi)
        cr.fill()
        cr.arc(x + 50*len(chars) + 30, y + 25, 3, 0, 2*pi)
        cr.fill()
        cr.arc(x + 50*len(chars) + 40, y + 25, 3, 0, 2*pi)
        cr.fill()
    
    if arrows:
        for i, text in arrows:
            draw_arrow(cr, x + 50*(i - numbers_offset) + 25, y + 60, text)
    
    if brackets:
        for i, j, layer, text in brackets:
            draw_bracket(cr, x + 50*(i - numbers_offset), x + 50*(j - numbers_offset + 1), y - 10 - layer*20, text)

    for i in range(0, len(chars)):
        if i + numbers_offset in highlight:
            cr.set_line_width(6)
        else:
            cr.set_line_width(2)

        if frame:
            cr.rectangle(x + 50*i, y, 50, 50)
            cr.stroke()

        draw_centered_text(cr, x + 50*i, y, 50, 50, 40, chars[i], fixyoffset=40)
        
        if (isinstance(numbers, bool) and numbers and (i + numbers_offset) % 5 == 0) or (isinstance(numbers, list) and i + numbers_offset in numbers):
            draw_centered_text(cr, x + 50*i, y + 50, 50, 35, 20, str(i + numbers_offset))

def color_highlight(cr, x, y, color, positions):
    cr.set_source_rgba(*color)

    for position in positions:
        cr.rectangle(x + position * 50, y, 50, 50)
        cr.fill()

def save_svg(draw_function, filename, width=1000, height=400):
    surface = cairo.SVGSurface(filename, width, height)
    ctx = cairo.Context(surface)

    draw_function(ctx)

def save_png(draw_function, filename, width=1000, height=400, transparent_background=False):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    if not transparent_background:
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

    draw_function(ctx)

    surface.write_to_png(filename)
