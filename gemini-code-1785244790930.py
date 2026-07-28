# src/console/plugins/base.py
from abc import ABC, abstractmethod

class ConsolePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin displayed in the menu."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Short summary of what the plugin does."""
        pass

    @abstractmethod
    def execute(self, session, normalizer, graph) -> None:
        """Entrypoint for the plugin execution logic."""
        pass