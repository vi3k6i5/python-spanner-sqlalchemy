# Copyright 2021 Google LLC
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file or at
# https://developers.google.com/open-source/licenses/bs

from samples import snippets
from samples.conftest import insert_data
from sqlalchemy import (
    Column,
    create_engine,
    Integer,
    inspect,
    MetaData,
    String,
    Table,
)

DATA = [
    {"user_id": 1, "user_name": "abcdefg"},
    {"user_id": 2, "user_name": "ab/cdefg"},
    {"user_id": 3, "user_name": "ab%cdefg"},
    {"user_id": 4, "user_name": "ab_cdefg"},
    {"user_id": 5, "user_name": "abcde/fg"},
    {"user_id": 6, "user_name": "abcde%fg"},
]


def test_enable_autocommit_mode(capsys, db_url):
    conn = snippets.enable_autocommit_mode(db_url)

    out, err = capsys.readouterr()
    assert "Connection autocommit default mode is " in out
    assert "Spanner DBAPI default autocommit mode is False" in out

    assert conn.connection.connection.autocommit is True
    assert "Connection autocommit mode is " in out
    assert "Spanner DBAPI autocommit mode is True" in out


def test_create_table(capsys, db_url, random_table_id):
    table = snippets.create_table(db_url, random_table_id)

    out, err = capsys.readouterr()
    assert "created successfully" in out
    assert table.name == random_table_id
    assert table.exists() is True

    table.drop()


def test_drop_table(capsys, db_url, random_table_id):
    engine = create_engine(db_url)
    metadata = MetaData(bind=engine)

    table = Table(
        random_table_id,
        metadata,
        Column("user_id", Integer, primary_key=True),
        Column("user_name", String(16), nullable=False),
    )

    table.create()

    snippets.drop_table(table)

    out, err = capsys.readouterr()
    assert "dropped successfully" in out
    assert table.exists() is False


def test_get_table_name(capsys, db_url, table):
    tables = snippets.get_table_names(db_url)

    out, err = capsys.readouterr()
    assert "Table names are:" in out
    assert table.name in tables


def test_table_create_unique_index(capsys, db_url, table):
    snippets.create_unique_indexes(table)

    engine = create_engine(db_url)
    insp = inspect(engine)
    indexes = insp.get_indexes(table.name)

    out, err = capsys.readouterr()

    assert "Index created successfully" in out
    assert indexes[0]["unique"] is True


def test_table_delete_all_rows(capsys, connection, table):
    insert_data(connection, table, DATA)
    snippets.delete_all_rows(connection, table)

    out, err = capsys.readouterr()
    assert "Total inserted rows: 6" in out
    assert "Total rows: 0" in out


def test_table_delete_row_with_where_condition(capsys, connection, table):
    insert_data(connection, table, DATA)
    snippets.delete_row_with_where_condition(connection, table)

    out, err = capsys.readouterr()
    assert "Total inserted rows: 6" in out
    assert "Total rows: 5" in out


def test_exists_table(capsys, table):
    snippets.table_exists(table)

    out, err = capsys.readouterr()
    assert "Table exists" in out


def test_table_fetch_rows(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.fetch_rows(connection, table)

    out, err = capsys.readouterr()
    assert "Total rows:" in out
    assert len(rows) is 6


def test_table_fetch_rows_with_limit(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.fetch_rows_with_limit(connection, table)

    out, err = capsys.readouterr()
    assert "The rows are:" in out
    assert len(rows) is 2


def test_table_fetch_rows_with_limit_offset(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.fetch_rows_with_limit_offset(connection, table)

    out, err = capsys.readouterr()
    assert "The rows are:" in out
    assert len(rows) is 2


def test_table_fetch_rows_with_offset(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.fetch_rows_with_offset(connection, table)

    out, err = capsys.readouterr()
    assert "The rows are:" in out
    assert len(rows) is 4


def test_table_fetch_rows_with_order_by(capsys, connection, table):
    insert_data(connection, table, DATA)
    snippets.fetch_rows_with_order_by(connection, table)

    out, err = capsys.readouterr()
    assert "The order by result is:" in out


def test_table_fetch_row_with_where_condition(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.fetch_row_with_where_condition(connection, table)

    out, err = capsys.readouterr()
    assert "Output is :" in out
    assert len(rows) is 1


def test_table_filter_data_endswith(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.filter_data_endswith(connection, table)

    out, err = capsys.readouterr()
    assert "Filtered data:" in out
    assert len(rows) is 4


def test_table_filter_data_startswith(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.filter_data_startswith(connection, table)

    out, err = capsys.readouterr()
    assert "Filtered data:" in out
    assert len(rows) is 3


def test_table_filter_data_with_contains(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.filter_data_with_contains(connection, table)

    out, err = capsys.readouterr()
    assert "Filtered data:" in out
    assert len(rows) is 4


def test_table_filter_data_with_like(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.filter_data_with_like(connection, table)

    out, err = capsys.readouterr()
    assert "Filtered data:" in out
    assert len(rows) is 3


def test_table_get_columns(capsys, db_url, table):
    columns = snippets.get_table_columns(db_url, table)
    out, err = capsys.readouterr()
    assert "Columns are:" in out
    assert len(columns) is 2

    for single in columns:
        assert single["name"] in table.columns


def test_table_get_foreign_key(capsys, db_url, table_w_foreign_key):
    f_key = snippets.get_table_foreign_key(db_url, table_w_foreign_key)
    table_fk = list(table_w_foreign_key.foreign_keys)[0]
    out, err = capsys.readouterr()

    assert "Foreign key is:" in out
    assert f_key[0].get("name") == table_fk.name


def test_table_get_indexes(capsys, db_url, table):
    indexes = snippets.get_table_indexes(db_url, table)
    out, err = capsys.readouterr()
    table_index = list(table.indexes)[0].name

    assert "Indexes are:" in out
    assert indexes[0]["name"] == table_index


def test_table_get_primary_key(capsys, db_url, table):

    p_key = snippets.get_table_primary_key(db_url, table)
    out, err = capsys.readouterr()
    assert "Primary key is:" in out
    assert p_key.get("constrained_columns")[0] in table.primary_key.columns


def test_table_insert_row(capsys, connection, table):
    rows = snippets.insert_row(connection, table)

    out, err = capsys.readouterr()
    assert "Total rows:" in out
    assert len(rows) is 1


def test_table_update_row(capsys, connection, table):
    insert_data(connection, table, DATA)
    rows = snippets.update_row(connection, table)

    out, err = capsys.readouterr()
    assert "Updated row is :" in out
    assert "GEH" == rows[0][1]