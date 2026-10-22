# Software Architecture

## Layered architecture
            GUI

             │

      Visualization

             │

      Data Manager

        ↙       ↘

    CANoe         CSV

        ↘       ↙

         Data Model

## Data Flow
Suppose you enter
X = 50
Y = 70

**Flow**
GUI
↓
Data Model
↓
CANoe Interface
↓
System Variable
↓
Vector Hardware
↓
ECU

**Simultaneously**
GUI
↓
Data Model
↓
Visualization
↓
Move Point

## Design
        SurroundView (Python GUI)
                 │
                 ▼
        User enters coordinates
                 │
        ┌────────┴────────┐
        ▼                 ▼
 Visualization      FlexRay Signals
 (Immediate)             │
                          ▼
                     CANoe Database
                          │
                     Measurement
                          │
                     VN8914 Interface
                          │
                          ▼
                         ECU

## Introduce the controller
GUI
 │
 ▼
Controller
 │
 ├──► Visualization
 │
 └──► CANoe
 
This follows the Model–View–Controller (MVC) pattern.

The advantages are:
- The control panel doesn't know the visualization exists.
- The visualization doesn't know CANoe exists.
- CANoe doesn't know about the GUI.
When you press Apply, the controller will:
1. Receive the objects.
2. Update the visualization.
3. Write the FlexRay signals.
4. Log the operation (later).

                      MainWindow
                          │
           ┌──────────────┴──────────────┐
           │                             │
      ControlPanel               SurroundViewWidget
           │
           │ apply_clicked(objects)
           ▼
         SurroundViewController
            │             │
            ▼             ▼
 Visualization       CANoe (later)


 # Final implementation

                 +-----------------------------+
                |      Python GUI             |
                | (PySide6 + PyQtGraph)       |
                +--------------+--------------+
                               |
                               | Apply
                               |
                               ▼
                    SurroundViewController
                               |
                 +-------------+-------------+
                 |                           |
                 ▼                           ▼
         Visualization                CANoe Interface
         (PyQtGraph)                     (COM API)
                 |                           |
                 |                           ▼
                 |                  Symbolic Signals
                 |                           |
                 ▼                           ▼
            2D Display             FlexRay Database Signals
                                           |
                                           ▼
                                        VN8914
                                           |
                                           ▼
                                          ECU