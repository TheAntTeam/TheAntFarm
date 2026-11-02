
# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [Unreleased]

### Added

- Rebuilt the macro system around a single validated tag catalog: unknown or malformed placeholders are refused instead of being sent to the machine, templates are validated when loaded and the expansion of every template is covered by golden tests.
- Added three selectable tool change procedures: work zero re-datum (`wcs`, default), dynamic tool length offset (`tlo`) and fixed tool setter (`setter`), selected with `tool_change_mode`.
- Tool change macro: two stage probing, spindle stop with dwell and restart, `G21`/`G49` and an explicit message on the manual change.
- Added `docs/macros.md`: design of the macro system, firmware capabilities and the backlog of the open work.

### Fixed

- Drilling: the centre and the diameter of a hole are now computed per polygon part (a slot joined to a pad no longer raises), the bit is never larger than the hole and a bit used for a single hole is drilled once.
- Design rule check: the invalid path indices are remapped after the minimum area filter, so the warning points to the right path.
- G-code writer: a missing `multi_depth` key and a zero cut depth no longer raise (`KeyError`/`ZeroDivisionError`).
- Alignment: an empty or degenerate (collinear) set of alignment points is refused instead of crashing the application.
- Tool change: the FluidNC per-axis tool length offset report is parsed, a failed probing cycle is discarded instead of being used as a measurement, the job is stopped when the macro cannot run, and the tool change reliably starts only when the machine is idle.
- `offset_polygon_holes` returns `None` when no hole survives the offset.

### Changed

- Packaging: the project requires Python 3.10-3.12 (gerbyx needs 3.10), `shiboken2` is now `shiboken6`, the cairocffi dependency family of pcb-tools is gone, the PyInstaller spec bundles the gerbyx parser and the build workflow uses the right spec and artifact name.
- `shape_core` publishes its API from the package (`from shape_core import GCoder, MachinePath, ...`); the visualization layer is imported on demand and the controllers import the classes from the package instead of the single modules.
- The toolpaths are `ToolPath` objects and the defaults of the toolpath generator, of the G-code writer and of the probe managers live in `shape_core/config.py`; a partial configuration is merged with the defaults instead of raising.
- Completed cleanup of legacy pcb-tools usage in PCB manager, keeping the active parsing pipeline on gerbyx.
- Removed legacy/unused pcb-tools-based code paths and backup file in shape_core.
- Updated packaging and documentation references from pcb-tools to gerbyx.


## [0.3.2] - Jan 10, 2026

### Added

- Draft for test development

### Fixed

- Corrected calls parameters in the GridLayout addWidget call for updated API in pyside 6 vs 2
- Cleared camera image when there is no new image streamed
- Fixed property name in settings save function
- Fixed error occurring when a point position was grabbed in the alignment tab before displaying the value
- Fixed a bug when importing Gerber files containing REGION primitives. If these primitives included arcs, a bug occurred in the handling of this geometry type. As a result, the REGION primitives were reconstructed incorrectly.
- Resolved bug on multiple drilling paths visualization

### Changed

- Improved selection of items in gcode table 
- Progress bar now displays elapsed time tracking with HH:MM:SS format.
- Enhanced progress tracking with 2-decimal precision percentage display (e.g., "45.67% - 00:02:34").


## [0.3.1] - Aug 21, 2025

### Fixed

- Fixed spec file for generation of Ubuntu OS executable.
- Fixed spec file for generation of Windows OS executable.
- Fixed dll path for Windows executable. 
- Fixed status tips for alignment buttons.

### Changed

- GH Actions generates executable for both python 3.10 and 3.12.
- Renewed UI generated from pyside 6 designer tool.

## [0.3.0] - Jun 28, 2025

### Added

- Migrated to PySide6 version.
- Updated the way the camera devices info are obtained. 
- Added a check on the serial ports in case there's none.
- NC files can be loaded in the control tab and are now automatically loaded if they are in the gcode_temp_dir
- Updated version of packages in toml file and requirements.txt.

### Fixed

