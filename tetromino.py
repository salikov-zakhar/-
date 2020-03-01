import random


class Tetromino:
    i_tetromino_angle_0 = ["0000",
                           "1111",
                           "0000",
                           "0000"]

    i_tetromino_angle_90 = ["0100",
                            "0100",
                            "0100",
                            "0100"]

    i_tetromino = (i_tetromino_angle_0, i_tetromino_angle_90,
                   i_tetromino_angle_0, i_tetromino_angle_90)

    o_tetromino_angle_0 = ["1100",
                           "1100",
                           "0000",
                           "0000"]

    o_tetromino = (o_tetromino_angle_0, o_tetromino_angle_0,
                   o_tetromino_angle_0, o_tetromino_angle_0)

    t_tetromino_angle_0 = ["0100",
                           "1110",
                           "0000",
                           "0000"]

    t_tetromino_angle_90 = ["0100",
                            "0110",
                            "0100",
                            "0000"]

    t_tetromino_angle_180 = ["0000",
                             "1110",
                             "0100",
                             "0000"]

    t_tetromino_angle_270 = ["0100",
                             "1100",
                             "0100",
                             "0000"]

    t_tetromino = (t_tetromino_angle_0, t_tetromino_angle_90,
                   t_tetromino_angle_180, t_tetromino_angle_270)

    j_tetromino_angle_0 = ["1000",
                           "1110",
                           "0000",
                           "0000"]

    j_tetromino_angle_90 = ["0110",
                            "0100",
                            "0100",
                            "0000"]

    j_tetromino_angle_180 = ["0000",
                             "1110",
                             "0010",
                             "0000"]

    j_tetromino_angle_270 = ["0100",
                             "0100",
                             "1100",
                             "0000"]

    j_tetromino = (j_tetromino_angle_0, j_tetromino_angle_90,
                   j_tetromino_angle_180, j_tetromino_angle_270)

    l_tetromino_angle_0 = ["0010",
                           "1110",
                           "0000",
                           "0000"]

    l_tetromino_angle_90 = ["0100",
                            "0100",
                            "0110",
                            "0000"]

    l_tetromino_angle_180 = ["0000",
                             "1110",
                             "1000",
                             "0000"]

    l_tetromino_angle_270 = ["1100",
                             "0100",
                             "0100",
                             "0000"]

    l_tetromino = (l_tetromino_angle_0, l_tetromino_angle_90,
                   l_tetromino_angle_180, l_tetromino_angle_270)

    s_tetromino_angle_0 = ["0110",
                           "1100",
                           "0000",
                           "0000"]

    s_tetromino_angle_90 = ["0100",
                            "0110",
                            "0010",
                            "0000"]

    s_tetromino = (s_tetromino_angle_0, s_tetromino_angle_90,
                   s_tetromino_angle_0, s_tetromino_angle_90)

    z_tetromino_angle_0 = ["1100",
                           "0110",
                           "0000",
                           "0000"]

    z_tetromino_angle_90 = ["0010",
                            "0110",
                            "0100",
                            "0000"]

    z_tetromino = (z_tetromino_angle_0, z_tetromino_angle_90,
                   z_tetromino_angle_0, z_tetromino_angle_90)

    tetrominoes = (i_tetromino, o_tetromino, t_tetromino, j_tetromino,
                   l_tetromino, s_tetromino, z_tetromino)

    fast_move_time = 0.03

    def __init__(self, block_dimensions, coord, move_time):
        self.random_index = random.randint(0, 6)
        self.random = Tetromino.tetrominoes[self.random_index]

        self.current_angle = 0
        self.current_frame = self.random[self.current_angle]

        self.block_width = block_dimensions[0]
        self.block_height = block_dimensions[1]

        self.center_coord = list(coord)

        self.blocks_coords = self.build()

        self.normal_move_time = move_time
        self.move_time = self.normal_move_time
        self.elapsed_time = 0.0

    def build(self):
        x, y = [self.center_coord[0] - self.block_width, self.center_coord[1]
                - self.block_height]
        tetromino_coords = []

        for i in range(len(self.current_frame)):
            for char in self.current_frame[i]:
                if char == '1':
                    tetromino_coords.append([x, y])
                x += self.block_width
            x = self.center_coord[0] - self.block_width
            y += self.block_height
        return tetromino_coords

    def set_coords(self, center_coord):
        self.center_coord = list(center_coord)
        self.blocks_coords = self.build()

    def get_coords(self):
        return self.blocks_coords

    def get_color_index(self):
        return self.random_index

    def speed_up(self):
        self.move_time = Tetromino.fast_move_time

    def reset_speed(self):
        self.move_time = self.normal_move_time

    def set_speed(self, move_time):
        self.normal_move_time = move_time
        self.move_time = self.normal_move_time

    def show(self, screen, color_blocks):
        for coord in self.blocks_coords:
            screen.blit(color_blocks[self.random_index], coord)

    def move_up(self):
        for coord in self.blocks_coords:
            coord[1] -= self.block_height
        self.center_coord[1] -= self.block_height

    def move_down(self, time):
        self.elapsed_time += time
        if self.elapsed_time >= self.move_time:
            self.elapsed_time = 0
            for coord in self.blocks_coords:
                coord[1] += self.block_height
            self.center_coord[1] += self.block_height

    def move_left(self):
        self.center_coord[0] -= self.block_width
        for coord in self.blocks_coords:
            coord[0] -= self.block_width

    def move_right(self):
        self.center_coord[0] += self.block_width
        for coord in self.blocks_coords:
            coord[0] += self.block_width

    def rotate_ccw(self):
        if self.current_angle == 0:
            self.current_angle = 3
        else:
            self.current_angle -= 1

        self.current_frame = self.random[self.current_angle]
        self.blocks_coords = self.build()

    def rotate_cw(self):
        self.current_angle = (self.current_angle + 1) % 4
        self.current_frame = self.random[self.current_angle]
        self.blocks_coords = self.build()
