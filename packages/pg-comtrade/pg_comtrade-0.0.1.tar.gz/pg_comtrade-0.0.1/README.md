# pg-comtrade

Python utility function to ingest data from UN Comtrade's bulk API into a (partitioned) PostgreSQL table.


## Installation

pg-comtrade can be installed from PyPI using pip. psycopg2 or psycopg (Psycopg 3) must also be explicitly installed.

```bash
pip install pg-comtrade psycopg
```


## Usage

```python
from pg_comtrade import sync_goods_yearly

# For example purposes, PostgreSQL can be run locally using this...
# docker run --rm -it -e POSTGRES_HOST_AUTH_METHOD=trust -p 5432:5432 postgres

# ... which should work with this engine
engine = sa.create_engine('postgresql+psycopg://postgres@127.0.0.1:5432/')

# ... to ingest into the un.comtrade_goods table
with engine.connect() as conn:
    sync_goods_yearly(conn, 'un', 'comtrade_goods', subscription_key='123456abcdef')
```

## Development / running tests

To develop pg-comtrade, you will need to install the package in editable mode, and install development dependencies.

```bash
pip install -e '.[dev]'
```

And then to run the tests:

```bash
pytest
```

