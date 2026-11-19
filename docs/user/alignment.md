# Alignment of double-sided boards

After the top side is milled, the board is turned over to mill the bottom. It never goes back in exactly the
same place. The **ALIGN** tab measures where the holes really are and corrects the jobs to match.

The tab is hidden by default: show it with **File › Show Align Tab**.

## Before starting

- Drill the board (or at least a few holes far apart) before turning it over.
- To find the holes with a camera, set the camera in **Settings/Preferences › Alignment Settings**:
  - **Get Tool Camera Offset**: put the tool on a mark, set the work zero there, move the camera over the
    same mark, then press the button; the distance between tool and camera is stored.
  - **Flip Camera Horizontally**, **Flip Camera Vertically** and **Rotate Camera** turn the image to match the
    movements of the machine.

## Measuring the points

1. Load the drill file with the load button of the tab. Use **FLIP HOR** or **FLIP VER** so that the holes are
   drawn as they are on the turned board.
2. Choose the camera in **Camera Selection** (or "No CAMERA" to use the tool) and the **Zoom**; the mouse
   wheel over the image also zooms.
3. **TOOL POSITION** / **CAMERA POSITION** says what you centre on the hole: the tip of the tool, or the centre of
   the camera image.
4. For each point:
   1. double-click a hole in the drawing to select it;
   2. jog the machine until the tool or the camera is centred on the same hole of the board;
   3. press **+** to add the point.

   **-** removes the selected points.
5. Measure at least 4 holes, far apart from each other.

## Applying the alignment

The apply button, on the ALIGN tab and on the CONTROL tab, turns the correction on and off for every job:

| Colour | State |
|---|---|
| no colour | fewer than 4 points |
| yellow | ready, not applied |
| blue | applied |

With the alignment applied, the selected job is drawn corrected in the CONTROL view and sent corrected.
