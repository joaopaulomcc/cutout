import numpy as np
import cairo


def rotation_matrix(rotation_angle):

    return np.array(
        [
            [np.cos(rotation_angle), -np.sin(rotation_angle), 0],
            [np.sin(rotation_angle), np.cos(rotation_angle), 0],
            [0, 0, 1],
        ]
    )


def translation_matrix(x_t, y_t):

    return np.array(
        [
            [1, 0, x_t],
            [0, 1, y_t],
            [0, 0, 1],
        ]
    )


def scale_matrix(scale_x, scale_y):

    return np.array(
        [
            [scale_x, 0, 0],
            [0, scale_y, 0],
            [0, 0, 1],
        ]
    )


def cairo_matrix(matrix):

    return cairo.Matrix(
        matrix[0][0],
        matrix[1][0],
        matrix[0][1],
        matrix[1][1],
        matrix[0][2],
        matrix[1][2],
    )


def rotate_around_point(rotation_angle, pivot_point):

    rot_matrix = rotation_matrix(rotation_angle)

    trans_matrix_0 = translation_matrix(-pivot_point[0], -pivot_point[1])

    trans_matrix_1 = translation_matrix(pivot_point[0], pivot_point[1])

    return cairo_matrix(trans_matrix_1 @ rot_matrix @ trans_matrix_0)
