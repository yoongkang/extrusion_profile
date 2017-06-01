

class Vertex(object):
    """
    Represents a vertex
    """
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x
        self.y = y


class Edge(object):
    """
    Base class for all Edge classes
    """
    def __init__(self, id_, vertice_ids, *args):
        self.id = id_
        self.vertice_ids = vertice_ids

    def cost(self):
        """Returns the cost of this Edge"""
        raise NotImplementedError("Subclass should implement this method.")


class LineSegmentEdge(Edge):
    """Represents a line segment edge"""
    pass


class CircularArcEdge(Edge):
    """Represents a circular arc edge"""
    def __init__(self, id_, vertice_ids, center_x, center_y, clockwise_from):
        super(CircularArcEdge, self).__init__(id_, vertice_ids)
        self.center_x = center_x
        self.center_y = center_y
        self.clockwise_from = clockwise_from


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
        pass
