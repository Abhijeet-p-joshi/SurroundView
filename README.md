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