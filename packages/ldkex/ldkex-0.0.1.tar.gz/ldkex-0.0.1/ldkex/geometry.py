from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Geometry:
    coordinates: List
    name: str
    color_hex: str
    metadata: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))

    @property
    def geometry_type(self):
        raise NotImplementedError("Subclasses should implement this property")

    @property
    def sidc(self):
        raise NotImplementedError("Subclasses should implement this property")

    def to_feature(self):
        return {
            "type": "Feature",
            "properties": {
                "name": self.name,
                "sidc": self.sidc,
                "outline-color": self.color_hex,
                "comments": []
            },
            "geometry": {
                "type": self.geometry_type,
                "coordinates": self.coordinates
            }
        }


@dataclass
class Point(Geometry):
    coordinates: List[float]

    @property
    def geometry_type(self):
        return "Point"

    @property
    def sidc(self):
        return "10012500001313000000"


@dataclass
class Line(Geometry):
    coordinates: List[List[float]]

    @property
    def geometry_type(self):
        return "LineString"

    @property
    def sidc(self):
        return "10016600001100000000"


@dataclass
class Polygon(Geometry):
    coordinates: List[List[List[float]]]

    @property
    def geometry_type(self):
        return "Polygon"

    @property
    def sidc(self):
        return "10012500001505010000"
