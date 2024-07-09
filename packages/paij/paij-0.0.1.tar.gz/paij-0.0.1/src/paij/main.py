from src.paij import run_maven_commands
import config


def main():
    base_dir = os.path.join(config.SRC_PATH, 'main', 'java', *config.PACKAGE_NAME.split('.'))
    test_dir = os.path.join(config.SRC_PATH, 'test', 'java', *config.PACKAGE_NAME.split('.'))

    project_name = config.PROJECT_NAME
    input_filename = config.INPUT_FILENAME

    unit_tests = read_from_file(input_filename)
    method_code = generate_method_from_tests(config.OPENAI_API_KEY, unit_tests, language="Java")

    project_path = create_project_structure(base_dir, project_name)
    test_path = create_project_structure(test_dir, project_name)

    import_package, real_codes = process_unit_tests(unit_tests)

    method_code_lines = method_code.split('\n')
    cleaned_method_code_lines = [line for line in method_code_lines if not line.startswith('package')]
    cleaned_method_code = '\n'.join(cleaned_method_code_lines)

    class_code = f"""
    package {config.PACKAGE_NAME}.{project_name};

    {import_package}


    {cleaned_method_code}
    """

    test_code = f"""
    package {config.PACKAGE_NAME}.{project_name};

    {unit_tests}
    {'}'}
    """

    write_to_file(
        os.path.join(project_path, f"{config.CLASS_NAME}.java"),
        class_code)
    print(f"Generated project structure with class files in {project_path}")

    write_to_file(
        os.path.join(test_path, f"{config.TEST_CLASS_NAME}.java"),
        test_code)
    print(f"Generated project structure with test files in {test_path}")

    if run_maven_commands(config.MAVEN_HOME, config.PROJECT_DIR):
        print("Maven build and tests were successful.")
    else:
        print("Maven build or tests failed.")


if __name__ == "__main__":
    main()
