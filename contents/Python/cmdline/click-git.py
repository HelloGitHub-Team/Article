import os
import click
from git.cmd import Git


git = Git(os.getcwd())


@click.group()
def cli():
    """
    git 命令行
    """
    pass


@cli.command()
def status():
    """
    处理 status 命令
    """
    cmd = ['git', 'status']
    output = git.execute(cmd)
    click.echo(output)


@cli.command()
@click.argument('pathspecs', nargs=-1, metavar='[PATHSPEC]...')
def add(pathspecs):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + list(pathspecs)
    output = git.execute(cmd)
    click.echo(output)


@cli.command()
@click.option('-m', 'msg')
def commit(msg):
    """
    处理 -m <msg> 命令
    """
    cmd = ['git', 'commit', '-m', msg]
    output = git.execute(cmd)
    click.echo(output)


@cli.command()
def push():
    """
    处理 push 命令
    """
    cmd = ['git', 'push']
    output = git.execute(cmd)
    click.echo(output)


if __name__ == '__main__':
    cli()
