"""
provides string_to_nim utilities
"""
from . import core
from . import utils
from . import c_like_utils


_get_function_name = utils.get_function_name_fun("fun")


def atom_to_code(in_atom):
    """
    returns a string/piece of nim code resulting in printing the
    in_atom.atom_char to the standard output
    """
    assert isinstance(in_atom, core.Atom)
    return f"stdout.write '{c_like_utils.escape_special_char(in_atom)}'"


def function_call_str(in_function_id, **kwargs):
    """
    returns a string calling a function with name in_function_name in nim
    """
    function_name = _get_function_name(in_function_id, **kwargs)
    return f"{function_name}()"


_call_function_or_atom = utils.get_call_function_or_atom(
    atom_to_code, function_call_str
)


_EMPTY_BODY = "  discard"

_body_to_str = utils.get_body_to_str(
    "\n", "  ", _call_function_or_atom, "", _EMPTY_BODY
)


def _merge_to_full_function(in_function_name, in_function_body):
    function_type = "func" if in_function_body == _EMPTY_BODY else "proc"
    return "\n".join([f"{function_type} {in_function_name}() =", in_function_body])


_function_to_code = utils.get_function_to_code(
    _get_function_name, _body_to_str, _merge_to_full_function
)


def _main_call_to_code(in_initial_call, **kwargs):
    return (
        _call_function_or_atom(in_initial_call, **kwargs) + "\n"
        if in_initial_call is not None
        else ""
    )


def _join_to_final(main_call, function_definitions, **_kwargs):
    res = "\n\n\n".join(function_definitions + [main_call])
    return res


proc_printer_program, proc = utils.get_all_proc_functions(
    _main_call_to_code, _function_to_code, _join_to_final
)
