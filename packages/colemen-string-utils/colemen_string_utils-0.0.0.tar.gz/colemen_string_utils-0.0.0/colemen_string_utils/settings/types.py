from typing import TYPE_CHECKING,TypeVar as _TypeVar


# ---------------------------------------------------------------------------- #
#                               TYPE DECLARATIONS                              #
# ---------------------------------------------------------------------------- #

_main_type = None

_inflect_engine_type = None
'''The inflect engine instance type'''

if TYPE_CHECKING:

    from colemen_string_utils.ColemenStringUtils import ColemenStringUtils as _m
    _main_type = _TypeVar('_main_type', bound=_m)



    import inflect as _inflect
    _inflect_engine_type = _TypeVar('_inflect_engine_type', bound=_inflect.engine)

