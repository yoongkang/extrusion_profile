import json


class Vertex(object):
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


class Edge(object):
    """
    Base class for all Edge classes
    """
    def __init__(self, id_, vertex_ids, *args):
        self.id = id_
        self.vertex_ids = vertex_ids

    @classmethod
    def create_from_schema(cls, key, value):
        """Creates an Edge based on a key-value pair from the schema"""
        class_type = edgefactory(value['Type'])
        return class_type._create_from_schema(key, value)

    @classmethod
    def _create_from_schema(cls, key, value):
        raise NotImplementedError("Subclass should implement this method.")

    def cost(self):
        """Returns the cost of this Edge"""
        return self._cost()

    def _cost(self):
        raise NotImplementedError("Subclass should implement this method.")


class LineSegmentEdge(Edge):
    """Represents a line segment edge"""

    @classmethod
    def _create_from_schema(cls, key, value):
        return cls(key, value['Vertices'])


class CircularArcEdge(Edge):
    """Represents a circular arc edge"""
    def __init__(self, id_, vertex_ids, center_x, center_y, clockwise_from):
        super(CircularArcEdge, self).__init__(id_, vertex_ids)
        self.center_x = center_x
        self.center_y = center_y
        self.clockwise_from = clockwise_from

    @classmethod
    def _create_from_schema(cls, key, value):
        return cls(key, value['Vertices'], value['Center']['X'], value['Center']['Y'], value['ClockwiseFrom'])


edge_mapping = {
    'LineSegment': LineSegmentEdge,
    'CircularArcEdge': CircularArcEdge,
}

def edgefactory(edge_type):
    """Returns the Edge class given the edge_type"""
    return edge_mapping[edge_type]


class Profile(object):
    """Represents an extrusion profile"""
    def __init__(self, edges, vertices):
        self.edges = {}
        self.vertices = {}
        for edge in edges:
            self.edges[edge.id] = edge
        for vertex in vertices:
            self.vertices[vertex.id] = vertex

    @classmethod
    def create_from_json(cls, filepath):
        """Creates a Profile instance from a JSON file"""
        with open(filepath) as f:
            json_string = f.read()
            profile_from_json = json.loads(json_string)
        vertices_json = profile_from_json['Vertices']
        edges_from_json = profile_from_json['Edges']

        vertices = [Vertex.create_from_schema(k, v) for k, v in vertices_json.items()]
        edges = [Edge.create_from_schema(k, v) for k, v in edges_from_json.items()]

        return cls(edges, vertices)
