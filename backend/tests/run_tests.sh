#!/bin/bash
 
rm -rf temp/data temp/utils temp/services temp/db

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables for directories
SRC_DIR="../"
TEMP_DIR="temp"
DATA_DIR="$TEMP_DIR/data"
UTILS_DIR="$TEMP_DIR/utils"
SERVICES_DIR="$TEMP_DIR/services"
DB_DIR="$TEMP_DIR/db"

echo "Setting up temporary environment..."

# Create the temp directory structure
mkdir -p "$UTILS_DIR" "$DATA_DIR" "$SERVICES_DIR" "$DB_DIR"

# Copy necessary files and directories to temp
cp -r "$SRC_DIR/utils/." "$UTILS_DIR"
cp -r "$SRC_DIR/data/." "$DATA_DIR"
cp -r "$SRC_DIR/services/." "$SERVICES_DIR"
cp -r "$SRC_DIR/db/." "$DB_DIR"

# Duplicate the stops.csv file as test_stops.csv
cp "$DATA_DIR/stops.csv" "$DATA_DIR/test_stops.csv"

echo "Temporary files copied!"

# Run tests
echo "Running tests..."
pytest .

# Indicate that tests have finished
echo "Tests finished!"

# Clean up the temporary environment
echo "Cleaning up temporary files..."
rm -rf temp/data temp/utils temp/services temp/db

echo "Cleanup complete!"
