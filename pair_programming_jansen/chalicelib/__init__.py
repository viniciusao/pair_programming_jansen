import pathlib
import sqlite3


DB_PATH = pathlib.Path(__file__).parent.parent.joinpath('pair_programming.db').resolve()


db = sqlite3.connect(DB_PATH)
cursor = db.cursor()