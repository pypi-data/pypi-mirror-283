import click
from . import api


@click.group
def main_group():
    pass


main_group.add_command(api.save_token)
main_group.add_command(api.call_api)


if __name__ == "__main__":
    main_group()
