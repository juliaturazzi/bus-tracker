import pytest
from mysql.connector import Error
from temp.db.create_db import BusStopDatabase


@pytest.fixture(scope="function")
def db():
    database = BusStopDatabase()
    yield database
    try:
        conn = database._connect()
        cursor = conn.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {database.database}")
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(e)


def test_database_creation(db):
    conn = db._connect()
    cursor = conn.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{db.database}'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    assert result is not None, "Database should be created"


def test_table_creation(db):
    conn = db._connect()
    cursor = conn.cursor()
    cursor.execute(f"SHOW TABLES IN {db.database} LIKE 'stops'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    assert result is not None, "Table should be created"


def test_insert_bus_stop(db):
    db.insert_bus_stop(
        email="test@example.com",
        bus_line="42",
        stop_name="Main St",
        latitude=123.456,
        longitude=-123.456,
        start_time="08:00:00",
        end_time="10:00:00",
    )

    conn = db._connect()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM {db.database}.stops WHERE email=%s", ("test@example.com",)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    assert result is not None, "Bus stop should be inserted"


def test_get_all_bus_stops(db):
    db.insert_bus_stop(
        email="test1@example.com",
        bus_line="42",
        stop_name="Main St",
        latitude=123.456,
        longitude=-123.456,
        start_time="08:00:00",
        end_time="10:00:00",
    )

    db.insert_bus_stop(
        email="test2@example.com",
        bus_line="43",
        stop_name="2nd St",
        latitude=123.789,
        longitude=-123.789,
        start_time="09:00:00",
        end_time="11:00:00",
    )

    results = db.get_all_bus_stops()
    assert len(results) == 2, "There should be 2 bus stops in the table"
