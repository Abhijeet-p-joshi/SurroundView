# Running the Application

## Prerequisites
Install
- Python 3.12+
- CANoe 19 (64-bit)
- CANoe COM Interface enabled
- pywin32
- PySide6
- pyqtgraph

## CANoe Setup
1. Open the CANoe configuration.
2. Load the FlexRay databases.
3. Include **SurroundVew.can** file in the ASDM node 
 - File can be found in https://intranet.volvocars.net/:f:/r/sites/DriverInformation/Shared%20Documents/Argus3%20Surround%20view?d=w47f35eeeb43a44f29cc2bf2836b0601e&csf=1&web=1&e=HtXDIg)
4. Compile the node successfully.
3. Start Measurement.
4. Verify all required System Variables exist:
   - ASDM::Obj01_X … Obj18_X
   - ASDM::Obj01_Y … Obj18_Y
   - ASDM::Obj01_Type … Obj18_Type
   - ASDM::LaneA_a … LaneD_Position
   - ASDM::InjectionEnable
5. Ensure the CAPL node is running.

## Start the GUI
- cd SurroundView(root folder)
- Run 'python main.py' in the terminal

## Injection Workflow
1. Open Inject tab.
2. Configure up to 18 objects.
3. Press Apply Scenario. This shows objects in the visualization panel.
4. Press Start Injection.
5. CANoe System Variables are updated.
6. CAPL copies System Variables into FlexRay signals.
7. DIM displays the objects. (if connected)

## Lane Geometry Workflow
1. Open Lane Geometry tab.
2. Enter
   - a for each lane.
   - b for each lane.
   - c for each lane.
   - d1 for each lane.
   - d2 for each lane.
3. Press Apply Lanes.
4. Press Start Injection in Object tab
5. The application
- Updates CANoe System Variables.
- Updates the visualization.
- CAPL continuously publishes System Variables to FlexRay signals.
6. DIM displays the lanes. (if connected)

## Replay Workflow
1. Open Replay tab.
2. Select a CANoe log.
3. Press Start Replay.
4. ReplayController reads CANoe signals.
5. Visualization updates automatically.