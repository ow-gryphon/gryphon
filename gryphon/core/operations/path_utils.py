from pathlib import Path


class PathUtils:

    @staticmethod
    def get_destination_path(folder=None) -> Path:
        """
        Function that helps to define the full path to a directory.

        It checks if the path is an absolute or relative path, then
        if relative, it appends the current folder to it, transforming
        it into an absolute path.
        """
        if folder is None:
            return Path.cwd()

        path_obj = Path(folder)

        if not path_obj.is_absolute():
            return path_obj.resolve()

        return path_obj

    @staticmethod
    def quote_windows_path(folder_path):
        return '"' + folder_path + '"'

    @staticmethod
    def escape_windows_path(folder_path):
        return fr'{folder_path}'
