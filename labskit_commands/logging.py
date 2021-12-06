import click

# TODO: insert file logging if needed in the future


class Logging:
    def __init__(self):
        pass

    @staticmethod
    def log(message, **kwargs):
        click.secho(message, **kwargs)

    @staticmethod
    def info(message):
        click.secho(f"INFO: {message}", fg='blue')

    @staticmethod
    def warn(message):
        click.secho(f"WARNING: {message}", fg='yellow')

    @staticmethod
    def error(message):
        click.secho(f"ERROR: {message}", fg='red')
