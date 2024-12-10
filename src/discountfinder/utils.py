import logging
import csv


# Configure the logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format for log messages
)

def search_csv_for_string(file_path, search_string):
    """
    Searches for rows in a CSV file that contain the specified string.

    Parameters:
    - file_path (str): Path to the CSV file.
    - search_string (str): The string to search for.

    Returns:
    - matching_rows (list): List of rows (as lists) containing the search string.
    """
    matching_rows = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            # Check if any cell in the row contains the search string
            if any(search_string in cell for cell in row):
                matching_rows.append(row)

    return matching_rows

def read_csv_to_tuples(filename, sep=','):
    result = []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=sep)
        next(reader)  # Skip the header row

        for row in reader:
            if len(row) < 3:
                print("warning, row less than 4 columns")
                continue
            # Ignore the first column and select the next three items
            result.append(list(row[1:4]))  # row[1:4] gets columns 2, 3, and 4

    return result


def search_csv_in_column(reader, search_string, column_index):
    """
    Searches for rows in a CSV file that contain the specified string in a specific column.

    Parameters:
    - file_path (str): Path to the CSV file.
    - search_string (str): The string to search for.
    - column_index (int): The index of the column to search (0-based).

    Returns:
    - matching_rows (list): List of rows (as lists) where the column matches the search string.
    """
    matching_rows = []

    for row in reader:
        # Ensure the column index is valid for the current row
        if column_index < len(row) and search_string in row[column_index]:
            matching_rows.append(row)

    return matching_rows


# Example usage
"""
#logger.debug("This is a debug message")
#logger.info("This is an info message")
#logger.warning("This is a warning message")
#logger.error("This is an error message")
#logger.critical("This is a critical message")
file_path = "example.csv"  # Replace with your file path
search_string = "Alice"  # Replace with your search string
column_index = 1  # Replace with the column index (0-based)
result = search_csv_in_column(file_path, search_string, column_index)

# Example log messages
if result:
    print(f"Rows containing '{search_string}' in column {column_index}:")
    for row in result:
        print(row)
else:
    print(f"No rows found containing '{search_string}' in column {column_index}.")


file_path = "example.csv"  # Replace with your file path
search_string = "Alice"  # Replace with your search string
result = search_csv_for_string(file_path, search_string)

if result:
    print(f"Rows containing '{search_string}':")
    for row in result:
        print(row)
else:
    print(f"No rows found containing '{search_string}'.")
    
# Example usage:
csv_data = read_csv_to_tuples('data.csv')
print(csv_data)
"""