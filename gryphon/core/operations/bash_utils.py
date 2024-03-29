import errno
import logging
import os
import shutil
import stat
import subprocess
from pathlib import Path

logger = logging.getLogger('gryphon')


def on_error(func, path, exc):
    value = exc[1]  # os.rmdir
    if func in (os.unlink, os.remove) and value.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        try:
            func(path)
        except PermissionError:
            logger.error(f"Permission error on {path}. Something might go wrong.")
    else:
        if func == os.rmdir:
            shutil.rmtree(path)
            return
        raise RuntimeError("File permission error.")


class BashUtils:

    @staticmethod
    def remove_folder(folder: Path):
        """
        Removes a folder (location relative to cwd or absolute).
        """
        shutil.rmtree(folder, ignore_errors=False, onerror=on_error)

    @staticmethod
    def create_folder(folder: Path):
        """
        Create a folder in the given path (location relative to cwd or absolute).
        """
        folder.mkdir(exist_ok=True)

    @staticmethod
    def copy_project_template(template_source: Path, template_destiny: Path):
        """Copies the templates to destination folder."""

        template_path = template_source / "template"
        template_destiny.mkdir(exist_ok=True)

        shutil.copytree(
            src=template_path,
            dst=rf'{str(template_destiny)}',
            dirs_exist_ok=True
        )

    @staticmethod
    def execute_and_log(command, use_subprocess=False) -> tuple:
        logger.debug(f"command: {command}")
        
        if use_subprocess:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Read the output and error streams in real-time
            full_output = []
            
            check_output = True
            while check_output:
                output = cmd.stdout.readline()
                error = cmd.stderr.readline()
                if output == b'' and error == b'' and cmd.poll() is not None:
                    break
                if output:
                    if output.decode('utf-8').strip() == "":
                        check_output = False
                    full_output.append(output.decode('utf-8').strip())
                if error:
                    full_output.append(error.decode('utf-8').strip())
                
            status_code = cmd.returncode
            if status_code == 0:
                status_code = None
            # status code
            return status_code, ", ".join(full_output)
        
        else:
            
            cmd = os.popen(command)
            output = cmd.read()
            for line in output.split('\n'):
                if len(line):
                    logger.debug(line)

            # status code
            return cmd.close(), output
