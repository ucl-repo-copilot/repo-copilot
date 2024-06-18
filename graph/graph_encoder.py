import json

from graph.graph import Graph


class GraphEncoder(json.JSONEncoder):
    """Custom JSON encoder for Graph objects."""

    def default(self, obj):
        """If Graph, convert to dict using to_dict method. Else, use default JSON encoder."""
        if isinstance(obj, Graph):
            return obj.to_dict()
        return obj.__dict__
