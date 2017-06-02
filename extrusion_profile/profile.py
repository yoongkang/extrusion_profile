import json

from .edge import Vertex, Edge


class Profile:
    """Represents an extrusion profile"""
    PADDING = 0.1
    COST_PER_IN2 = 0.75

    def __init__(self, edges):
        self.edges = edges

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

    @property
    def machine_cost(self):
        return sum([e.cost for e in self.edges])

    @property
    def material_cost(self):
        x_min = min([e.x_min for e in self.edges])
        x_max = max([e.x_max for e in self.edges])
        y_min = min([e.y_min for e in self.edges])
        y_max = max([e.y_max for e in self.edges])
        total_area = (x_max - x_min + self.PADDING) * (y_max - y_min + self.PADDING)
        return total_area * self.COST_PER_IN2

    @property
    def cost(self):
        return round(self.machine_cost + self.material_cost, 2)

    @property
    def formatted_cost(self):
        return f"{self.cost:.2f} dollars"


def estimate_cost(filepath):
    profile = Profile.create_from_json(filepath)
    print(profile.formatted_cost)
