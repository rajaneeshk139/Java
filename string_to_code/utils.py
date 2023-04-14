"""
utilities for to_some_language modules
"""

from . import core


def get_function_name_fun(in_prefix="fun_"):
    """returns a function returing a function name based on id"""

    def _get_function_name(in_function_id, **kwargs):
        return kwargs.get(
            "function_id_to_name", core.get_function_namer(in_prefix)
        )(in_function_id)

    return _get_function_name


def get_call_function_or_atom(in_atom_to_code, in_function_call_str):
    """
    returns the function call_function_or_atom returning a string
    representing a function call or displayng given atom
    """

    def _inner(in_data, **kwargs):
        if isinstance(in_data, core.Atom):
            return in_atom_to_code(in_data)
        assert isinstance(in_data, int)
        return in_function_call_str(in_data, **kwargs)

    return _inner


def get_proc_printer_program_function(
    main_call_to_code, function_to_code, join_to_final
):
    """returns the proc_printer_program function"""

    def _inner(in_printer_program, **kwargs):
        main_call = main_call_to_code(in_printer_program.initial_call, **kwargs)
        function_definitions = (
            in_printer_program.needed_function_definitions_str_list(
                function_to_code, **kwargs
            )
        )
        return join_to_final(main_call, function_definitions, **kwargs)

    return _inner


def get_proc_function(main_call_to_code, function_to_code, join_to_final):
    """returns the proc function"""

    def _inner(in_str, **kwargs):
        printer_program = core.get_printer_program(in_str)
        return get_proc_printer_program_function(
            main_call_to_code, function_to_code, join_to_final
        )(printer_program, **kwargs)

    return _inner


def get_all_proc_functions(main_call_to_code, function_to_code, join_to_final):
    """returns proc and proc_printer_program functions"""
    return get_proc_printer_program_function(
        main_call_to_code, function_to_code, join_to_final
    ), get_proc_function(main_call_to_code, function_to_code, join_to_final)