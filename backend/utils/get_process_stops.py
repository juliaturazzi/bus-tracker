import re
import csv


# process CSV file with duplicate bus stops stop names
def process_stops(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        stops = list(reader)

    stop_name_counts = {}
    for stop in stops:
        stop_name = stop[2]
        base_name = re.sub(r" \d+$", "", stop_name)

        # append numeric suffix if duplicated
        if base_name in stop_name_counts:
            stop_name_counts[base_name] += 1
        else:
            stop_name_counts[base_name] = 1

        if stop_name != base_name:
            current_number = int(stop_name.split()[-1])
            new_number = max(current_number, stop_name_counts[base_name])
            stop[2] = f"{base_name} {new_number}"
        elif stop_name_counts[base_name] > 1:
            stop[2] = f"{base_name} {stop_name_counts[base_name]}"

    # updated rows to output CSV file
    with open(output_file, "w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(stops)


if __name__ == "__main__":
    input_file = "stops.csv"  # input CSV
    output_file = "stops_updated.csv"  # output CSV
    process_stops(input_file, output_file)
    print(f"{output_file} file created")
