import csv


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


import csv


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
file_path = "example.csv"  # Replace with your file path
search_string = "Alice"  # Replace with your search string
column_index = 1  # Replace with the column index (0-based)
result = search_csv_in_column(file_path, search_string, column_index)

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
"""