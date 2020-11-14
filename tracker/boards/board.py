from abc import ABC


class Board(ABC):
    def __init__(self, state, root_render_method):
        self.state = state
        self._register_paths()

        # Should be used when render needs to happen immediately, e.g. on button click
        self._trigger_render = root_render_method

        self._frame = None

    @property
    def is_needs_render(self):
        """
        Whenever this property is accessed and returns True, a render should be triggered
        before the next time it is accessed.
        """
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def render(self, parent):
        """
        All _render methods should return the rendered frame.
        The parent board should then be responsible for slotting the returned frame into its parent element.
        """
        raise NotImplementedError

    def _register_paths(self):
        """
        Any keys registered in subclasses should be prefixed with the class name
        in the format: "class__key_string"
        """
        pass

    def _increment_class_var(self, var_name, increment_amount, max_value=None, min_value=None):
        new_value = getattr(self, var_name) + increment_amount

        if max_value is not None:
            new_value = min(max_value, new_value)
        if min_value is not None:
            new_value = max(min_value, new_value)

        setattr(self, var_name, new_value)

        self._trigger_render()

