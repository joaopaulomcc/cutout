import context

import math

import cairo
import numpy as np

import cutout


def create_image(width, height, background_color):

    image = cairo.ImageSurface(
        cairo.FORMAT_ARGB32,
        width,
        height,
    )
    surface = cairo.Context(image)
    surface.set_source_rgb(*cutout.colors.get_color(background_color))
    surface.paint()

    transformation_matrix = cairo.Matrix(1, 0, 0, -1, 0, height)
    surface.set_matrix(transformation_matrix)

    return image, surface


def test_circle():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    circle = cutout.shapes.Circle(
        radius=100,
        position=[500, 500],
        orientation=55,
        line_color="firebrick",
        line_width=5,
        line_style="-",
        fill_color="gold",
        opacity=1.0,
    )

    circle.draw(surface)

    image.write_to_png("tests/images/circle.png")


def test_rectangle():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    rectangle = cutout.shapes.Rectangle(
        position=[500, 500],
        width=700,
        height=250,
        orientation=45,
        line_color="black",
        line_width=5,
        line_style=".",
        line_cap="butt",
        line_join="round",
        fill_color="forestgreen",
        opacity=1.0,
    )

    rectangle.draw(surface)

    image.write_to_png("tests/images/rectangle.png")


def test_lines():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    x = np.linspace(0, 4 * np.pi, 1000)
    y = x * np.sin(x)

    x = (width / (4 * np.pi)) * x
    y = (height / 2) + (height * 0.04) * y

    points = np.transpose([x, y])

    lines = cutout.shapes.Lines(
        points,
        orientation=0,
        line_color="firebrick",
        line_style="-",
        line_width=3,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    )

    lines.draw(surface)

    image.write_to_png("tests/images/lines.png")


def test_polygon():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    x = np.linspace(0, 4 * np.pi, 1000)
    y = x * np.sin(x)

    x = (width / (4 * np.pi)) * x
    y = (height / 2) + (height * 0.04) * y

    points = np.array([[100, 100], [50, 500], [600, 850], [750, 50]])

    polygon = cutout.shapes.Polygon(
        points,
        orientation=0,
        fill_color="gold",
        line_color="firebrick",
        line_style="--",
        line_width=7,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    )

    polygon.draw(surface)

    image.write_to_png("tests/images/polygon.png")


def test_regular_polygon():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    regular_polygon = cutout.shapes.RegularPolygon(
        n_faces=5,
        radius=250,
        position=[500, 500],
        orientation=90.0,
        fill_color="gold",
        line_color="black",
        line_style=".",
        line_width=10,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    )

    regular_polygon.draw(surface)

    image.write_to_png("tests/images/regular_polygon.png")


def test_star():

    width = 1000
    height = 1000
    background_color = "white"

    image, surface = create_image(width, height, background_color)

    star = cutout.shapes.Star(
        n_points=5,
        external_radius=250,
        internal_radius=100,
        position=[500, 500],
        orientation=0.0,
        fill_color="gold",
        line_color="red",
        line_style="-",
        line_width=10,
        line_cap="butt",
        line_join="round",
        opacity=1.0,
    )

    star.draw(surface)

    image.write_to_png("tests/images/star.png")


def test_arrow():

    width = 1000
    height = 1000
    background_color = "black"

    image, surface = create_image(width, height, background_color)

    n = 36
    for i in range(n):

        angle = i * 2 * math.pi / n
        x = 500 * math.cos(angle) * (n - i) / n
        y = 500 * math.sin(angle) * (n - i) / n

        arrow = cutout.shapes.Arrow(
            origin=[500, 500],
            vector=[x, y],
            head_style="arrow",
            head_length=0.1,
            head_width=0.05,
            min_head_length=20,
            line_color="gold",
            line_style=".",
            line_width=3,
            opacity=1.0,
        )

        arrow.draw(surface)

    image.write_to_png("tests/images/arrow.png")


if __name__ == "__main__":

    print()
    print("# Testing")

    test_circle()
    print("- test_circle()")

    test_rectangle()
    print("- test_rectangle()")

    test_lines()
    print("- test_lines()")

    test_polygon()
    print("- test_polygon()")

    test_regular_polygon()
    print("- test_regular_polygon()")

    test_star()
    print("- test_star()")

    test_arrow()
    print("- test_arrow()")

    print()
