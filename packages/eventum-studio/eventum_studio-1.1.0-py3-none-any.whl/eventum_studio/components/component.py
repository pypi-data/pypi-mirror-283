
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any, MutableMapping, Optional

import streamlit as st

from eventum_studio.widget_management import (EPHEMERAL_PREFIX,
                                              ContextualSessionState,
                                              WidgetKeysContext)


def persist_state():
    """Persist state after changing displaying page."""
    for k, v in st.session_state.items():
        if k.startswith(EPHEMERAL_PREFIX):
            del st.session_state[k]
        else:
            st.session_state[k] = v


class ComponentPropsError(Exception):
    """Exception indicating that the properties passed to the component
    do not correspond to the expected set of elements.
    """


class ComponentActionError(Exception):
    """Exception for indicating that action performed on component is
    incorrect.
    """


class BaseComponent(ABC):
    """Base class for creating session isolated components."""
    _STATE_INITIALIZATION_PROPS: dict[str, Any] = {}
    _SHOW_PROPS: dict[str, Any] = {}

    def __init__(
        self,
        session_state: MutableMapping = st.session_state,
        id: int = 1,
        widget_keys_context: Optional[WidgetKeysContext] = None,
        props: Optional[dict] = None
    ) -> None:
        self._wk = (
            deepcopy(widget_keys_context)
            if widget_keys_context else WidgetKeysContext()
        )
        self._props = props or dict()

        self._wk.register_component(self.__class__.__name__, id)
        self._session_state = ContextualSessionState(session_state, self._wk)

        self.__init_state_wrapper()

    def __init_state_wrapper(self) -> None:
        """Check whether the session is initialized and call
        initialization in case it's not.
        """
        if 'initialized' in self._session_state:
            return

        expected_keys = self._STATE_INITIALIZATION_PROPS.keys()
        provided_keys = self._props.keys()
        if not set(expected_keys).issubset(provided_keys):
            raise ComponentPropsError(
                f'Expected {list(expected_keys)} props to init component '
                f'session but provided props are {list(provided_keys)}'
            )

        self._init_state()
        self._session_state['initialized'] = True

    def _init_state(self) -> None:
        """Perform state initialization."""
        ...

    def release_state(self) -> None:
        """Delete items from session state added on initialization or used
        as widget keys in `_show` method."""
        self._session_state.delete_context_elements()

    def show(self) -> None:
        """Present component structure."""
        expected_keys = self._SHOW_PROPS.keys()
        provided_keys = self._props.keys()
        if not set(expected_keys).issubset(provided_keys):
            raise ComponentPropsError(
                f'Expected {list(expected_keys)} props to show component '
                f'but provided props are {list(provided_keys)}'
            )

        self._show()

    @abstractmethod
    def _show(self) -> None:
        """Present component structure."""
        ...
