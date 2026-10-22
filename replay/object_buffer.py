from config.replay_config import OBJECTS_PER_BATCH

class ObjectBuffer:
    """
    Stores one complete replay batch.

    The replay protocol delivers 3 objects every 5 ms.

    Six updates make one complete batch.

    Therefore this class stores 18 objects before they
    are passed to the visualization.
    """

    def __init__(self):

        self.clear()

    def clear(self):

        self.objects = []

    def add_objects(self, objects):

        """
        Adds one update (3 objects).
        """

        self.objects.extend(objects)

    def is_complete(self):

        return len(self.objects) >= OBJECTS_PER_BATCH

    def get_objects(self):

        return list(self.objects)

    def object_count(self):

        return len(self.objects)