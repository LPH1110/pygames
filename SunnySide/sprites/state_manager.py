class StateManager:
    def __init__(self, entity):
        self.entity = entity
        self.states = {}
        self.current_state = None

    def add_state(self, name, state):
        """Registers a state with a given name."""
        self.states[name] = state

    def set_initial_state(self, name):
        """Sets the starting state."""
        if name in self.states:
            self.current_state = self.states[name]
            self.current_state.enter()

    def change_state(self, new_state_name):
        """Transitions to a new state if it exists and is different from current."""
        new_state = self.states.get(new_state_name)
        if new_state and new_state != self.current_state:
            if self.current_state:
                self.current_state.exit()
            self.current_state = new_state
            self.current_state.enter()

    def update(self):
        """Delegates update and input handling to the current state."""
        if self.current_state:
            self.current_state.handle_input()
            self.current_state.update()
