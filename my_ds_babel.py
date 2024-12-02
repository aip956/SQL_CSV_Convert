import sqlite3
import csv
import io

# Convert SQL table to CSV
def sql_to_csv(database, table_name):
    # Use "List of all fault lines"
    # Connect to the SQLite db
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Fetch data from the table
    # print the number of rows
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    print("row_count: ", row_count)

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Fetch column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]

    # Write to CSV format
    output = io.StringIO()
    csv_writer = csv.writer(output)

    # Write header
    csv_writer.writerow(columns)
    # Write data rows
    csv_writer.writerows(rows)

    # Close the database connection
    conn.close()

    return output.getvalue()

# Function to convert CSV to SQL table
def csv_to_sql(csv_content, database, table_name):
    # Connect to the SQLite db
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Read CSV content
    csv_reader = csv.reader(csv_content)

    # Extract column names from the first row
    columns = next(csv_reader)
    print("Columns:", columns)
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
    # Part 1: SQL to CSV - Fault Lines
    database_file = "all_fault_line.db"
    fault_lines_table = "fault_lines"
    print("Running SQL to CSV (Fault Lines)")
    
    # Convert SQL to CSV and print result
    fault_lines_csv = sql_to_csv(database_file, fault_lines_table)
    with open("fault_lines.csv", "w") as file:
        file.write(fault_lines_csv)
    print("SQL to CSV conversion complete; saved to 'fault_lines.csv'.")

    # Part 2: CSV to SQL - Volcanoes
    volcano_csv_file = "list_volcano.csv"
    volcano_db_file = "list_volcanoes.db"
    volcano_table = "volcanoes"
    print("\nRunning CSV to SQL (Volcanoes)")
    with open(volcano_csv_file, "r") as csv_file:
        csv_to_sql(csv_file,volcano_db_file, volcano_table)
    print("CSV to SQL conversion complete. Data stored in 'list_volcanoes.db'.")

    # Part 3a: Use CSV to SQL for the Volcanoes CSV
    print("\nPart 3a: Populating the database with volcanoes from CSV")
    with open(volcano_csv_file, "r") as csv_file:
        csv_to_sql(csv_file, volcano_db_file, volcano_table)
    print(f"Volcanoes successfully added to '{volcano_db_file}' in table {volcano_table}'.")

    # Part 3b: Use SQL to CSV for the Fault Lines table
    print("\nPart 3b: Extracting fault lines from the database to CSV")
    fault_lines_csv = sql_to_csv(database_file, fault_lines_table)
    with open("fault_lines_part3b.csv", "w") as file:
        file.write(fault_lines_csv)
    print("Fault lines successfully exported to 'fault_lines_part3b.csv'.")
