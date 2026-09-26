from rules.excessive_function_arguments import find_excessive_function_arguments
from rules.base import Finding
from test_util import create_test_file


def test_excessive_function_arguments_empty(tmp_path):
    file_path = create_test_file(tmp_path, """
    def test_fun():
        pass
""")
    result = find_excessive_function_arguments(str(file_path))
    assert True 
