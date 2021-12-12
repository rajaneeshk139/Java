"""
tests of the string_to_code module
"""

import unittest
import subprocess

import general_utilities as gu
import string_to_code_module.string_to_code as stc


def get_cpp_compiler():
    """returns the name of the c++ compiler"""
    return 'g++'


def compile_cpp_code(in_code):
    """
    Compiles the C++ in_code and returns the filename of the output.
    The output file is located in gu.get_tmp_test_folder_path()
    """
    source_filename = gu.get_unique_filename('cpp')
    executable_filename = gu.get_unique_filename('o')
    gu.save_str_to_file(
        gu.get_tmp_test_folder_path()/source_filename, in_code)
    subprocess.run(
        [get_cpp_compiler(), source_filename,
         '-Werror', '-Wpedantic', '-Wall', '-Wextra',
         '-o', executable_filename],
        cwd=str(gu.get_tmp_test_folder_path()),
        check=True)
    return executable_filename


def run_executable(in_executable_name):
    """
    runs the executable in_executable_name
    in the folder gu.get_tmp_test_folder_path()
    """
    assert (gu.get_tmp_test_folder_path()/in_executable_name).is_file()
    return subprocess.run(
        ['./'+in_executable_name],
        cwd=str(gu.get_tmp_test_folder_path()),
        check=True,
        capture_output=True,
        text=True)


def run_cpp_code(in_code):
    """
    Compiles and executes the C++ code in_code.
    Returns the output of the program.
    """
    return run_executable(compile_cpp_code(in_code))


def check_output(test_obj, in_ex_output, in_target_str):
    """
    does all of the checks of the program output against the expected result
    """
    test_obj.assertEqual(in_ex_output.stdout, in_target_str)
    test_obj.assertEqual(in_ex_output.stderr, '')


class TestSetup(unittest.TestCase):
    """
    tests verifying if the setup of the system is suitable
    to perform other tests
    """
    def test_compiler(self):
        subprocess.run(
            [get_cpp_compiler(), '--version'],
            check=True,
            capture_output=True)


class TestStingToCodeCpp(unittest.TestCase):
    """
    unit tests for the function str_to_cpp
    """

    def setUp(self):
        gu.create_tmp_test_folder()

    def tearDown(self):
        gu.delete_tmp_test_folder()

    def test_str_to_cpp(self):
        """
        basic test of the function str_to_cpp
        """
        def proc_single(in_str):
            source_code = stc.str_to_cpp(in_str)
            executable_output = run_cpp_code(source_code)
            check_output(self, executable_output, in_str)
        gu.check_all(proc_single)

    def test_str_to_cpp_iteration(self):
        """
        tests the iterations of the function str_to_cpp
        """
        def proc_single(in_str):
            string_list = [in_str]
            max_iteration = 2
            for _ in range(max_iteration):
                string_list.append(stc.str_to_cpp(string_list[-1]))

            for _ in range(max_iteration, 0, -1):
                check_output(
                    self, run_cpp_code(string_list[_]), string_list[_-1])
        gu.check_all(proc_single)


if __name__ == '__main__':
    unittest.main()