- Fixed color picking in settings preferences
- Workaround added to solve Pyside6 QTMultimedia bug with recent python versions. See [https://bugreports.qt.io/browse/PYSIDE-2935?attachmentViewMode=list]
- Minor fix on regex pattern string in controller_manager.py
- Bug Fix on geometry_manager.py. the is_overlaping_multiple_polygons method failed when comparing a polygon to many polygons
- Override pcb-tools read function to be compatible with python 3 most recent versions.

### Changed

- Improvement in visual manager routines. Speed up of gcode visualization.    

## [0.2.1] - Aug 11, 2024  

Bugfix to be able to generate executable using pyinstaller and added executable's icon.
 
## [0.2.0] - Aug 11, 2024  
 
Added first implementation of alignment tab based on manual selection of points in
the loaded layer and positioning of the machin tool using camera.
This allows to create double sided PCB aligning them optically.


### Camera Functionality Improvements:
- **Camera Selection and Deselection**: Added the ability to deselect the camera when the application closes and improved camera selection management, including adding a default "NO Camera" option to avoid accidental startups.
- **Camera Zoom**: Linked the camera zoom combobox to update the view and added mouse wheel events to control the zoom.
- **Camera Alignment**: Improved synchronization of alignment buttons, connected camera zoom to the frame manager, and added support for selecting alignment points, including the ability to remove points.

### Alignment Procedure Enhancements:
- **Alignment Point Management and Visualization**: Introduced a system to manage alignment points, including the removal of points and visual synchronization when alignment is applied. Added signals to update the coordinates of alignment points.
- **Path Optimization Algorithms**: Implemented and optimized a genetic algorithm to optimize the drilling path, also adding other algorithms like "nearest_insertion" and "two_opt". 

### User Interface Improvements:
- **UI Changes**: Made numerous changes to enhance the user experience, such as reorganizing the alignment tab, adding new control elements, and connecting various signals to synchronize the application state.
- **LED Indicators**: Added visual LEDs to signal the status of various processes, such as probing and alignment.
- **GCode File Handling**: Added the ability to load GCode files as a reference for alignment and improved the integration of the alignment system with the main program.

### Bug Fixes and Optimizations:
- **Minor Fixes**: Resolved various bugs, such as issues with camera image misalignment, minor UI errors, and incorrect conditions. Improved handling of variables and boundary conditions in XY and Z movements.
- **MacOS Compatibility**: Termporarily removed generation of executable for ARM64 processor for MacOS.  

### Other Enhancements:
- **DRC and Camera Offset**: Implemented a validity check for Gerber paths and optimized the use of working positions instead of machine positions to get the camera-tool offset.
- **Integration of New Features**: Added a new `AlignManager` class to handle alignment and introduced a new alignment algorithm.

 
## [0.1.1] - May 13, 2023  
  
Modified python-app.yml and added files to generate executables for 3 main OS using  
github actions.

### **Version and Documentation Updates**:
   - **Version Bump**: Updated the project version to 0.1.1.
   - **Documentation**: Enhanced and moved documentation to the wiki and updated `CommandManager` documentation.

### **Build Process Enhancements**:
   - **Artifact Handling**: Improved artifact naming and handling for different Python versions and operating systems.
   - **Path and File Management**: Corrected paths for YAML files, executable runs, and excluded certain files from linting.
   - **CI Configuration**: Adjusted the CI pipeline to support specific Python versions, use a matrix strategy, and added conditional artifact uploads.

### **Compatibility and Dependency Management**:
   - **Python Version**: Managed support for different Python versions (added 3.11, later removed due to incompatibility).
   - **Shapely Library**: Addressed deprecation warnings and made preventive changes for Shapely >= 2.0.
   - **`pyinstaller` Support**: Added spec file and adjustments to support building with `pyinstaller`.

### **Miscellaneous Changes**:
   - **UI Updates**: Made minor changes to how status signals are managed and displayed in the UI.
   - **Packaging**: Added `pyproject.toml` for package management using `poetry` (not used at the moment).

 
## [0.1.0] - Oct 07, 2022  
 
First issue of The Ant Farm, implemented functionality to generate gcode from TOP, 
BOTTOM, DRILL and EDGE gerber/excellon layers.  
Implemented Control tab to load gcode and manage CNC controllers using GRBL 1.x.  

### **Initial Setup and Core Functionality**:
   - Introduction of new features like UI improvements, gcode generation, and tool change automation.
   - Added handling for different file formats, including Gerber and Excellon files, with support for metric and imperial units.
   - Improvements to core functionalities like drill file processing, layer management, and gcode visualization.

### **Bug Fixes and Issue Resolution**:
   - Numerous bug fixes addressing issues like loading files without geometries, converting units, and serial port communication.
   - Resolved issues related to gcode generation, such as handling empty layers, mirroring, and feedrate errors.
   - Fixes for threading issues, error handling, and UI bugs.

### **Enhancements and Refactoring**:
   - Enhanced user interface with better management of settings, color selections, and shortcut keys.
   - Refactoring of code to improve structure, including splitting large classes into smaller, more manageable parts.
   - Added features like tool change settings, probe offsets, and automated boundary box (ABL) processing.

### **Documentation and Readability**:
   - Added and updated documentation, including comments, docstrings, and the README file.
   - Improved code readability by translating comments into English and following coding style guidelines.

### **Version Control and Compatibility**:
   - Managed dependencies and compatibility with different Python versions.
   - Set up environment settings for different operating systems, including Windows, Linux, and Mac.

### **Testing and Optimization**:
   - Added tests and debugging tools to improve reliability and performance.
   - Implemented optimizations to reduce gcode complexity and improve processing speed.

### **Final Touches and Releases**:
   - Prepared the project for release with a new logo, version tagging, and final code clean-up.
   - Updated requirements, resources, and icons, preparing the application for broader use.
