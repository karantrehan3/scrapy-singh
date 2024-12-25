from typing import Any


class Notifier:
    @staticmethod
    def notify(message: Any) -> None:
        """
        Print a notification message.
        """

        print(message)
