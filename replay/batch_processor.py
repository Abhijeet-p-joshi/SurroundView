from replay.object_buffer import ObjectBuffer
from config.replay_config import (
    UPDATES_PER_BATCH,
    OBJECTS_PER_BATCH,
    OBJECTS_PER_UPDATE
)


class BatchProcessor:
    """
    Reconstructs one complete replay batch.

    Protocol:

    - UpdateBit rising edge -> Start Batch
    - Every 5 ms -> Receive 3 objects
    - After 6 updates -> 18 objects complete
    - Wait until UpdateBit goes LOW
    """

    def __init__(self):

        self.buffer = ObjectBuffer()

        self.previous_update_bit = False

        self.collecting = False

        self.slot_index = 0

    def process(self, update_bit, objects):
        """
        Processes one CANoe update.

        Parameters
        ----------
        update_bit : bool
            Current value of Update Bit.

        objects : list[DetectedObject]
            Three detected objects received in this update.

        Returns
        -------
        list | None
            Returns a complete batch (18 objects)
            when all six updates have been received.
        """

        # ----------------------------------------
        # Rising Edge -> Start of new batch
        # ----------------------------------------

        if update_bit and not self.previous_update_bit:

            self.buffer.clear()

            self.collecting = True

            self.slot_index = 0

            print("========== New Batch ==========")

        # ----------------------------------------
        # Collect one slot
        # ----------------------------------------

        if self.collecting and update_bit:

            self.buffer.add_objects(objects)
            self.slot_index += 1

            print(
                f"Slot {self.slot_index}/{UPDATES_PER_BATCH} "
                f"received ({self.buffer.object_count()} objects)"
            )

            if self.slot_index == UPDATES_PER_BATCH:

                completed_batch = self.buffer.get_objects()

                self.collecting = False

                print("Batch Complete")

                self.previous_update_bit = update_bit

                return completed_batch

        # ----------------------------------------
        # Falling Edge
        # ----------------------------------------

        if (not update_bit) and self.previous_update_bit:

            print("Waiting for next batch...")

            self.collecting = False

            self.slot_index = 0

        self.previous_update_bit = update_bit

        return None

    def reset(self):
        """
        Resets the processor to its initial state.
        """

        self.buffer.clear()

        self.collecting = False

        self.slot_index = 0

        self.previous_update_bit = False

    def current_update(self):
        """
        Returns the current replay update index (0..5).
        """

        return self.slot_index