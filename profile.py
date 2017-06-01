import json
import math


class Vertex:
    """
    Represents a vertex
    """
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x
        self.y = y

    @classmethod
    def create_from_schema(cls, key, value):
        """Creates a Vertex based on a key-value pair from the schema"""
        position = value['Position']
        return cls(key, position['X'], position['Y'])


class Edge:
    """
    Base class for all Edge classes
    """
    def __init__(self, id_, vertices, *args):
        self.id = id_
        self.vertices = vertices

    @classmethod
    def create_from_schema(cls, key, value, all_vertices):
        """Creates an Edge based on a key-value pair from the schema"""
        class_type = edgefactory(value['Type'])
        vertices_for_edge = [all_vertices[str(k)] for k in value['Vertices']]
        return class_type._create_from_schema(key, value, vertices_for_edge)

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        raise NotImplementedError("Subclass should implement this method.")

    def cost(self):
        """Returns the cost of this Edge"""
        return self._cost()

    def _cost(self):
        return 0


class LineSegmentEdge(Edge):
    """Represents a line segment edge"""

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        return cls(key, vertices)

    def _cost(self):
        horizontal_distance = self.vertices[0].x - self.vertices[1].x
        vertical_distance = self.vertices[0].y - self.vertices[1].y
        return (math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2) / 0.5) * 0.07


class CircularArcEdge(Edge):
    """Represents a circular arc edge"""
    def __init__(self, id_, vertices, center_x, center_y, clockwise_from):
        super().__init__(id_, vertices)
        self.center_x = center_x
        self.center_y = center_y
        self.clockwise_from = clockwise_from

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        return cls(key, vertices, value['Center']['X'], value['Center']['Y'], value['ClockwiseFrom'])


edge_mapping = {
    'LineSegment': LineSegmentEdge,
    'CircularArcEdge': CircularArcEdge,
}

def edgefactory(edge_type):
    """Returns the Edge class given the edge_type"""
    return edge_mapping[edge_type]


class Profile:
    """Represents an extrusion profile"""
    def __init__(self, edges):
        self.edges = {}
        self.vertices = {}
        for edge in edges:
            self.edges[edge.id] = edge

    @classmethod
    def create_from_json(cls, filepath):
        """Creates a Profile instance from a JSON file"""
        with open(filepath) as f:
            profile_from_json = json.loads(f.read())
        vertices_json = profile_from_json['Vertices']
        edges_from_json = profile_from_json['Edges']

        all_vertices = {k: Vertex.create_from_schema(k, v) for k, v in vertices_json.items()}
        edges = [Edge.create_from_schema(k, v, all_vertices) for k, v in edges_from_json.items()]
        return cls(edges)
