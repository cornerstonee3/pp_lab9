import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    radius = 15
    mode = 'blue'
    prev_mode = 'blue'
    points = []
    erase_points = []
    shapes = []
    drawing_shape = False
    shape_start = None
    draw_mode = 'freehand'

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_r:
                    mode = 'red'
                    prev_mode = mode
                elif event.key == pygame.K_g:
                    mode = 'green'
                    prev_mode = mode
                elif event.key == pygame.K_b:
                    mode = 'blue'
                    prev_mode = mode
                elif event.key == pygame.K_e:
                    if mode != 'eraser':
                        prev_mode = mode
                        mode = 'eraser'
                    else:
                        mode = prev_mode
                elif event.key == pygame.K_c:
                    draw_mode = 'circle'
                elif event.key == pygame.K_t:
                    draw_mode = 'rect'
                elif event.key == pygame.K_f:
                    draw_mode = 'freehand'
                elif event.key == pygame.K_s:
                    draw_mode = 'square'
                elif event.key == pygame.K_y:
                    draw_mode = 'right_triangle'
                elif event.key == pygame.K_u:
                    draw_mode = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    draw_mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if draw_mode in ('circle', 'rect', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus'):
                        drawing_shape = True
                        shape_start = event.pos
                    else:
                        radius = min(200, radius + 1)
                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing_shape:
                    shape_end = event.pos
                    rect = pygame.Rect(min(shape_start[0], shape_end[0]),
                                     min(shape_start[1], shape_end[1]),
                                     abs(shape_end[0] - shape_start[0]),
                                     abs(shape_end[1] - shape_start[1]))
                    shapes.append({'type': draw_mode, 'rect': rect, 'color': color_from_mode(mode), 'width': radius})
                    shapes = shapes[-512:]
                    drawing_shape = False
                    shape_start = None

            if event.type == pygame.MOUSEMOTION:
                position = event.pos
                buttons = pygame.mouse.get_pressed()
                right_down = buttons[2]

                if mode == 'eraser' or right_down:
                    erase_points = erase_points + [position]
                    erase_points = erase_points[-1024:]
                else:
                    if not drawing_shape:
                        points = points + [position]
                        points = points[-256:]

        screen.fill((0, 0, 0))

        for s in shapes:
            draw_shape(screen, s)

        i = 0
        while i < len(points) - 1:
            drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
            i += 1

        for pos in erase_points:
            pygame.draw.circle(screen, (0, 0, 0), pos, radius)

        if drawing_shape and shape_start:
            cur = pygame.mouse.get_pos()
            preview_rect = pygame.Rect(min(shape_start[0], cur[0]),
                                     min(shape_start[1], cur[1]),
                                     abs(cur[0] - shape_start[0]),
                                     abs(cur[1] - shape_start[1]))
            preview = {'type': draw_mode, 'rect': preview_rect, 'color': color_from_mode(mode), 'width': radius}
            draw_shape(screen, preview, preview=True)

        pygame.display.flip()
        clock.tick(60)

def color_from_mode(mode):
    if mode == 'blue':
        return (0, 0, 255)
    elif mode == 'red':
        return (255, 0, 0)
    elif mode == 'green':
        return (0, 255, 0)
    else:
        return (200, 200, 200)

def draw_shape(screen, shape, preview=False):
    rect = shape['rect']
    color = shape['color']

    if shape['type'] == 'rect':
        if preview:
            pygame.draw.rect(screen, color, rect, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.rect(screen, color, rect)

    elif shape['type'] == 'circle':
        size = max(rect.w, rect.h)
        square = pygame.Rect(rect.left, rect.top, size, size)
        center = square.center
        radius = size // 2
        if preview:
            pygame.draw.circle(screen, color, center, radius, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.circle(screen, color, center, radius)

    elif shape['type'] == 'square':
        size = max(rect.w, rect.h)
        square_rect = pygame.Rect(rect.left, rect.top, size, size)
        if preview:
            pygame.draw.rect(screen, color, square_rect, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.rect(screen, color, square_rect)

    elif shape['type'] == 'right_triangle':
        x1 = rect.left
        y1 = rect.top
        x2 = rect.right
        y2 = rect.top
        x3 = rect.left
        y3 = rect.bottom
        points = [(x1, y1), (x2, y2), (x3, y3)]
        if preview:
            pygame.draw.polygon(screen, color, points, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.polygon(screen, color, points)

    elif shape['type'] == 'equilateral_triangle':
        center_x = rect.centerx
        center_y = rect.top
        size = max(rect.w, rect.h)
        height = int(size * 0.866)
        x1 = center_x
        y1 = rect.top
        x2 = rect.left
        y2 = rect.top + height
        x3 = rect.right
        y3 = rect.top + height
        points = [(x1, y1), (x2, y2), (x3, y3)]
        if preview:
            pygame.draw.polygon(screen, color, points, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.polygon(screen, color, points)

    elif shape['type'] == 'rhombus':
        center_x = rect.centerx
        center_y = rect.centery
        x1 = center_x
        y1 = rect.top
        x2 = rect.right
        y2 = center_y
        x3 = center_x
        y3 = rect.bottom
        x4 = rect.left
        y4 = center_y
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        if preview:
            pygame.draw.polygon(screen, color, points, max(1, int(shape['width'] / 2)))
        else:
            pygame.draw.polygon(screen, color, points)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    else:
        color = (c1, c1, c2)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()
