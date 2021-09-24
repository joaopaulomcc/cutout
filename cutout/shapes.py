import math

import cairo
import numpy as np

import cutout.colors as colors
import cutout.transformations as transformations

# --------------------------------------------------------------------------------------
# Constants

LINE_STYLES = {"--": [4, 1], "-": [], ".": [0, 2], "-.": [0, 2, 4, 2]}

LINE_CAPS = {
    "square": cairo.LINE_CAP_SQUARE,
    "round": cairo.LINE_CAP_ROUND,
    "butt": cairo.LINE_CAP_BUTT,
}

LINE_JOINS = {
    "bevel": cairo.LINE_JOIN_BEVEL,
    "round": cairo.LINE_JOIN_ROUND,
    "mitter": cairo.LINE_JOIN_MITER,
}

# --------------------------------------------------------------------------------------
# Functions


def paint_paths(
    surface: cairo.Context,
    fill_color=None,
    line_color=None,
    line_width=1.0,
    line_style="-",
    line_cap="butt",
    line_join="mitter",
    opacity=1.0,
):

    if line_style not in LINE_STYLES.keys():
        raise ValueError(
            f"Available line styles are {[key for key in LINE_STYLES.keys()]}"
        )

    if line_cap not in LINE_CAPS.keys():
        raise ValueError(f"Available line caps are {[key for key in LINE_CAPS.keys()]}")

    if line_join not in LINE_JOINS.keys():
        raise ValueError(
            f"Available line joints are {[key for key in LINE_CAPS.keys()]}"
        )

    if fill_color is not None:
        surface.set_source_rgba(*colors.get_color(fill_color), opacity)
        surface.fill_preserve()

    if line_color is not None:
        surface.set_source_rgba(*colors.get_color(line_color), opacity)
        surface.set_line_width(line_width)

        line_style_values = (line_width * i for i in LINE_STYLES[line_style])
        surface.set_dash(line_style_values)

        if line_style in [".", "-."]:
            surface.set_line_cap(LINE_CAPS["round"])
        else:
            surface.set_line_cap(LINE_CAPS[line_cap])

        surface.set_line_join(LINE_JOINS[line_join])

        surface.stroke()


# --------------------------------------------------------------------------------------
# Classes


class Circle(object):
    def __init__(
        self,
        radius,
        position=(0, 0),
        orientation=0.0,
        line_color="black",
        line_width=1,
        line_style="-",
        fill_color=None,
        opacity=1.0,
    ):
        self.radius = radius
        self.position = position
        self.orientation = orientation
        self.line_color = line_color
        self.line_width = line_width
        self.line_style = line_style
        self.fill_color = fill_color
        self.opacity = opacity

    def draw(self, surface: cairo.Context):

        surface.save()
        transformation_matrix = transformations.rotate_around_point(
            math.radians(self.orientation), self.position
        )
        surface.transform(transformation_matrix)

        surface.arc(
            self.position[0],
            self.position[1],
            self.radius,
            0.0,
            2 * math.pi,
        )

        paint_paths(
            surface,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap="butt",
            line_join="mitter",
            opacity=self.opacity,
        )

        surface.restore()


