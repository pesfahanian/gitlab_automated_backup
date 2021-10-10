from backup import CodebaseBackUpHandler

from configuration import read_codebase_configuration

JSON_FILE_PATH = 'configuration.json'


def main() -> None:
    codebase_configuration = read_codebase_configuration(
        json_file_path=JSON_FILE_PATH)
    codebase_backup_handler = CodebaseBackUpHandler(
        codebase_configuration=codebase_configuration)
    codebase_backup_handler.run()


if __name__ == '__main__':
    main()
