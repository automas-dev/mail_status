#!/usr/bin/env python3

import os
import socket
import sys

import apprise
import click


@click.command()
@click.argument('status', type=click.Choice(['alert', 'status']))
@click.argument('title', type=str)
@click.argument(
    'message',
    type=str,
    required=False,
)
@click.option(
    '-p', '--password', help='Gmail password, if this is empty read the password file'
)
@click.option(
    '--password-file',
    type=click.File(),
    help='File to read gmail password from, if this is empty read from GMAIL_PASSWORD environment variable',
)
def cli(status, title, message, password, password_file):
    if not password:
        if password_file:
            password = password_file.read()
        else:
            password = os.getenv('GMAIL_PASSWORD')

    if not password:
        print('Failed to read gmail password')
        exit(1)

    password = password.strip()

    if not message:
        message = sys.stdin.read()

    target = f'mailto://theharrisoncrafter+{status}:{password}@gmail.com'

    ap = apprise.Apprise()
    ap.add(target)

    ap.notify(
        title=f'[{status.upper()}] {socket.gethostname()} {title}',
        body=message,
    )


if __name__ == '__main__':
    cli()
