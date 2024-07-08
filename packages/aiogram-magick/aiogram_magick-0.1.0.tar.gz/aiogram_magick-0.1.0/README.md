<p align="center">
    <h1 align="center">Aiogram Magick</h1>
    <p align="center">
        <a href="https://pypi.org/project/aiogram_magick/"><img alt="PyPI" src="https://img.shields.io/pypi/v/aiogram_magick?style=flat&logo=python&logoColor=white"></a>
    </p>
    <p align="center">Magick for Aiogram 3.x-based Telegram bots.</p>
    <p align="center">
        <a href="https://arichr.github.io/aiogram_magick/"><img alt="Read documentation" src="https://img.shields.io/badge/read-documentation-cyan?style=for-the-badge&logo=python&logoColor=white"></a>
    </p>
</p>

**Compontents:**

* [SQLite-based storage with caching & automatic commits](https://arichr.github.io/aiogram-magick/2_-_SQLite_storage.html)

## Getting started!

1. Install `aiogram_magick` and dependencies for submodules:
```console
pip install aiogram_magick

# For aiogram_magick.sqlite
pip install aiosqlite jsonpickle
```
2. Import submodules that provide needed functionality ([see examples below](#examples) or [read documentation](https://arichr.github.io/aiogram-magick/))

## Examples

### SQLite storage
```python
from aiogram_magick.sqlite import SqliteStorage

# By default, SqliteStorage is configured to:
#    - Commit changes on 30 minute idle and on shutdown;
#    - Cache states (up to 20 entries) and data (up to 10 entries);
#    - Ignore any exceptions;
#    - To avoid file corruptions on shutdown any `sqlite3.OperationalError`s
#      are printed using `traceback.print_exception` instead of raised normally.
dp = Dispatcher(storage=SqliteStorage('aiogram.sqlite'))
```
