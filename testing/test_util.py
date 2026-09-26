def create_test_file(tmp_path, code):
    """Creates the basic setup for all tests, creating the file and writing the code to it
    
    Params:
        code (str): the code used in the test
    Returns:
        Path: the new file path
    """
    file = tmp_path / "sample.py"
    file.write_text(code)
    return file 