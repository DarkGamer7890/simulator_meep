from core.geometry.registry import GEOMETRY_REGISTRY


def build_geometry(geom_type, params):
    if geom_type not in GEOMETRY_REGISTRY:
        raise ValueError(f"Unknown geometry type: {geom_type}")

    builder_cls = GEOMETRY_REGISTRY[geom_type]
    builder = builder_cls(**params)
    return builder.build()
