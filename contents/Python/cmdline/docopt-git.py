"""
Git 命令行

前置条件:
    1. pip install gitpython
    2. 安装了 git

Usage:
    git status
    git add [<pathspec>...]
    git commit -m msg
    git push

Options:
  -h --help         Show help.
  -m --message msg  Commit with message.

"""
import os
from docopt import docopt
from git.cmd import Git


def cli():
    """
    git 命名程序入口
    """
    args = docopt(__doc__)
    git = Git(os.getcwd())

    if args['status']:
        handle_status(git)
    elif args['add']:
        handle_add(git, args['<pathspec>'])
    elif args['commit']:
        handle_commit(git, args['--message'])
    elif args['push']:
        handle_push(git)
    else:
        print(__doc__)


def handle_status(git):
    """
    处理 status 命令
    """
    cmd = ['git', 'status']
    output = git.execute(cmd)
    print(output)


def handle_add(git, pathspec):
    """
    处理 add 命令
    """
    cmd = ['git', 'add'] + pathspec
    output = git.execute(cmd)
    print(output)


def handle_commit(git, msg):
    """
    处理 -m <msg> 命令
    """
    cmd = ['git', 'commit', '-m', msg]
    output = git.execute(cmd)
    print(output)


def handle_push(git):
    """
    处理 push 命令
    """
    cmd = ['git', 'push']
    output = git.execute(cmd)
    print(output)


if __name__ == '__main__':
    cli()
