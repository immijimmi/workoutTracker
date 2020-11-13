from abc import ABC


class Board(ABC):
    def __init__(self, state, root_render_method):
        self.state = state
        # Should be used when render needs to happen immediately, e.g. on button click
        self._trigger_render = root_render_method

        self._frame = None

    @property
    def is_needs_render(self):
        """
        Whenever this property returns True, continue under the assumption that
        the render will then be carried out as a result.
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
