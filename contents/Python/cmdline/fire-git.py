import os
import fire
from git.cmd import Git


git = Git(os.getcwd())


class GitCli:
    def status(self):
        """
        处理 status 命令
        """
        cmd = ['git', 'status']
        output = git.execute(cmd)
        return output

    def add(self, *pathspecs):
        """
        处理 add 命令
        """
        cmd = ['git', 'add'] + list(pathspecs)
        output = git.execute(cmd)
        return output

    def commit(self, m):
        """
        处理 -m <msg> 命令
        """
        cmd = ['git', 'commit', '-m', m]
        output = git.execute(cmd)
        return output

    def push(self):
        """
        处理 push 命令
        """
        cmd = ['git', 'push']
        output = git.execute(cmd)
        return output


if __name__ == '__main__':
    fire.Fire(GitCli())
