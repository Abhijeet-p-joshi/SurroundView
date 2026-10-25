from injection.scenario import Scenario


class ScenarioBuffer:
    """
    Stores the currently active injection scenario.

    Responsibilities
    ----------------
    - Hold exactly one active Scenario.
    - Provide sorted object access.
    - Allow replacing the active scenario.
    - Provide validation/status information.

    This class contains no GUI logic and no CANoe logic.
    """

    def __init__(self):

        self._scenario = Scenario()

    # ---------------------------------------------------------
    # Scenario Management
    # ---------------------------------------------------------

    def set_scenario(self, scenario: Scenario):
        """
        Replace the current scenario with a copy.

        A copy is stored so that further edits in the
        Scenario Editor do not modify the active scenario
        until Apply Scenario is pressed again.
        """

        self._scenario = Scenario(
            name=scenario.name,
            objects=list(scenario.objects)
        )

    def get_scenario(self) -> Scenario:
        """
        Returns the active scenario.
        """
        return self._scenario

    def clear(self):
        """
        Clears the active scenario.
        """
        self._scenario = Scenario()

    # ---------------------------------------------------------
    # Object Access
    # ---------------------------------------------------------

    def get_objects(self):
        """
        Returns all objects sorted by slot number.
        """
        return self._scenario.sorted_objects()

    def get_object(self, slot: int):
        """
        Returns one object by logical slot number.
        """
        return self._scenario.get_object(slot)

    def object_count(self):
        return self._scenario.object_count()

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def has_scenario(self):
        return self.object_count() > 0

    def is_valid(self):
        return self._scenario.is_valid()

    def is_empty(self):
        return self.object_count() == 0

    # ---------------------------------------------------------
    # Utility
    # ---------------------------------------------------------

    def scenario_name(self):
        return self._scenario.name

    def __len__(self):
        return self.object_count()

    def __iter__(self):
        return iter(self.get_objects())

    def __str__(self):
        if self.is_empty():
            return "ScenarioBuffer (Empty)"
        
        return (
            f"ScenarioBuffer("
            f"name='{self.scenario_name()}', "
            f"objects={self.object_count()})"
        )