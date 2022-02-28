from enum import Enum

class RequestType(str, Enum):
    QUERY = 'query'
    MUTATION = 'mutation'


class GpsCarrierPhaseStatus(str, Enum):
    STANDARD = 'STANDARD'
    FLOAT = 'FLOAT'
    FIXED = 'FIXED'


class ColorApplied(str, Enum):
    UNKOWN = 'UNKOWN'
    NONE = 'NONE'
    RED_TO_GREEN = 'RED_TO_GREEN'


class SensorType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    RGB = 'RGB'
    RGNIR = 'RGNIR'
    RGRE = 'RGRE'
    MULTISPECTRAL = 'MULTISPECTRAL'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    RED = 'RED'
    RE = 'RE'
    NIR = 'NIR'
    LWIR = 'LWIR'


class CalculatedIndex(str, Enum):
    UNKNOWN = 'UNKNOWN'
    NONE = 'NONE'
    NDVI = 'NDVI'
    NDRE = 'NDRE'