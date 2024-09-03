import os
import csv
from temp.utils.get_process_stops import process_stops

INPUT_FILE = "temp/data/test_stops.csv"
OUTPUT_FILE = "temp/data/test_stops_updated.csv"


def setup_csv(INPUT_FILE, stops_data):
    with open(INPUT_FILE, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stops_data)


def test_basic_functionality():

    stops_data = [
        ["stop_id", "stop_code", "stop_name", "stop_desc"],
        ["1", "1001", "Main St", "Description 1"],
        ["2", "1002", "Main St", "Description 2"],
        ["3", "1003", "Main St", "Description 3"],
        ["4", "1004", "Second St", "Description 4"],
    ]
    setup_csv(INPUT_FILE, stops_data)
    process_stops(INPUT_FILE, OUTPUT_FILE)

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        updated_data = list(reader)

    assert updated_data[1][2] == "Main St"
    assert updated_data[2][2] == "Main St 2"
    assert updated_data[3][2] == "Main St 3"
    assert updated_data[4][2] == "Second St"

    os.remove(INPUT_FILE)
    os.remove(OUTPUT_FILE)


def test_no_duplicates():

    stops_data = [
        ["stop_id", "stop_code", "stop_name", "stop_desc"],
        ["1", "1001", "First St", "Description 1"],
        ["2", "1002", "Second St", "Description 2"],
    ]
    setup_csv(INPUT_FILE, stops_data)
    process_stops(INPUT_FILE, OUTPUT_FILE)

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        updated_data = list(reader)

    assert updated_data[1][2] == "First St"
    assert updated_data[2][2] == "Second St"

    os.remove(INPUT_FILE)
    os.remove(OUTPUT_FILE)


def test_duplicates_with_numbers():

    stops_data = [
        ["stop_id", "stop_code", "stop_name", "stop_desc"],
        ["1", "1001", "Main St", "Description 1"],
        ["2", "1002", "Main St 2", "Description 2"],
        ["3", "1003", "Main St", "Description 3"],
    ]
    setup_csv(INPUT_FILE, stops_data)
    process_stops(INPUT_FILE, OUTPUT_FILE)

    with open(OUTPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        updated_data = list(reader)

    assert updated_data[1][2] == "Main St"
    assert updated_data[2][2] == "Main St 2"
    assert updated_data[3][2] == "Main St 3"

    os.remove(INPUT_FILE)
    os.remove(OUTPUT_FILE)
