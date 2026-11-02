"""Types shared by the toolpath generator, the G-code writer and the viewer."""

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class ToolPath:
    """A group of toolpaths machined with the same tool and procedure.

    Parameters
    ----------
    tool_diameter : float
        Diameter of the tool used for the group, in mm.
    machining_type : str
        ``"gerber"``, ``"profile"``, ``"pocketing"`` or ``"drill"``.
    paths : list
        The geometries to machine, usually ``shapely.geometry.LineString``
        (for the drilling they are the sequences of the holes of one bit).
    invalid_ids : list of int
        Positions in ``paths`` flagged by the design rule check: they are drawn
        with a warning colour and reported to the user.
    """

    tool_diameter: float
    machining_type: str
    paths: List[Any] = field(default_factory=list)
    invalid_ids: List[int] = field(default_factory=list)

    def __repr__(self) -> str:
        return (
            f"ToolPath({self.machining_type}, tool={self.tool_diameter} mm, "
            f"{len(self.paths)} paths, {len(self.invalid_ids)} invalid)"
        )
