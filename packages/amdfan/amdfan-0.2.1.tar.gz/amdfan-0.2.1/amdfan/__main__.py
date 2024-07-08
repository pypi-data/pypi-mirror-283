#!/usr/bin/env python
""" entry point for amdfan """
# __main__.py
import click

from .commands import cli, monitor_cards, run_daemon, set_fan_speed


@click.group()
def main():
    pass


main.add_command(cli)
main.add_command(run_daemon)
main.add_command(monitor_cards)
main.add_command(set_fan_speed)

if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
