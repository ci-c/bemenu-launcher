#!/usr/bin/python3

import os
import subprocess
import pathlib
from xdg.DesktopEntry import DesktopEntry
import sqlite3
import datetime
import logging

from Menu import Menu

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
        a = 0.8
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
            for pathItem in path.iterdir():
                if pathItem.is_file() and pathItem.suffix == ".desktop":
                    entry = DesktopEntry(pathItem)
                    if not entry.getExec() is None:
                        desktops[entry.getName()] = pathItem
    connfig_path = pathlib.Path.home() / ".config" / "bemenu-launcher"
    if not connfig_path.is_dir():
        connfig_path.mkdir()
    db = DB(connfig_path / "jornal.db")
    # menu
    menu_list = list(desktops.keys()) + binfiles
    db_rating_table = db.get_rating_table()
    if db_rating_table is not None:
        db_names = list(db_rating_table.keys())
        db_names.sort(key=lambda k: db_rating_table[k],reverse=True)
        for db_name in db_names:
            if db_name in menu_list:
                menu_list.remove(db_name)
        menu_list = db_names + menu_list
    selected = menu.run("Run: ",menu_list)
    # run
    selected = selected[:-1]
    if selected in desktops.keys():
        subprocess.run(["dex" , desktops[selected]]) 
        db.registre(selected)
    elif selected in binfiles:
        subprocess.run(f"kitty -e {selected}",shell=True, text=True) # , "--hold"
        db.registre(selected)
    elif selected == "":
        print("Nothing selected")
    else:
        print(f"Unknown input: '{selected}' - run in shell")
        subprocess.run(selected, shell=True, capture_output=True, text=True)


