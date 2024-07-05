import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text, inspect, Column, String, Integer, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import column
def get_abs_path():
  return os.path.abspath(__name__)
def get_abs_dir():
  return os.path.dirname(get_abs_path())
def create_abs_path(path):
  return os.path.join(get_abs_dir(),path)
def get_db_url(db_path):
    db_url = f"sqlite:///{db_path}"
    return db_url
class DatabaseBrowser:
    def __init__(self, db_path):
        self.db_url=get_db_url(db_path)
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.metadata = MetaData()
        self.inspector = inspect(self.engine)
    
    def list_tables(self):
        """List all tables in the database."""
        tables = self.inspector.get_table_names()
        print("Available tables:")
        for idx, table in enumerate(tables):
            print(f"{idx + 1}. {table}")
        return tables

    def list_columns(self, table_name):
        """List all columns in a table."""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            columns = [column.name for column in table.columns]
            print(f"Columns in {table_name}:")
            for idx, column in enumerate(columns):
                print(f"{idx + 1}. {column}")
            return columns
        except Exception as e:
            print(f"Error loading table {table_name}: {e}")
            return []

    def view_table(self, table_name, start=0, end=5):
        """View a range of rows in a table."""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            query = table.select().offset(start).limit(end - start)
            result = self.session.execute(query)
            rows = result.fetchall()

            if rows:
                df = pd.DataFrame(rows)
                df.columns = result.keys()
                # Set pandas options to display all rows and columns
                pd.set_option('display.max_rows', None)
                pd.set_option('display.max_columns', None)
                pd.set_option('display.width', None)
                pd.set_option('display.max_colwidth', None)
                print(df)
                # Reset pandas options to default
                pd.reset_option('display.max_rows')
                pd.reset_option('display.max_columns')
                pd.reset_option('display.width')
                pd.reset_option('display.max_colwidth')
            else:
                print(f"No data found in table {table_name} from row {start} to {end}")
        except Exception as e:
            print(f"Error viewing table {table_name}: {e}")

    def search_table(self, table_name, column_name, search_value):
        """Search for a specific value in a table."""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
        except Exception as e:
            print(f"Error loading table {table_name}: {e}")
            return
        
        if column_name not in [col.name for col in table.columns]:
            print(f"Column {column_name} does not exist in table {table_name}.")
            return

        try:
            query = text(f"SELECT * FROM {table_name} WHERE {column_name} = :val")
            result = self.session.execute(query, {"val": search_value})
            rows = result.fetchall()

            if rows:
                df = pd.DataFrame(rows)
                df.columns = result.keys()
                print(df)
            else:
                print(f"No results found for {search_value} in {column_name} of {table_name}")
        except Exception as e:
            print(f"Error executing search query: {e}")

    def alter_column_type(self, table_name, column_name, new_type):
        """Alter the type of a specific column in a table."""
        if new_type not in ['String', 'Integer', 'Float']:
            print("Invalid type. Please choose from 'String', 'Integer', or 'Float'.")
            return
        
        try:
            # Load the table
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            old_column = table.c[column_name]
            
            # Determine the new column type
            if new_type == 'String':
                new_column = Column(column_name, String, nullable=old_column.nullable)
            elif new_type == 'Integer':
                new_column = Column(column_name, Integer, nullable=old_column.nullable)
            elif new_type == 'Float':
                new_column = Column(column_name, Float, nullable=old_column.nullable)
            
            # Perform the column type change
            with self.engine.connect() as connection:
                connection.execute(text(f"ALTER TABLE {table_name} RENAME COLUMN {column_name} TO {column_name}_old"))
                connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {new_type}"))
                connection.execute(text(f"UPDATE {table_name} SET {column_name} = {column_name}_old"))
                connection.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}_old"))
                connection.commit()
            
            print(f"Column {column_name} in table {table_name} successfully altered to {new_type}.")
        except Exception as e:
            print(f"Error altering column type: {e}")

    def update_all_entries(self, table_name, column_name, new_value):
        """Update all entries in a specific column with a new value."""
        try:
            table = Table(table_name, self.metadata, autoload_with=self.engine)
            query = table.update().values({column_name: new_value})
            result = self.session.execute(query)
            self.session.commit()
            print(f"All entries in column {column_name} of table {table_name} updated to {new_value}.")
        except Exception as e:
            print(f"Error updating entries: {e}")

    def export_data_by_zipcode(self, table_name,value, file_path,key='zipcode' ):
        """Export data from a specific zipcode to an Excel file."""
        try:
            query = text(f"SELECT * FROM {table_name} WHERE {key} = :{key}")
            result = self.session.execute(query, {"{key}": value})
            rows = result.fetchall()

            if rows:
                df = pd.DataFrame(rows)
                df.columns = result.keys()
                df.to_excel(file_path, index=False)
                print(f"Data for {key} {value} exported to {file_path}")
            else:
                print(f"No data found for {key} {value} in table {table_name}")
        except Exception as e:
            print(f"Error exporting data: {e}")

    def get_integer_input(self, prompt, min_value, max_value):
        """Get an integer input from the user within a specified range."""
        while True:
            try:
                value = int(input(f"{prompt} ({min_value}-{max_value}): "))
                if min_value <= value <= max_value:
                    return value
                else:
                    print(f"Please enter a number between {min_value} and {max_value}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def main(self):
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List tables")
            print("2. Search table")
            print("3. View table contents")
            print("4. List columns in a table")
            print("5. Alter column type")
            print("6. Update all entries in a column")
            print("7. Export data by key")
            
            choice = input("Enter your choice: ")

            if choice == "0":
                logging.info("Exiting the program")
                print("Exiting...")
                break
            elif choice == "1":
                self.list_tables()
            elif choice == "2":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                columns = self.list_columns(table_name)
                if not columns:
                    continue
                column_choice = self.get_integer_input("Choose a column", 1, len(columns)) - 1
                column_name = columns[column_choice]
                search_value = input(f"Enter value to search for in {column_name}: ")
                self.search_table(table_name, column_name, search_value)
            elif choice == "3":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                table_row_count = self.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                start = self.get_integer_input(f"Enter start row (0-{table_row_count - 1})", 0, table_row_count - 1)
                end = self.get_integer_input(f"Enter end row ({start + 1}-{table_row_count})", start + 1, table_row_count)
                self.view_table(table_name, start, end)
            elif choice == "4":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                self.list_columns(table_name)
            elif choice == "5":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                columns = self.list_columns(table_name)
                if not columns:
                    continue
                column_choice = self.get_integer_input("Choose a column", 1, len(columns)) - 1
                column_name = columns[column_choice]
                new_type = input("Enter new type (String, Integer, Float): ")
                self.alter_column_type(table_name, column_name, new_type)
            elif choice == "6":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                columns = self.list_columns(table_name)
                if not columns:
                    continue
                column_choice = self.get_integer_input("Choose a column", 1, len(columns)) - 1
                column_name = columns[column_choice]
                new_value = input(f"Enter new value for all entries in {column_name}: ")
                self.update_all_entries(table_name, column_name, new_value)
            elif choice == "7":
                tables = self.list_tables()
                if not tables:
                    continue
                table_choice = self.get_integer_input("Choose a table", 1, len(tables)) - 1
                table_name = tables[table_choice]
                columns = self.list_columns(table_name)
                if not columns:
                    continue
                column_choice = self.get_integer_input("Choose a column", 1, len(columns)) - 1
                column_name = columns[column_choice]
                value = input(f"Enter the {column_name} value to filter by: ")
                file_path = input("Enter the file path to save the Excel file: ")
                self.export_data_by_zipcode(table_name=table_name, value=value, file_path=file_path,key=column_name)
            else:
                print("Invalid choice. Please try again.")

