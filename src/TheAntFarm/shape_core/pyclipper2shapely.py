# FROM: https://www.programcreek.com/python/?code=tilezen%2Fmapbox-vector-tile%2Fmapbox-vector-tile-master%2Fmapbox_vector_tile%2Fpolygon.py
# LICENSE: MIT

import logging
from typing import List, Tuple, Union, Any

import pyclipper as pc
from shapely.geometry import Polygon, MultiPolygon, LinearRing
from shapely.ops import unary_union
from shapely.validation import explain_validity, make_valid

logger = logging.getLogger(__name__)


def _contour_to_linear_ring(contour_in: Any, scale: float) -> LinearRing:
    """
    Converts a Clipper contour to a Shapely LinearRing.
    """
    contour = contour_in
    if scale:
        contour = pc.scale_from_clipper(contour_in)
    
    # Clipper contours might not be closed, Shapely LinearRings must be.
    # Shapely auto-closes if the last point != first point, but let's be safe.
    if len(contour) < 3:
        return LinearRing() # Invalid ring

    try:
        ring = LinearRing(contour)
    except Exception as e:
        logger.warning(f"Failed to create LinearRing from contour: {e}")
        return LinearRing()

    if not ring.is_valid:
        # Try to fix self-intersections or other issues
        # make_valid on a LinearRing usually returns a MultiLineString or GeometryCollection
        # We need a valid ring for the polygon constructor.
        # If it's invalid, it's often better to let the Polygon constructor handle it via make_valid later,
        # or try to simplify.
        # For now, we return it as is, and the Polygon validation will catch it.
        pass
        
    return ring


def _polytree_node_to_shapely(node: Any, scale: float) -> Tuple[List[Polygon], List[LinearRing]]:
    """
    Recurses down a Clipper PolyTree, extracting the results as Shapely objects.
    
    Logic:
    - A PolyTree node represents a nesting level.
    - If node.IsHole is False (Outer):
        - It defines a Polygon Shell.
        - Its children are Holes.
        - Its grandchildren are nested Polygons (Islands).
    - If node.IsHole is True (Hole):
        - It defines a Hole for its parent.
        - Its children are nested Polygons (Islands).
    
    Returns:
        (polygons, holes)
        - polygons: List of fully constructed Polygons found at this level and below.
        - holes: List of LinearRings representing holes to be passed up to the parent.
    """
    polygons = []
    holes = []
    
    # 1. Process Children
    # Children of this node.
    # If this node is Outer, children are Holes.
    # If this node is Hole, children are Outers (Islands).
    
    child_holes = [] # Holes to be applied to THIS node (if it's an Outer)
    
    for ch in node.Childs:
        child_polys, child_rings = _polytree_node_to_shapely(ch, scale)
        
        # Any polygons found deeper down are independent islands, add them to our list
        polygons.extend(child_polys)
        
        # Any rings returned by children are holes for US
        child_holes.extend(child_rings)

    # 2. Process Current Node
    if node.Contour:
        ring = _contour_to_linear_ring(node.Contour, scale)
        
        if not ring.is_empty:
            if node.IsHole:
                # If I am a hole, I pass my ring up to my parent to be used as a hole.
                # My children (which are Outers) have already been processed and added to 'polygons'.
                holes.append(ring)
            else:
                # If I am an Outer, I am a Polygon Shell.
                # My children are holes for me.
                try:
                    poly = Polygon(shell=ring, holes=child_holes)
                except Exception as e:
                    logger.warning(f"Failed to construct Polygon: {e}")
                    poly = Polygon()

                if not poly.is_valid:
                    poly = make_valid(poly)

                if poly.geom_type == "MultiPolygon":
                    polygons.extend(poly.geoms)
                elif poly.geom_type == "Polygon":
                    polygons.append(poly)
                elif poly.geom_type == "GeometryCollection":
                     for g in poly.geoms:
                         if g.geom_type in ["Polygon", "MultiPolygon"]:
                             if g.geom_type == "MultiPolygon":
                                 polygons.extend(g.geoms)
                             else:
                                 polygons.append(g)
    else:
        # Root node (usually has no contour, not a hole)
        # Just pass up the polygons collected from children
        pass

    return polygons, holes


def _polytree_to_shapely(tree: Any, scale: float) -> Union[Polygon, MultiPolygon]:
    polygons, holes = _polytree_node_to_shapely(tree, scale)

    # The root should not return holes, only polygons.
    if len(holes) > 0:
        logger.warning("Root node returned holes, which should be impossible for a valid PolyTree.")

    if not polygons:
        return Polygon()

    union = unary_union(polygons)
    
    if not union.is_valid:
        union = make_valid(union)
        
    return union


def polytree_to_shapely(tree: Any, scale: float = 1.0) -> Union[Polygon, MultiPolygon]:
    """
    Main entry point to convert a Clipper PolyTree to a Shapely geometry.
    """
    return _polytree_to_shapely(tree, scale)
