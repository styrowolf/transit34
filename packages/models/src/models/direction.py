from enum import Enum


class Direction(str, Enum):
    OUTBOUND = "outbound"  # gidiş
    INBOUND = "inbound"  # dönüş

    @staticmethod
    def from_int(direction: int):
        if direction == 119:
            return Direction.OUTBOUND
        elif direction == 120:
            return Direction.INBOUND
        else:
            return None

    @staticmethod
    def from_str(direction: str):
        if direction == "G":
            return Direction.OUTBOUND
        elif direction == "D":
            return Direction.INBOUND
        else:
            return None

    @staticmethod
    def from_route_pattern(pattern_code: str):
        return Direction.from_str(pattern_code.split("_")[1])
