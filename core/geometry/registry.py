GEOMETRY_REGISTRY = {}


def register_geometry(name: str):

    def decorator(cls):
        GEOMETRY_REGISTRY[name] = cls
        return cls
    return decorator
