"""
defines a base class for all string_to_code type tests
"""
import unittest
import general_utilities as gu


def check_output(test_obj, in_ex_output, in_target_str):
    """
    does all of the checks of the program output against the expected result
    """
    test_obj.assertEqual(in_ex_output.stdout, in_target_str)
    test_obj.assertEqual(in_ex_output.stderr, '')


class BaseStringToCode(unittest.TestCase):
    __test__ = False

    def setUp(self):
        gu.create_tmp_test_folder()

    def tearDown(self):
        gu.delete_tmp_test_folder()

    def test_string_to_code(self):
        """
        basic test of the string_to_code type function
        """
        def proc_single(in_str):
            str_to_code_fun = self.str_to_code
            source_code = str_to_code_fun(in_str)
            run_code_fun = self.run_code
            executable_output = run_code_fun(source_code)
            check_output(self, executable_output, in_str)
        gu.check_all(proc_single)

    def test_string_to_code_iteration(self):
        """
        tests the iterations of the string_to_code function
        """
        def proc_single(in_str):
            string_list = [in_str]
            max_iteration = 2
            for _ in range(max_iteration):
                str_to_code_fun = self.str_to_code
                string_list.append(str_to_code_fun(string_list[-1]))

            for _ in range(max_iteration, 0, -1):
                run_code_fun = self.run_code
                check_output(
                    self, run_code_fun(string_list[_]), string_list[_-1])
        gu.check_all(proc_single)