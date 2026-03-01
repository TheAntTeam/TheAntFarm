import logging
from typing import List, Tuple, Any, Optional

import numpy as np
from shapely.geometry import LineString, Point
from scipy.spatial import distance

logger = logging.getLogger(__name__)


class GerberPathOptimizer:
    """
    Optimizes the milling path for Gerber files (traces/profiles).
    The goal is to minimize the travel distance (rapid moves) between milling operations.
    This is a variation of the Rural Postman Problem, solved here with a Greedy Nearest Neighbor approach.
    """

    def __init__(self, lines: List[LineString]) -> None:
        """
        Initialize the optimizer.

        :param lines: List of shapely.geometry.LineString objects representing the cuts.
        """
        self.lines = lines
        # Store start and end points for fast access
        # coords[i][0] is start, coords[i][-1] is end
        self.endpoints = []
        for line in lines:
            coords = list(line.coords)
            self.endpoints.append((coords[0], coords[-1]))
        
        self.num_lines = len(lines)
        self.visited = [False] * self.num_lines

    def optimize(self, start_point: Tuple[float, float] = (0.0, 0.0)) -> List[LineString]:
        """
        Reorders and potentially reverses the lines to minimize travel distance.

        :param start_point: The starting position of the tool (default: 0,0).
        :return: Optimized list of LineString objects.
        """
        if not self.lines:
            return []

        optimized_path: List[LineString] = []
        current_pos = start_point
        
        # We can use a spatial index (KDTree) for faster lookups if N is large.
        # For typical PCB paths (N < 10000), a simple vectorized search or even loop might suffice,
        # but let's try to be reasonably efficient.
        
        # Flatten endpoints for vectorized distance calculation:
        # [start_0, end_0, start_1, end_1, ...]
        # We will mask visited points by setting them to infinity.
        
        all_endpoints = np.array([pt for pair in self.endpoints for pt in pair])
        # Map from flat index back to line index: 0->0, 1->0, 2->1, 3->1 ...
        flat_to_line_idx = np.repeat(np.arange(self.num_lines), 2)
        
        # Mask to keep track of available endpoints (True = available)
        available_mask = np.ones(len(all_endpoints), dtype=bool)

        logger.info(f"Optimizing Gerber path with {self.num_lines} segments...")

        for _ in range(self.num_lines):
            # Calculate distances from current_pos to all available endpoints
            # Note: cdist expects 2D arrays
            dists = distance.cdist([current_pos], all_endpoints, "euclidean")[0]
            
            # Set distances of visited lines to infinity
            # We check the mask. If a line is visited, both its start and end are unavailable.
            dists[~available_mask] = np.inf
            
            # Find the nearest endpoint
            nearest_flat_idx = np.argmin(dists)
            
            # If all are inf, we are done (shouldn't happen in this loop structure)
            if dists[nearest_flat_idx] == np.inf:
                break
                
            line_idx = flat_to_line_idx[nearest_flat_idx]
            
            # Determine orientation
            # nearest_flat_idx is even -> Start point is closer -> Normal direction
            # nearest_flat_idx is odd  -> End point is closer   -> Reverse direction
            is_start_closer = (nearest_flat_idx % 2 == 0)
            
            line = self.lines[line_idx]
            
            if is_start_closer:
                # A -> B
                optimized_path.append(line)
                current_pos = self.endpoints[line_idx][1] # New pos is End
            else:
                # B -> A (Reverse)
                reversed_line = LineString(list(line.coords)[::-1])
                optimized_path.append(reversed_line)
                current_pos = self.endpoints[line_idx][0] # New pos is Start (which was the original Start)

            # Mark line as visited
            # Disable both start (2*line_idx) and end (2*line_idx + 1) in the mask
            available_mask[2 * line_idx] = False
            available_mask[2 * line_idx + 1] = False

        logger.info("Gerber path optimization complete.")
        return optimized_path
