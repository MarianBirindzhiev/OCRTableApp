from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        """Execute the action."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def undo(self):
        """Undo the action, reverting state to before execute()."""
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod    
    def redo(self):
        """Redo the action, re-executing the command."""
        raise NotImplementedError("Subclasses should implement this method")
