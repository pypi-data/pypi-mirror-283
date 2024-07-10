import os

from paij.functions import *
import config
from paij.functions import PAiJ


def main():
    base_dir = os.path.join(config.SRC_PATH, 'main', 'java', *config.WHOLE_PACKAGE_NAME.split('.'))
    test_dir = os.path.join(config.SRC_PATH, 'test', 'java', *config.WHOLE_PACKAGE_NAME.split('.'))

    project_name = config.PACKAGE_NAME
    input_filename = config.INPUT_FILENAME

    unit_tests = PAiJ.read_from_file(input_filename)
    method_code = generate_method_from_tests(config.OPENAI_API_KEY, unit_tests, language="Java")

    project_path = PAiJ.create_project_structure(base_dir, project_name)

    method_code_lines = method_code.split('\n')
    cleaned_method_code_lines = [line for line in method_code_lines if not line.startswith('package')]
    cleaned_method_code = '\n'.join(cleaned_method_code_lines)

    class_code = f"""
        package {config.WHOLE_PACKAGE_NAME}.{project_name};

        {cleaned_method_code}
        """

    PAiJ.write_to_file(
        os.path.join(project_path, f"{config.CLASS_NAME}.java"),
        class_code)
    print(f"Generated project structure with class files in {project_path}")

    if PAiJ.run_maven_commands(config.MAVEN_HOME, config.PROJECT_DIR, "TDDOrderServiceTest", max_retries=3):
        print("Maven build and tests were successful.")
    else:
        print("Maven build or tests failed.")


if __name__ == "__main__":
    main()
