# Quick start

From the Gerber files of a board to a milled board, for one side. Each step links to its page.

1. **Load the layers.** In **VIEW › LOAD LAYERS**, load the top copper with **TOP**, the outline with
   **PROFILE** and the holes with **DRILL**. → [Loading layers](loading-layers.md)
2. **Make the jobs.** In **VIEW › CREATE JOB**, choose each layer, check the tool and the depths, and press
   **Generate Job**. → [Creating a job](creating-a-job.md)
3. **Connect.** In **CONTROL**, press **Refresh**, choose the port and press **Connect**. Home the machine
   with **HOME**, if it has limit switches. → [Running a job](running-a-job.md#connecting)
4. **Set the work zero.** Jog the tool to the corner of the board and press **XY = 0**; bring it to the
   copper and press **Z = 0**, or probe it. → [Setting the work zero](running-a-job.md#setting-the-work-zero)
5. **Run.** In the **GCode** tab, press **Add generated G-code**, select the isolation job and press
   **PLAY**. Then the drill job, then the profile. → [Sending a job](running-a-job.md#sending-a-job)

For a double-sided board, mill the bottom side after turning the board over, with the
[alignment](alignment.md).

To try all of this without a machine, enable the [GRBL simulator](simulator.md).
