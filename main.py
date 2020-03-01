import os
import pygame
import randomizer
import menu
import net
import tetromino


text_color = (255, 255, 255)

min_screen_coord = (0, 0)
max_screen_coord = (640, 720)
screen_res = max_screen_coord

block_width, block_height = 32, 32
columns = 10
rows = 20
FPS = 60
initial_move_time = 1
difficulty_modifier = 0.85
display_fps = False
display_time = True

score_coord = (20, 50)
time_coord = (20, 100)
level_coord = (20, 150)
fps_coord = (20, 200)
menu_coord = (screen_res[0] / 2, screen_res[1] / 4)
next_tetromino_coord = (screen_res[0] / 10, screen_res[1] * 0.65)
next_coord = (next_tetromino_coord[0] - 10, next_tetromino_coord[1] - 3 * block_height)

font_file = 'SadanaSquare.ttf'


def write(font, message, color):
    text = font.render(str(message), True, color)
    text = text.convert_alpha()

    return text


def main():
    pygame.init()
    pygame.display.set_caption("Tetris")
    screen = pygame.display.set_mode(screen_res)
    pygame.key.set_repeat(100, 70)

    normal_blocks_path = os.path.join('sprites', 'blocks.png')
    assist_blocks_path = os.path.join('sprites', 'assist_blocks.png')
    game_background_path = os.path.join('sprites', 'background.png')
    menu_background_path = os.path.join('sprites', 'background.png')
    grid_background_path = os.path.join('sprites', 'grid_background.png')

    background = pygame.image.load(game_background_path).convert()
    background = pygame.transform.scale(background, screen.get_size())

    font = pygame.font.Font(os.path.join('fonts', font_file), 38)

    def load_blocks(path):
        blocks_list = []
        blocks = pygame.image.load(path).convert_alpha()
        blocks = pygame.transform.scale(blocks, (block_width * 7, block_height))
        for i in range(7):
            block_surface = blocks.subsurface(i * block_width, 0, block_width, block_height)
            blocks_list.append(block_surface)
        return blocks_list

    normal_blocks = load_blocks(normal_blocks_path)
    assist_blocks = load_blocks(assist_blocks_path)

    next_surface = write(font, "NEXT", text_color)

    menu_items = ['START', 'QUIT']
    main_menu = menu.Menu('TETRIS', menu_background_path, screen_res, font_file, menu_coord)
    for item in menu_items:
        main_menu.add_item(item)

    while True:
        randomizer.reset()
        display_menu = True
        while display_menu:
            main_menu.show(screen)
            pygame.display.flip()

            event = pygame.event.wait()
            user_input = main_menu.check_input(event)
            if user_input == menu_items[0]:
                display_menu = False
            elif user_input == menu_items[1] or event.type == pygame.QUIT:
                exit()

        grid = net.Net(columns, rows, (block_width, block_height), screen_res, grid_background_path)
        tetromino_move_time = initial_move_time
        current_tetromino = tetromino.Tetromino((block_width, block_height), grid.get_center_coord(),
                                                tetromino_move_time)
        next_tetromino = tetromino.Tetromino((block_width, block_height), next_tetromino_coord, tetromino_move_time)

        game_over = game_paused = drop_tetromino = False
        clock = pygame.time.Clock()
        total_time = 0.0

        difficulty_level = 1
        dt = 1.0 / FPS
        accumulator = 0.0

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    current_tetromino.move_right()
                    if grid.is_out_of_bounds(current_tetromino.get_coords()) or \
                            grid.overlap(current_tetromino.get_coords()):
                        current_tetromino.move_left()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    current_tetromino.move_left()
                    if grid.is_out_of_bounds(current_tetromino.get_coords()) or \
                            grid.overlap(current_tetromino.get_coords()):
                        current_tetromino.move_right()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    current_tetromino.rotate_cw()
                    if grid.is_out_of_bounds(current_tetromino.get_coords()) or \
                            grid.overlap(current_tetromino.get_coords()):
                        current_tetromino.rotate_ccw()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    current_tetromino.rotate_ccw()
                    if grid.is_out_of_bounds(current_tetromino.get_coords()) or \
                            grid.overlap(current_tetromino.get_coords()):
                        current_tetromino.rotate_cw()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    current_tetromino.speed_up()
                elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    current_tetromino.reset_speed()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    drop_tetromino = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    pause = True
                    grid.display_message(screen, font, text_color, 'PAUSE')
                    while pause:
                        event = pygame.event.wait()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                            pause = False
                        elif event.type == pygame.QUIT:
                            exit()
                    game_paused = True

            if game_paused:
                frame_time = dt
                game_paused = False
                clock.tick(FPS)
            else:
                frame_time = clock.tick(FPS) / 1000.0  # convert to seconds

            accumulator += frame_time
            while accumulator >= dt and not game_over:
                while True:
                    current_tetromino.move_down(dt)
                    overlap = grid.overlap(current_tetromino.get_coords())
                    if not drop_tetromino or overlap:
                        drop_tetromino = False
                        break

                if overlap:
                    current_tetromino.move_up()
                    grid.update(current_tetromino.get_coords(), current_tetromino.get_color_index())
                    if grid.get_score() // 10 + 1 != difficulty_level:
                        difficulty_level += 1
                        tetromino_move_time *= difficulty_modifier

                    current_tetromino = next_tetromino
                    current_tetromino.set_coords(grid.get_center_coord())
                    current_tetromino.set_speed(tetromino_move_time)
                    next_tetromino = tetromino.Tetromino((block_width, block_height), next_tetromino_coord,
                                                         tetromino_move_time)
                game_over = grid.is_game_over()
                accumulator -= dt

            if display_time:
                total_time += frame_time
                time_string = "TIME " + '{0:02d}'.format(int(total_time // 60))\
                              + ":" + '{0:02d}'.format(int(total_time % 60))
                time_surface = write(font, time_string, text_color)
            if display_fps:
                fps_string = "FPS: " + str(int(clock.get_fps()))
                fps_surface = write(font, fps_string, text_color)

            score_string = "SCORE: " + str(grid.get_score())
            score_surface = write(font, score_string, text_color)
            level_string = "LEVEL: " + str(difficulty_level)
            level_surface = write(font, level_string, text_color)

            screen.blit(background, min_screen_coord)
            screen.blit(score_surface, score_coord)
            screen.blit(level_surface, level_coord)
            if display_time:
                screen.blit(time_surface, time_coord)
            if display_fps:
                screen.blit(fps_surface, fps_coord)
            screen.blit(next_surface, next_coord)
            grid.show(screen, normal_blocks)
            if not game_over:
                assist_coords = grid.get_assist_coords(current_tetromino.get_coords())
                for coord in assist_coords:
                    screen.blit(assist_blocks[current_tetromino.get_color_index()], coord)
                current_tetromino.show(screen, normal_blocks)
            next_tetromino.show(screen, normal_blocks)
            pygame.display.flip()

        grid.display_message(screen, font, text_color, 'GAME OVER')
        clock.tick(0.7)


if __name__ == '__main__':
    main()
