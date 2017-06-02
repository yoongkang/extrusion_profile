from unittest import TestCase
from profile import Profile, LineSegmentEdge, Vertex, CircularArcEdge


class TestProfile(TestCase):
    def test_create_from_json(self):
        profile = Profile.create_from_json('fixtures/Rectangle.json')
        self.assertEqual(len(profile.edges), 4)


class LineSegmentTest(TestCase):
    def test_horizontal_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 5, 0)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost, 0.7)

    def test_vertical_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 0, 5)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost, 0.7)

    def test_diagonal_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 1, 1)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost, 0.19798989873223333)


class CircularArcTest(TestCase):
    def test_points_in_arc1(self):
        c = CircularArcEdge(1, [Vertex(1, 2, 0), Vertex(2, 2, 1)], 2, 0.5, 2)
        self.assertListEqual(
            [c.point_in_arc(*p) for p in c.important_points()],
            [True, True, True, True, True, False]
        )

    def test_points_in_arc2(self):
        c = CircularArcEdge(1, [Vertex(1, 2, 0), Vertex(2, 2, 1)], 2, 0.5, 1)
        self.assertListEqual(
            [c.point_in_arc(*p) for p in c.important_points()],
            [True, True, True, False, True, True]
        )


class AcceptanceTest(TestCase):
    def test_rectangle(self):
        profile = Profile.create_from_json('fixtures/Rectangle.json')
        self.assertAlmostEqual(profile.cost, 14.10)

    def test_cut_circular_arc(self):
        profile = Profile.create_from_json('fixtures/CutCircularArc.json')
        self.assertAlmostEqual(profile.cost, 4.06)

    def test_extrude_circular_arc(self):
        profile = Profile.create_from_json('fixtures/ExtrudeCircularArc.json')
        self.assertAlmostEqual(profile.cost, 4.47)