class Rectangle(object):
    def __init__(
        self,
        position,
        width,
        height,
        orientation=0.0,
        line_color="black",
        line_width=1,
        line_style="-",
        line_cap="butt",
        line_join="mitter",
        fill_color=None,
        opacity=1.0,
    ):
        self.position = position
        self.width = width
        self.height = height
        self.orientation = orientation
        self.line_color = line_color
        self.line_width = line_width
        self.line_style = line_style
        self.line_cap = line_cap
        self.line_join = line_join
        self.fill_color = fill_color
        self.opacity = opacity

    def draw(self, surface: cairo.Context):

        surface.save()

        transformation_matrix = transformations.rotate_around_point(
            math.radians(self.orientation), self.position
        )
        surface.transform(transformation_matrix)

        corner_x = self.position[0] - self.width / 2
        corner_y = self.position[1] - self.height / 2

        surface.rectangle(
            corner_x,
            corner_y,
            self.width,
            self.height,
        )

        paint_paths(
            surface,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        surface.restore()


class Lines(object):
    def __init__(
        self,
        points,
        orientation=0.0,
        line_color="black",
        line_style="-",
        line_width=1,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    ):
        self.points = np.array(points)
        self.orientation = orientation
        self.line_color = line_color
        self.line_style = line_style
        self.line_width = line_width
        self.line_cap = line_cap
        self.line_join = line_join
        self.opacity = opacity
        self.max_x = np.max(self.points[:, 0])
        self.min_x = np.min(self.points[:, 0])
        self.max_y = np.max(self.points[:, 1])
        self.min_y = np.min(self.points[:, 1])
        self.position = [(self.max_x - self.min_x) / 2, (self.max_y - self.min_y) / 2]

    def draw(self, surface: cairo.Context):
        surface.save()

        transformation_matrix = transformations.rotate_around_point(
            math.radians(self.orientation), self.position
        )
        surface.transform(transformation_matrix)

        x0 = self.points[0, 0]
        y0 = self.points[0, 1]

        surface.move_to(x0, y0)

        for i in range(1, len(self.points)):

            surface.line_to(*self.points[i])

        paint_paths(
            surface,
            fill_color=None,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        surface.restore()


class Polygon(object):
    def __init__(
        self,
        points,
        orientation=0.0,
        fill_color=None,
        line_color="black",
        line_style="-",
        line_width=1,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    ):
        self.points = np.array(points)
        self.orientation = orientation
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_style = line_style
        self.line_width = line_width
        self.line_cap = line_cap
        self.line_join = line_join
        self.opacity = opacity
        self.max_x = np.max(self.points[:, 0])
        self.min_x = np.min(self.points[:, 0])
        self.max_y = np.max(self.points[:, 1])
        self.min_y = np.min(self.points[:, 1])
        self.position = [(self.max_x - self.min_x) / 2, (self.max_y - self.min_y) / 2]

    def draw(self, surface: cairo.Context):
        surface.save()

        transformation_matrix = transformations.rotate_around_point(
            math.radians(self.orientation), self.position
        )
        surface.transform(transformation_matrix)

        x0 = self.points[0, 0]
        y0 = self.points[0, 1]

        surface.move_to(x0, y0)

        for i in range(1, len(self.points)):

            surface.line_to(*self.points[i])

        surface.close_path()

        paint_paths(
            surface,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        surface.restore()


class RegularPolygon(object):
    def __init__(
        self,
        n_faces,
        radius,
        position,
        orientation=0.0,
        fill_color=None,
        line_color="black",
        line_style="-",
        line_width=1,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    ):
        self.n_faces = n_faces
        self.radius = radius
        self.position = position
        self.orientation = orientation
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_style = line_style
        self.line_width = line_width
        self.line_cap = line_cap
        self.line_join = line_join
        self.opacity = opacity

        angles = np.arange(0, 2 * np.pi, 2 * np.pi / n_faces)
        x = self.radius * np.cos(angles) + self.position[0]
        y = self.radius * np.sin(angles) + self.position[1]

        self.points = np.transpose(np.array([x, y]))

    def draw(self, surface: cairo.Context):

        polygon = Polygon(
            points=self.points,
            orientation=self.orientation,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_style=self.line_style,
            line_width=self.line_width,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        polygon.position = self.position
        polygon.draw(surface=surface)


class Star(object):
    def __init__(
        self,
        n_points,
        external_radius,
        internal_radius,
        position,
        orientation=0.0,
        fill_color=None,
        line_color="black",
        line_style="-",
        line_width=1,
        line_cap="butt",
        line_join="bevel",
        opacity=1.0,
    ):
        self.n_faces = n_points
        self.external_radius = external_radius
        self.internal_radius = internal_radius
        self.position = position
        self.orientation = orientation
        self.fill_color = fill_color
        self.line_color = line_color
        self.line_style = line_style
        self.line_width = line_width
        self.line_cap = line_cap
        self.line_join = line_join
        self.opacity = opacity

        delta_angle = 2 * np.pi / n_points

        external_angles = np.arange(0, 2 * np.pi, delta_angle)
        x_ext = self.external_radius * np.cos(external_angles) + self.position[0]
        y_ext = self.external_radius * np.sin(external_angles) + self.position[1]

        internal_angles = np.arange(delta_angle / 2, 2 * np.pi, delta_angle)
        x_int = self.internal_radius * np.cos(internal_angles) + self.position[0]
        y_int = self.internal_radius * np.sin(internal_angles) + self.position[1]

        points = []

        for i in range(len(external_angles)):

            points.append([x_ext[i], y_ext[i]])
            points.append([x_int[i], y_int[i]])

        self.points = np.array(points)

    def draw(self, surface: cairo.Context):

        polygon = Polygon(
            points=self.points,
            orientation=self.orientation,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_style=self.line_style,
            line_width=self.line_width,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        polygon.position = self.position
        polygon.draw(surface=surface)


class Arrow(object):
    def __init__(
        self,
        origin,
        vector,
        head_style="triangle",
        head_length=0.1,
        head_width=0.1,
        min_head_length=None,
        line_color="black",
        line_style="-",
        line_width=1,
        opacity=1.0,
    ):
        self.origin = origin
        self.vector = np.array(vector)
        self.length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        self.head_style = head_style
        self.head_length = head_length
        self.head_width = head_width
        self.min_head_length = min_head_length
        self.line_color = line_color
        self.line_style = line_style
        self.line_width = line_width
        self.opacity = opacity

        normal_to_arrow = np.array([-self.vector[1], self.vector[0]]) / self.length

        if self.min_head_length:

            if self.length < self.min_head_length:

                head_aspect = self.head_width / self.head_length

                self.head_length = 1
                self.head_width = head_aspect

            elif self.head_length * self.length < self.min_head_length:

                head_aspect = self.head_width / self.head_length

                self.head_length = self.min_head_length / self.length
                self.head_width = head_aspect * self.head_length

        self.arrow_head_points = np.array(
            [
                self.origin + self.vector,
                self.origin
                + (1 - self.head_length) * self.vector
                + normal_to_arrow * (self.head_width / 2) * self.length,
                self.origin + (1 - 0.8 * self.head_length) * self.vector,
                self.origin
                + (1 - self.head_length) * self.vector
                - normal_to_arrow * (self.head_width / 2) * self.length,
            ]
        )

    def draw(self, surface: cairo.Context):

        surface.move_to(*self.origin)
        surface.line_to(*(self.origin + self.vector))

        paint_paths(
            surface,
            fill_color=None,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap="butt",
            line_join="mitter",
            opacity=self.opacity,
        )

        if self.head_style == "triangle":

            points = self.arrow_head_points[[True, True, False, True]]

            arrow_head = Polygon(
                points=points,
                line_width=self.line_width,
                fill_color=self.line_color,
                line_color=self.line_color,
                opacity=self.opacity,
            )

            arrow_head.draw(surface)

        elif self.head_style == "stroke":

            points = [
                self.arrow_head_points[1],
                self.arrow_head_points[0],
                self.arrow_head_points[3],
            ]

            arrow_head = Lines(
                points=points,
                line_width=self.line_width,
                line_color=self.line_color,
                line_style=self.line_style,
            )

            arrow_head.draw(surface)

        elif self.head_style == "arrow":

            points = self.arrow_head_points
            arrow_head = Polygon(
                points=points,
                line_width=self.line_width,
                fill_color=self.line_color,
                line_color=self.line_color,
                opacity=self.opacity,
            )

            arrow_head.draw(surface)

        paint_paths(
            surface,
            fill_color=self.line_color,
            line_color=None,
            line_width=self.line_width,
            line_style="-",
            line_cap="butt",
            line_join="mitter",
            opacity=self.opacity,
        )


class RoundedRectangle(object):
    def __init__(
        self,
        position,
        width,
        height,
        corner_radius=None,
        orientation=0.0,
        line_color="black",
        line_width=1,
        line_style="-",
        line_cap="butt",
        line_join="mitter",
        fill_color=None,
        opacity=1.0,
    ):
        self.position = np.array(position)
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.orientation = orientation
        self.line_color = line_color
        self.line_width = line_width
        self.line_style = line_style
        self.line_cap = line_cap
        self.line_join = line_join
        self.fill_color = fill_color
        self.opacity = opacity

    def draw(self, surface: cairo.Context):

        surface.save()

        transformation_matrix = transformations.rotate_around_point(
            math.radians(self.orientation), self.position
        )
        surface.transform(transformation_matrix)

        p0 = self.position
        p1 = p0 + (self.width / 2, self.height / 2 - self.corner_radius)
        # p2 = p0 + (self.width / 2 - self.corner_radius, self.height / 2)
        p3 = p0 + (-self.width / 2 + self.corner_radius, self.height / 2)
        # p4 = p0 + (-self.width / 2, self.height / 2 - self.corner_radius)
        p5 = p0 + (-self.width / 2, -self.height / 2 + self.corner_radius)
        # p6 = p0 + (-self.width / 2 + self.corner_radius, -self.height / 2)
        p7 = p0 + (self.width / 2 - self.corner_radius, -self.height / 2)
        # p8 = p0 + (self.width / 2, -self.height / 2 + self.corner_radius)

        c1 = p0 + (
            self.width / 2 - self.corner_radius,
            self.height / 2 - self.corner_radius,
        )
        c2 = p0 + (
            -self.width / 2 + self.corner_radius,
            self.height / 2 - self.corner_radius,
        )
        c3 = p0 + (
            -self.width / 2 + self.corner_radius,
            -self.height / 2 + self.corner_radius,
        )
        c4 = p0 + (
            self.width / 2 - self.corner_radius,
            -self.height / 2 + self.corner_radius,
        )

        surface.move_to(*p1)
        surface.arc(c1[0], c1[1], self.corner_radius, 0, np.pi / 2)
        surface.line_to(*p3)
        surface.arc(c2[0], c2[1], self.corner_radius, np.pi / 2, np.pi)
        surface.line_to(*p5)
        surface.arc(c3[0], c3[1], self.corner_radius, np.pi, 3 * np.pi / 2)
        surface.line_to(*p7)
        surface.arc(c4[0], c4[1], self.corner_radius, 3 * np.pi / 2, 2 * np.pi)
        surface.close_path()

        paint_paths(
            surface,
            fill_color=self.fill_color,
            line_color=self.line_color,
            line_width=self.line_width,
            line_style=self.line_style,
            line_cap=self.line_cap,
            line_join=self.line_join,
            opacity=self.opacity,
        )

        surface.restore()
