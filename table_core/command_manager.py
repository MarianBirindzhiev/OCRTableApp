class GridCommandManager:
    """
    A class to manage commands in the application.
    It handles the execution and undoing of commands.
    """

    def __init__(self):
        # Stack to keep track of executed commands for undo
        self.undo_stack = []
        # Stack to keep track of undone commands for redo
        self.redo_stack = []

    def execute(self, command):
        # Execute the command and store it in the undo stack
        command.execute()
        self.undo_stack.append(command)
        # Clear the redo stack since new action invalidates redo history
        self.redo_stack.clear()

    def undo(self):
        # If nothing to undo, return early
        if not self.undo_stack:
            return
        # Pop the last executed command and undo it
        command = self.undo_stack.pop()
        command.undo()
        # Store the undone command in the redo stack
        self.redo_stack.append(command)

    def redo(self):
        # If nothing to redo, return early
        if not self.redo_stack:
            return
        # Pop the last undone command and re-execute it
        command = self.redo_stack.pop()
        command.execute()
        # Push it back to the undo stack
        self.undo_stack.append(command)
