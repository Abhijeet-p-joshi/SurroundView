class PreviewCANoeInterface:
    """
    Fake CANoe interface.

    Used when running without CANoe hardware.
    """

    def __init__(self):

        print("Preview CANoe Interface")

    # --------------------------------------------------

    def connect(self):

        return True

    # --------------------------------------------------

    def disconnect(self):

        pass

    # --------------------------------------------------

    def write_signal(
        self,
        signal_name,
        value,
    ):

        print(
            f"[Preview] {signal_name} = {value}"
        )

    # --------------------------------------------------

    def read_signal(
        self,
        signal_name,
    ):

        return 0