# Architecture Diagram

                         +----------------------------------+
                         |          SurroundView GUI        |
                         |----------------------------------|
                         | Inject Tab                       |
                         | Replay Tab                       |
                         | Lane Geometry Tab                |
                         +----------------+-----------------+
                                          |
                                          |
                           User Actions   |
                                          v
                 +--------------------------------------+
                 |            Controllers               |
                 |--------------------------------------|
                 | Injection Controller                 |
                 | Replay Controller                    |
                 | Lane Controller                      |
                 | Visualization Controller             |
                 +----------------+---------------------+
                                  |
               +------------------+------------------+
               |                                     |
               v                                     v
      +--------------------+              +----------------------+
      |   CANoe Interface  |              | Visualization Widget |
      |--------------------|              |----------------------|
      | write_scenario()   |              | draw_objects()       |
      | write_lane()       |              | draw_lanes()         |
      | COM Interface      |              | PyQtGraph            |
      +---------+----------+              +-----------+----------+
                |                                     ^
                |                                     |
                v                                     |
         +--------------+                     +------------------+
         | CANoe System |                     | Lane Geometry    |
         | Variables    |                     | Polynomial Model |
         +------+-------+                     +------------------+
                |
                |
                v
          +-------------+
          | CAPL Script |
          +------+------+
                 |
                 |
                 v
          FlexRay Signals

# Class diagram

                         MainWindow
                              │
         ┌────────────────────┼─────────────────────┐
         │                    │                     │
         │                    │                     │
         ▼                    ▼                     ▼
    InjectTab            ReplayTab            LaneEditor
         │                    │                     │
         │                    │                     │
         ▼                    ▼                     ▼
InjectionController   ReplayController      LaneController
         │                    │                     │
         └──────────────┬─────┴─────────────────────┘
                        │
                        ▼
              VisualizationController
                        │
                        ▼
              SurroundViewWidget
                        │
         ┌──────────────┴───────────────┐
         │                              │
         ▼                              ▼
  Object Rendering              Lane Rendering
         │                              │
         └──────────────┬───────────────┘
                        ▼
                 CANoeInterface
                        │
                        ▼
              Python COM Automation
                        │
                        ▼
                     CANoe
                        │
                        ▼
                 CAPL Scheduler
                        │
                        ▼
                FlexRay Signal Output

# Repository structure

SurroundView
│
├── canoe/
│      CANoe COM interface
│      Signal mapping
│      System variable access
│
├── config/
│      Global constants
│      ECU mappings
│
├── controllers/
│      Business logic
│
├── gui/
│      Qt widgets
│
├── models/
│      Data classes
│
├── replay/
│      Replay engine
│
├── injection/
│      Injection engine
│
├── visualization/
│      Object and lane rendering
│
├── scenarios/
│      JSON scenarios
│
└── main.py

# MVC Architecture

                 GUI
                  │
                  │ Signals
                  ▼
             Controllers
                  │
                  ▼
              Data Models
                  │
         +--------+--------+
         |                 |
         ▼                 ▼
 Visualization        CANoe Interface
         │                 │
         ▼                 ▼
    PyQtGraph         System Variables

# Injection flow

User
 │
 ▼
Apply Scenario
 │
 ▼
InjectionController
 │
 ▼
Scenario
 │
 ▼
CANoeInterface.write_scenario()
 │
 ▼
CANoe System Variables
 │
 ▼
CAPL Scheduler
 │
 ▼
FlexRay Signals
 │
 ▼
ECU

# Replay flow

User
 │
 ▼
Apply Scenario
 │
 ▼
InjectionController
 │
 ▼
Scenario
 │
 ▼
CANoeInterface.write_scenario()
 │
 ▼
CANoe System Variables
 │
 ▼
CAPL Scheduler
 │
 ▼
FlexRay Signals
 │
 ▼
ECU

# Lane flow

Lane Geometry Tab
 │
 ▼
LaneController
 │
 ▼
CANoeInterface.write_lane()
 │
 ▼
System Variables
 │
 ▼
CAPL
 │
 ▼
Lane Signals
 │
 ▼
Visualization

# Visualization Pipeline

Detected Objects
        │
        ▼
Visualization Controller
        │
        ▼
SurroundViewWidget
        │
        ├── Draw Vehicles
        ├── Draw Ego Vehicle
        ├── Draw Grid
        └── Draw Lane Geometry

# CANoe Communication

Python GUI
 │
 ▼
win32com
 │
 ▼
CANoe COM API
 │
 ▼
System Variables
 │
 ▼
CAPL
 │
 ▼
FlexRay Frames