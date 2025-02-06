from typing import List
from rayforge.config import config
from rayforge.modifier import Modifier, \
                              MakeTransparent, \
                              ToGrayscale, \
                              OutlineTracer
from .machine import LaserHead
from .workpiece import WorkPiece
from .path import Path


class WorkStep:
    """
    A WorkStep is a set of Modifiers that operate on a set of
    WorkPieces. It normally generates a Path in the end, but
    may also include modifiers that manipulate the input image.
    """

    def __init__(self, name):
        self.name: str = name
        self.workpieces: List[WorkPiece] = []
        self.modifiers: List[Modifier] = [
            MakeTransparent(),
            ToGrayscale(),
            OutlineTracer(),
        ]
        self.path: Path = Path()
        self.laser: LaserHead = config.machine.heads[0]
        self.power = self.laser.max_power
        self.cut_speed = config.machine.max_cut_speed
        self.travel_speed = config.machine.max_travel_speed

    def get_summary(self):
        power = int(self.power/self.laser.max_power*100)
        speed = int(self.cut_speed)
        return f"{power}% power, {speed} mm/min"

    def add_workpiece(self, workpiece: WorkPiece):
        self.workpieces.append(workpiece)

    def remove_workpiece(self, workpiece):
        self.workpieces.remove(workpiece)

    def dump(self, indent=0):
        print("  "*indent, self.name)
        for workpiece in self.workpieces:
            workpiece.dump(1)
