import pygame


class Net:

    def __init__(self, columns, rows, block_dimensions, screen_res, background_path):
        self.score = 0
        self.end = False

        self.block_width = block_dimensions[0]
        self.block_height = block_dimensions[1]

        self.area_width = columns * self.block_width
        self.area_height = rows * self.block_height

        self.min_coord = ((screen_res[0] - self.area_width - 80),
                          (screen_res[1] - self.area_height) / 2)
        self.max_coord = (self.min_coord[0] + self.area_width,
                          self.min_coord[1] + self.area_height)

        self.center_coord = (self.min_coord[0] + (columns // 2) * self.block_width,
                             self.min_coord[1] + self.block_height)

        self.columns = columns
        self.rows = rows
        self.net = [[-1 for i in range(self.columns)] for j in range(self.rows)]

        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (self.area_width, self.area_height))
        self.background.set_alpha(200)

    def overlap(self, tetromino_coords):
        indexes_list = self.convert_coords(tetromino_coords)
        for row_index, column_index in indexes_list:
            if row_index >= self.rows or self.net[row_index][column_index] >= 0:
                return True
        return False

    def is_out_of_bounds(self, tetromino_coords):
        for x, y in tetromino_coords:
            if x > self.max_coord[0] - self.block_width or x < self.min_coord[0]:
                return True
        return False

    def is_game_over(self):
        return self.end

    def convert_coords(self, coords):
        indexes_list = []
        for coord in coords:
            column_index = int((coord[0] - self.min_coord[0]) // self.block_width)
            row_index = int((coord[1] - self.min_coord[1]) // self.block_height)
            indexes_list.append((row_index, column_index))
        return indexes_list

    def convert_indexes(self, indexes):
        coords_list = []
        for index in indexes:
            x = int(index[1] * self.block_width + self.min_coord[0])
            y = int(index[0] * self.block_height + self.min_coord[1])
            coords_list.append((x, y))
        return coords_list

    def update(self, coords, color_index):
        indexes_list = self.convert_coords(coords)
        for row_index, column_index in indexes_list:
            if row_index >= 0 and column_index >= 0:
                self.net[row_index][column_index] = color_index

        for row_index, column_index in indexes_list:
            if row_index == 0:
                self.end = True

            full_row = True
            for j in range(self.columns):
                if self.net[row_index][j] == -1:
                    full_row = False
                    break

            if full_row:
                del self.net[row_index]
                self.score += 1
                self.net.insert(0, [-1 for i in range(self.columns)])

    def get_assist_coords(self, tetromino_coords):
        indexes_list = self.convert_coords(tetromino_coords)
        bottom = False
        overlap = False

        for row_index, column_index in indexes_list:
            if row_index >= self.rows - 1:
                return tetromino_coords

        while not bottom and not overlap:
            for i in range(len(indexes_list)):
                row_index, column_index = indexes_list[i]
                indexes_list[i] = (row_index + 1, column_index)
                if self.net[row_index + 1][column_index] >= 0:
                    overlap = True
                elif row_index + 1 >= self.rows - 1:
                    bottom = True

        if overlap:
            i = 0
            for row_index, column_index in indexes_list:
                indexes_list[i] = (row_index - 1, column_index)
                i += 1
        return self.convert_indexes(indexes_list)

    def show(self, screen, color_blocks):
        screen.blit(self.background, self.min_coord)
        for i in range(self.rows):
            for j in range(self.columns):
                if self.net[i][j] >= 0:
                    color_index = self.net[i][j]
                    coord_x = self.min_coord[0] + j * self.block_width
                    coord_y = self.min_coord[1] + i * self.block_height
                    screen.blit(color_blocks[color_index], (coord_x, coord_y))

    def display_message(self, screen, font, color, message):
        text_surface = font.render(str(message), True, color).convert_alpha()
        text_x = self.min_coord[0] + (self.area_width - text_surface.get_width()) / 2
        text_y = (self.min_coord[1] + self.area_height) / 2
        screen.blit(text_surface, (text_x, text_y))
        pygame.display.flip()

    def get_score(self):
        return self.score

    def get_center_coord(self):
        return self.center_coord
