from unittest import TestCase
from profile import Profile, LineSegmentEdge, Vertex


class TestProfile(TestCase):
    def test_create_from_json(self):
        profile = Profile.create_from_json('fixtures/Rectangle.json')
        self.assertEqual(len(profile.edges), 4)


class LineSegmentTest(TestCase):
    def test_horizontal_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 5, 0)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost(), 0.7)

    def test_vertical_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 0, 5)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost(), 0.7)

    def test_diagonal_line_segment_cost(self):
        vertices = [Vertex(1, 0, 0), Vertex(2, 1, 1)]
        edge = LineSegmentEdge(1, vertices)
        self.assertAlmostEqual(edge.cost(), 0.19798989873223333)
