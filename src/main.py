#!/usr/bin/python3

import os
import subprocess
import pathlib

class Menu():
    def __init__(self,cmd:str="bemenu", args:list[str]=[]):
        self._cmd:str = cmd
        self._args:list[str] = args
    def run(self, prompt:str, items:list[str]=[],new_args:list[str]=[]) -> str:
        out = subprocess.run(
            [self._cmd] + self._args + new_args,
            input="\n".join(items).encode("utf-8"),
            stdout=subprocess.PIPE
        )
        if out.returncode is not None:
            print(out.stderr)
        if out.stdout.decode("utf-8") is not None:
            return out.stdout.decode("utf-8")


if __name__ == '__main__':
    menu = Menu(
        cmd="bemenu",
        args=['--scrollbar',
            'autohide',
            '-p',
            '"❯',
            '"',
            '-P',
            '"\uf105',
            '"',
            '-n',
            '-l',
            '10',
            '-c',
            '-B',
            '1',
            '-R',
            '0',
            '-M',
            '500',
            '--fn',
            '"Roboto',
            '16"',
            '--tb',
            '\\#0000007F',
            '--tf',
            '\\#ffffff7f',
            '--fb',
            '\\#0000007f',
            '--ff',
            '\\#ffffff7f',
            '--cb',
            '\\#0000007f',
            '--cf',
            '\\#ffffff7f',
            '--nb',
            '\\#0000007f',
            '--nf',
            '\\#ffffff7f',
            '--hb',
            '\\#0000007f',
            '--hf',
            '\\#ffffff7f',
            '--sb',
            '\\#0000007f',
            '--sf',
            '\\#ffffff7f',
            '--ab',
            '\\#0000007f',
            '--af',
            '\\#ffffff7f',
            '--scb',
            '\\#0000007f',
            '--scf',
            '\\#ffffff7f',
            '--fbb',
            '\\#0000007f',
            '--fbf',
            '\\#ffffff7f',
            '--bdr',
            '\\#ffffff7f']
    )
    envPath = os.environ['PATH'].split(":")
    binfiles = []
    for path in envPath:
        path = pathlib.Path(path)
    print(menu.run("fuck!",envPath))