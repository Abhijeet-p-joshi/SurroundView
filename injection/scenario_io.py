import json
from pathlib import Path

from injection.scenario import Scenario
from models import DetectedObject, ObjectType


class ScenarioIO:

    DEFAULT_FILE = (
        Path(__file__).parent.parent
        / "scenarios"
        / "default.json"
    )

    # ---------------------------------------------------------

    @classmethod
    def load(cls):

        path = cls.DEFAULT_FILE

        if not path.exists():

            scenario = Scenario(
                name="Default Scenario"
            )

            cls.save(scenario)

            return scenario

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        scenario = Scenario(
            name=data.get(
                "name",
                "Default Scenario"
            )
        )

        for item in data.get(
            "objects",
            []
        ):

            obj = DetectedObject(
                slot=item["slot"],
                object_type=ObjectType[
                    item["type"]
                ],
                x=item["x"],
                y=item["y"],
            )

            scenario.add_object(obj)

        return scenario

    # ---------------------------------------------------------

    @classmethod
    def save(
        cls,
        scenario: Scenario,
    ):

        path = cls.DEFAULT_FILE

        path.parent.mkdir(
            exist_ok=True
        )

        objects = []

        for obj in scenario.sorted_objects():
            objects.append(
                {
                    "slot": obj.slot,
                    "type": obj.object_type.name,
                    "x": obj.x,
                    "y": obj.y,
                }
            )

        data = {
            "name": scenario.name,
            "objects": objects,
        }

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )