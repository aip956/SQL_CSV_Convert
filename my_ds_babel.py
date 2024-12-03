import sqlite3
import csv
import io

# Convert SQL table to CSV
# Converts a specified table from an SQLite db to CSV format.
# Args: 
#     - database (str): Path to the SQLite db file
#     - table name (str): Name of the table to export
# Returns:
#     - str: CSV-formatted string of the table content

def sql_to_csv(database, table_name):
    # Use "List of all fault lines"
    # Connect to the SQLite db
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Fetch data from the table
    # print the number of rows
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    # print("row_count: ", row_count)

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Fetch column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Write to CSV format
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(columns) # Write header
    csv_writer.writerows(rows)     # Write data rows

    conn.close() # Close the database connection
    return output.getvalue()

# Function to convert CSV to SQL table
# Creates a table in an SQLite db from CSV content and populates it with data.
# Args:
#     - csv_content (file-like object): CSV content to be imported.
#     - database (str): Path to the SQLite db file
#     - table_name (str): Name of the table to create and populate.
# Returns:
#     - None
def csv_to_sql(csv_content, database, table_name):
    # Connect to the SQLite db
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Read CSV content
    csv_reader = csv.reader(csv_content)

    columns = next(csv_reader) # Extract column names from the first row
    # print("Columns:", columns)
    placeholders = ', '.join(['?' for _ in columns]) # Creates placholders for INSERT

    # Create the table dynamically
    column_definitions = ', '.join([f'"{col}" TEXT' for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")

    # Insert rows
    for row in csv_reader:
        cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    # Commit and close the connection 
    conn.commit()
    conn.close()


# Main program: Execute all parts
if __name__ == "__main__":
    # Part 1 and 3b: SQL to CSV - Export fault_lines table
    database_file = "all_fault_line.db"
    fault_lines_table = "fault_lines"
    print("Exporting fault lines from SQL to CSV")
        
    fault_lines_csv = sql_to_csv(database_file, fault_lines_table) # Convert SQL to CSV and print result
    with open("list_fault_lines.csv", "w") as file:
        file.write(fault_lines_csv)
    print("SQL to CSV conversion and export complete; saved to 'list_fault_lines.csv'.")
    

    # Part 2 and 3a: CSV to SQL - Import volcanoes data
    volcano_csv_file = "list_volcano.csv"
    volcano_db_file = "list_volcanoes.db"
    volcano_table = "volcanoes"
    print("\nImporting volcanoes from CSV to SQL")
    with open(volcano_csv_file, "r") as csv_file:
        csv_to_sql(csv_file, volcano_db_file, volcano_table)
    print("Import complete. Data stored in 'list_volcanoes.db'.")

