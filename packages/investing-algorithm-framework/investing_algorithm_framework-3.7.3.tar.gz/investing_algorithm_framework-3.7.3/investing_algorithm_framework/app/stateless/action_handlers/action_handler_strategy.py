from abc import ABC, abstractmethod


class ActionHandlerStrategy(ABC):

    @abstractmethod
    def handle_event(self, payload, algorithm):
        pass
