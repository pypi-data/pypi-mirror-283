from dataclasses import dataclass


@dataclass
class Polygon:
    lon_left: float
    lon_right: float
    lat_top: float
    lat_bottom: float
    count: int
