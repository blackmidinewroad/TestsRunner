# Tests Runner for «Поколение Python» (Stepik)
This script is a test runner designed to automate testing of Python solutions for «Поколение Python» courses on Stepik. It executes a solution file against a set of test cases provided in a ZIP file, compares the output with expected results, and displays the test results.


## Installation
1. **Clone the Repository**:
   ```shell
   git clone https://github.com/blackmidinewroad/TestsRunner.git
   cd TestsRunner
   ```

2. **Install Dependencies**:
   ```shell
   pipenv install
   ```

3. **Set Up Environment Variables**

   Create a `.env` file in the project root with the following:
   ```env
   TESTS_ZIP_PATTERN='path/to/tests/*.zip'
   SOLUTION_PATH='path/to/solution.py'
   ```
   - Replace `path/to/tests/*.zip` with the actual glob pattern (e.g., `C:/Users/JohnDoe/Downloads/*.zip`).
   - Replace `path/to/solution.py` with the actual path to your solution file (e.g., `C:/Users/JohnDoe/Documents/solution.py`).


## Usage
1. Download test ZIP file from Stepik using `Архив с тестами` link and put it in the directory specified by `TESTS_ZIP_PATTERN`.

2. Run the script from within the `pipenv` virtual environment:
   ```shell
   python run_tests.py
   ```

3. The script will:
   - Find the latest ZIP file matching the `TESTS_FOLDER_PATH` glob pattern.
   - Extract test cases and expected outputs.
   - Run your solution against each test.
   - Display results with pass/fail status, runtime, and detailed output for failed tests.


## Example Output
```
Test 1 completed! ✅
Runtime: 0.0322
---------------------------------------------------------------------
Test 2 failed! ❌
Input:
print(2 + 2)
Output:
4
Expected:
5
---------------------------------------------------------------------
Tests passed: 1/2
---------------------------------------------------------------------
```