import json

from graph import Graph

class GraphEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Graph):
            return obj.to_dict()
        return obj.__dict__