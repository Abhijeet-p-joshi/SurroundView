import json
import sys
from pathlib import Path

from injection.scenario import Scenario
from models import DetectedObject, ObjectType
from models.lane import Lane, LanePosition


class ScenarioIO:

    # Determine project folder
    if getattr(sys, "frozen", False):
        # Running from executable
        BASE_DIR = Path(sys.executable).parent

    else:
        # Running from Python
        BASE_DIR = Path(__file__).resolve().parent.parent

    DEFAULT_FILE = (
        BASE_DIR
        / "scenarios"
        / "default.json"
    )

    # ---------------------------------------------------------

    @classmethod
    def load(cls):

        path = cls.DEFAULT_FILE
        print("Loading JSON from:")
        print(cls.DEFAULT_FILE.resolve())

        if not path.exists():

            scenario = Scenario(
                name="Default Scenario"
            )

            cls.save(scenario)

            return scenario

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        except json.JSONDecodeError:
            print(
                "default.json is corrupted."
            )

            scenario = Scenario(
                name="Default Scenario"
            )

            cls.save(scenario)

            return scenario

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

        #
        # Read existing JSON so that
        # lane information is preserved.
        #
        if path.exists():

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        else:

            data = {}

        # Convert objects
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

        #
        # Update only scenario fields
        #
        data["name"] = scenario.name
        data["objects"] = objects

        #
        # Write back
        #
        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )

    @classmethod
    def load_lanes(cls):
        """
        Loads lane geometry from default.json.
        """

        path = cls.DEFAULT_FILE

        if not path.exists():
            return []

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)
        except (
            FileNotFoundError,
            json.JSONDecodeError,
        ):

            return []

        lane_data = data.get("lanes",[],)
        print("lane_data =", lane_data)
        print("lane count =", len(lane_data))

        print("lane_data =", lane_data)

        lanes = []

        for item in lane_data:

            lanes.append(
                Lane(
                    name=item["name"],
                    a=item["a"],
                    b=item["b"],
                    c=item["c"],
                    d1=item["d1"],
                    d2=item["d2"],
                    position=LanePosition(
                        item["position"]
                    ),
                )
            )

        print("Returning Lane objects:")

        for lane in lanes:
            print(lane)

        return lanes

    @classmethod
    def save_lanes(
        cls,
        lanes,
    ):
        """
        Saves lane geometry into default.json.
        """

        path = cls.DEFAULT_FILE

        path.parent.mkdir(
            exist_ok=True
        )

        #
        # Preserve existing scenario
        #
        if path.exists():

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        else:

            data = {}

        lane_list = []

        for lane in lanes:

            lane_list.append(
                {
                    "name": lane.name,
                    "a": lane.a,
                    "b": lane.b,
                    "c": lane.c,
                    "d1": lane.d1,
                    "d2": lane.d2,
                    "position": lane.position.value,
                }
            )

        data["lanes"] = lane_list

        with open(
            path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )