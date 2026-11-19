# Creating a job

A job is a G-code file that machines one layer of the board. It is made from a loaded layer
([Loading layers](loading-layers.md)) and from the settings you choose for that layer.

Open **VIEW › CREATE JOB** and choose the layer in the list at the top. The tab shows the settings of that
layer and the view shows the layer. With no layer loaded the tab only says "Load a valid Layer".

Press **Generate Job**: the toolpath is drawn over the layer and the G-code is written in the
`gcode_temp_dir` folder as `<layer>_<type>.gcode`. To send it to the machine, add it to the list of the
**CONTROL › GCode** tab with the **Add generated G-code** button (see [Running a job](running-a-job.md)).

The settings of each layer are kept between sessions in `configurations/jobs_sets_config.ini`.

## Settings common to every layer

| Setting | Meaning |
|---|---|
| Tool Diameter [mm] | diameter of the cutting part of the tool, used to compute the toolpath |
| Cut Z [mm] | depth of the cut, from the work zero (negative is into the board) |
| Travel Z [mm] | height of the moves between cuts, from the work zero |
| Spindle Speed | spindle speed sent with `M3 S...` |
| XY Feed Rate [mm/min] | feed rate of the cutting moves |
| Z Feed Rate [mm/min] | feed rate when going down into the board |

All heights are measured from the work zero, so set Z = 0 on the copper surface before running the job
([Running a job](running-a-job.md#setting-the-work-zero)).

## TOP and BOTTOM: isolation

The tool goes around each copper area to separate it from the rest.

| Setting | Meaning |
|---|---|
| Number of Passes | how many paths go around each copper area; more passes remove more copper |
| Overlap | how much each pass covers the previous one, as a fraction of the tool diameter (0.4 = 40 %) |

The BOTTOM job is mirrored, since the board is turned over to mill it. The axis of the mirror is set in
**Settings/Preferences › Jobs/Machine Settings › Mirroring axis**: X turns the board top-down, Y left-right.

## PROFILE: cutting the board out

| Setting | Meaning |
|---|---|
| Margin [mm] | distance between the outline and the cut, added to the tool radius |
| Multi-depth | cut in several passes instead of one |
| Depth per Pass [mm] | depth of each pass with Multi-depth |
| Gaps layout | where the tabs that hold the board in the sheet are left: none, 1 or 2 per side, 1 per corner |
| Gap size [mm] | length of each tab |
| Mirror | mirror the path, for a profile cut from the bottom side |

## DRILL: holes

The table lists the drill bits. **+** adds a bit (0.8 mm by default, the diameter can be edited), **-** removes
the selected ones; Generate Job needs at least one bit.

Each hole is drilled with the largest bit that is not larger than the hole (with a 2 % tolerance). A hole
smaller than every bit is not drilled: the console says so; add a smaller bit.

| Setting | Meaning |
|---|---|
| Milling Tool | mill the holes that are larger than the milling tool instead of drilling them |
| Mill Tool Diameter [mm] | diameter of that tool |
| Algorithm | how the order of the holes is optimised: Nearest Insertion (fast), 2-opt (shorter path, slower) or Genetic |
| Mirror | mirror the holes, for drilling from the bottom side |

With more than one bit the job stops for a [tool change](tool-change.md) between them.
