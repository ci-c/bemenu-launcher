#!/usr/bin/python3

import os
import subprocess
import pathlib
from xdg.DesktopEntry import DesktopEntry
import sqlite3
import datetime

class Menu():
    def __init__(self,cmd:str="bemenu", args:list[str]=[]):
        self._cmd:str = cmd
        self._args:list[str] = args
    def run(self, prompt:str, items:list[str]=[],new_args:list[str]=[]) -> str | None:
        out = subprocess.run(
            [self._cmd] + self._args + new_args + ["-p", prompt],
            input="\n".join(items).encode("utf-8"),
            stdout=subprocess.PIPE
        )
        if not (out.returncode == 0 or out.returncode == 1) or out.stderr is not None:
            print(f"code: {out.returncode}\nerr: {out.stderr}")
        if out.stdout.decode("utf-8") is not None:
            return out.stdout.decode("utf-8")
        if out.returncode == 1:
            return None

class DB:
    def __init__(self, path:pathlib.Path | str):
        if isinstance(path,str):
            path = pathlib.Path(path)
        self._db_path = path
        self._create_table()

    def _create_table(self):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS jornal
                     (datetime TEXT PRIMARY KEY,
                     name TEXT)''')
        conn.commit()
        conn.close()

    def registre(self, name:str):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        date_time = datetime.datetime.now().isoformat()
        cur.execute("INSERT INTO jornal (datetime, name) VALUES (?, ?)", (date_time, name))
        conn.commit()
        conn.close()

    def _get_all(self):
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM jornal")
        rows = cur.fetchall()
        conn.close()
        return rows
    
    def get_rating_table(self):
        a = 0.5
        table = {}
        for row in self._get_all():
            dt = datetime.datetime.fromisoformat(row[0]).timestamp()
            name = row[1]
            if name not in table:
                table[name] = 1
            else:
                table[name] = (a * dt) + ((1 - a) * table[name])
        return table

if __name__ == '__main__':
    menu = Menu(
        cmd="bemenu",
        args=['--scrollbar',
            'autohide',
            '-P',
            '\uf105',
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
            'Roboto 16',
            '--tb',
            '#000000',
            '--tf',
            '#ffffff',
            '--fb',
            '#000000',
            '--ff',
            '#ffffff',
            '--cb',
            '#000000',
            '--cf',
            '#ffffff',
            '--nb',
            '#000000',
            '--nf',
            '#ffffff',
            '--hb',
            '#000000',
            '--hf',
            '#ffffff',
            '--sb',
            '#000000',
            '--sf',
            '#ffffff',
            '--ab',
            '#000000',
            '--af',
            '#ffffff',
            '--scb',
            '#000000',
            '--scf',
            '#ffffff',
            '--fbb',
            '#000000',
            '--fbf',
            '#ffffff',
            '--bdr',
            '#ffffff7f']
    )
    #bins
    envPath = os.environ['PATH'].split(":")
    binfiles = []
    for path in envPath:
        for item in pathlib.Path(path).iterdir():
            if item.is_file():
                binfiles.append(item.name)
    #freedesktop
    desktops = {}
    fdPaths = [
        "/usr/share/applications/",
        "/usr/local/share/applications/",
        "~/.local/share/applications/"]
    for path in fdPaths:
        path = pathlib.Path(path)
        if path.is_dir():
            for item in path.iterdir():
                if item.is_file() and item.suffix == ".desktop":
                    entry = DesktopEntry(item)
                    if not entry.getExec() is None:
                        desktops[entry.getName()] = {
                            "cmd":entry.getExec(),
                            "cwd":entry.getPath(),
                            "term":entry.getTerminal(),
                            }
    connfig_path = pathlib.Path.home() / ".config" / "bemenu-launcher"
    if not connfig_path.is_dir():
        connfig_path.mkdir()
    db = DB(connfig_path / "jornal.db")
    # menu
    menu_list = list(desktops.keys()) + binfiles
    db_rating_table = db.get_rating_table()
    if db_rating_table is not None:
        db_names = list(db_rating_table.keys())
        db_names.sort(key=lambda k: db_rating_table[k])
        for db_name in db_names:
            menu_list.remove(db_name)
        menu_list = db_names + menu_list
    selected = menu.run("Run: ",menu_list)
    # run
    selected = selected[:-1]
    if selected in desktops.keys():
        if desktops[selected]["cwd"] == None or desktops[selected]["cwd"] == '':
            subprocess.run(desktops[selected]["cmd"], shell=True, capture_output=True, text=True) 
        else:
            subprocess.run(desktops[selected]["cmd"],cwd=desktops[selected]["cwd"], shell=True, capture_output=True, text=True)
        db.registre(selected)
    elif selected in binfiles:
        subprocess.run(["kitty", "-e", selected])
        db.registre(selected)
    else:
        print("Unknown app")
        subprocess.run(selected, shell=True, capture_output=True, text=True)


