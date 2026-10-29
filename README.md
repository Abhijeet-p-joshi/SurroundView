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

![ClassDiagram.png](ClassDiagram.png)

# Repository structure

![RepositoryStructure.png](RepositoryStructure.png)

# CANoe Communication

![CANoeCommunication.png](CANoeCommunication.png)