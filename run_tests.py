import glob
import os
import subprocess
import sys
import time
from zipfile import ZipFile

from dotenv import load_dotenv


load_dotenv()

RESET, GREEN, RED, CYAN, YELLOW, BLUE = '\033[0m', '\033[32m', '\033[31m', '\033[36m', '\033[0;33m', '\033[0;34m'
try:
    TERMINAL_SIZE = os.get_terminal_size().columns
except:
    TERMINAL_SIZE = 70 - 1


TESTS_ZIP_PATTERN = os.getenv('TESTS_ZIP_PATTERN')
SOLUTION_PATH = os.getenv('SOLUTION_PATH')

if TESTS_ZIP_PATTERN is None or SOLUTION_PATH is None:
    print(f"{RED}Couldn't find {CYAN}'TESTS_ZIP_PATTERN'{RED} or {CYAN}'SOLUTION_PATH'{RED} in environment variables.{RESET}")
    sys.exit()


def get_latest_zip(path: str) -> str:
    '''Get path of the latest added zip file in folder.'''

    list_of_files = glob.glob(path)
    if not list_of_files:
        print(f"{RED}Couldn't find zip file with tests, path: {CYAN}'{path}'{RED}.{RESET}")
        sys.exit()
    return max(list_of_files, key=os.path.getctime)


def get_tests(zip_file_path: str) -> dict[str, str]:
    '''Get tests from zip. Keys in dict are test code and value is expected output.'''

    if not os.path.exists(zip_file_path):
        print(f"{RED}Tests zip file {CYAN}'{zip_file_path}'{RED} does not exist.{RESET}")
        sys.exit()

    tests = {}
    with ZipFile(zip_file_path) as zip:
        len_tests = len(zip.namelist()) // 2
        for i in range(1, len_tests + 1):
            with zip.open(f'{i}') as test_file, zip.open(f'{i}.clue') as answer_file:
                tests[test_file.read().decode('utf-8')] = answer_file.read().decode('utf-8')
    return tests


def get_solution_code(file_path: str) -> str:
    '''Get solution code from file.'''

    if not os.path.exists(file_path):
        print(f"{RED}Solution file {CYAN}'{file_path}'{RED} does not exist.{RESET}")
        sys.exit()

    with open(file_path, encoding='utf-8') as code_file:
        code = code_file.read()
        return code


def is_code_test(code: str, test: str, func_class: str) -> bool:
    '''Determine if test is code (not test with input).
    Find function/class names in solution code, if one of the names is used in test then this test is code.
    '''

    n_keywords = code.count(func_class)
    if not n_keywords:
        return False

    f_c_specific = {'offset': 4 if func_class == 'def' else 6, 'end_char': '(' if func_class == 'def' else ':'}
    f_c_names = []
    for _ in range(n_keywords):
        start = code.find(func_class) + f_c_specific['offset']
        end = code.find(f_c_specific['end_char'], start)
        f_c_names.append(code[start:end])
        code = code.replace(func_class, '', 1)

    for f_c_name in f_c_names:
        if func_class == 'class' and '(' in f_c_name:
            f_c_name = f_c_name[: f_c_name.find('(')]
        if f_c_name in test or f'@{f_c_name}' in test:
            return True

    return False


def run_tests(solution_code: str, tests: dict[str, str], is_code: bool) -> None:
    '''Run each test, compare output with expected output, display results.'''

    tests_passed = 0
    total_tests = len(tests)

    for i, (test, corr_out) in enumerate(tests.items(), 1):
        complete_code = solution_code + '\n\n' + test if is_code else solution_code
        inp = None if is_code else test

        start_time = time.perf_counter()
        result = subprocess.run(
            ['py', '-c', complete_code],
            input=inp,
            text=True,
            capture_output=True,
            encoding='utf-8',
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
        )
        end_time = time.perf_counter()
        run_time = round(end_time - start_time, 5)

        out = result.stdout.rstrip('\n') if result.returncode == 0 else result.stderr.rstrip('\n')

        if out == corr_out:
            tests_passed += 1
            print(f'{GREEN}Test {i} completed! ✅\nRuntime: {YELLOW}{run_time}\n{RESET}{'-' * TERMINAL_SIZE}')
        else:
            print(f'{RED}Test {i} faild! ❌\nInput:\n{CYAN}{test}')
            print(f'{RED}Output:\n{BLUE}{out}\n{RED}Expected:\n{BLUE}{corr_out}\n{RESET}{'-' * TERMINAL_SIZE}')

    if tests_passed == total_tests:
        result_color = GREEN
    elif tests_passed == 0:
        result_color = RED
    else:
        result_color = YELLOW

    print(f'{result_color}Tests passed: {tests_passed}/{total_tests}\n{RESET}{'-' * TERMINAL_SIZE}')


def main():
    tests_zip_file_path = get_latest_zip(TESTS_ZIP_PATTERN)
    tests = get_tests(tests_zip_file_path)
    solution_code = get_solution_code(SOLUTION_PATH)
    run_tests(
        solution_code,
        tests,
        is_code_test(solution_code, next(iter(tests.keys())), 'def') or is_code_test(solution_code, next(iter(tests.keys())), 'class'),
    )


if __name__ == '__main__':
    main()
