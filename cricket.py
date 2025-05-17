import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the MySQL database
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",  
            user="2k28pcyNk66J4wT.root",  
            password="MJfUrQWyu2HIZEBk",  
            database="cricket_analysis"  
        )
        return mydb
    except mysql.connector.Error as err:
        st.error(f"Database connection error, check yor database server: {err}")
        return None

# Function to execute a SQL query
def execute_query(mydb, query, fetch=True):
    try:
        cursor = mydb.cursor()
        cursor.execute(query)
        if fetch:
            result = cursor.fetchall() # Fetch all rows from the query result
            columns = [col[0] for col in cursor.description] 
            return result, columns
        else:
            mydb.commit()
            return None, None
    except mysql.connector.Error as err:
        raise err  # Raise the error to be handled in the main function

# Function to get list of tables in the database
def get_tables(mydb):
    query = "SHOW TABLES"
    result, columns = execute_query(mydb, query)
    tables = [row[0] for row in result]  # Extract table names from the result
    return tables

# Function to get column names for a table
def get_columns(mydb, table):
    query = f"SHOW COLUMNS FROM {table}"
    result, columns = execute_query(mydb, query)
    columns = [row[0] for row in result]  # Extract column names from the result
    return columns

# Function to create a new record
def create_record(mydb, table, columns, values):
    try:
        cursor = mydb.cursor()
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        cursor.execute(query, values)  # Pass the values as a tuple
        mydb.commit()
        new_id = cursor.lastrowid
        st.success(f"Record created successfully! New ID: {new_id}")
        
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    except Exception as e:
        st.error(f"Error: {e}")
    

# Function to read records
def read_records(mydb, table):
    query = f"SELECT * FROM {table}"
    result, columns = execute_query(mydb, query)
    return result, columns

# Function to update a record
def update_record(mydb, table, column, new_value, condition):
    try:
        if not condition.strip():
            raise ValueError("WHERE condition cannot be empty.")
        query = f"UPDATE {table} SET {column} = %s WHERE {condition}"
        cursor = mydb.cursor()
        cursor.execute(query, (new_value,))
        mydb.commit()
        st.success("Record updated successfully!")
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    except ValueError as ve:
        st.error(f"Validation error: {ve}")

# Function to delete a record
def delete_record(mydb, table, condition):
    try:
        if not condition.strip():
            raise ValueError("WHERE condition cannot be empty.")
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        st.success("Record deleted successfully!")
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
    except ValueError as ve:
        st.error(f"Validation error: {ve}")

# Home Page
def home_page():
    st.title("Welcome to Zomato Food Delivery")
    st.write("Explore delicious food delivered to your doorstep!")

    # Display Zomato food delivery images
    
    

# Main Streamlit app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "CRUD Operations"])

    if page == "Home":
        home_page()
    elif page == "CRUD Operations":
        st.title("CRUD Operations")


    # Connect to the database
    mydb = connect_to_database()

    # Get list of tables in the database
    tables = get_tables(mydb)

    # Sidebar for CRUD operations
    st.sidebar.header("CRUD Operations")
    operation = st.sidebar.selectbox(
        "Choose Operation",
        ["Query Executor", "Create", "Read", "Update", "Delete"]
    )

    if operation == "Query Executor":
        # List of 20 SQL queries
        queries = [
            #Q1
            """select count(*) as total_matches from odis_matches;""",
            #Q2
            """ select city,count(*) as matches
                from odis_matches 
                group by city;""", 
            #Q3
             """ select winner, count(*) as win_count
                 from odis_matches
                 group by winner
                 order by win_count desc; """,
            #Q4
            """select Toss_winner,count(*) as Toss_win
                from odis_matches
                group by Toss_winner
                order by Toss_win desc;""",
            #Q5
            """ select Toss_Decision,count(*) as Decision_count
                from odis_matches
                group by Toss_Decision;  """,
            #Q6
            """ select venue,count(*) as num_of_matches
                from odis_matches
                group by venue 
                order by num_of_matches desc limit 10;""",
            #Q7
            """select Player_of_Match, count(*) as num_of_matches
                from odis_matches
                group by Player_of_Match order by num_of_matches asc;""",
            #Q8
            """ select year(str_to_date(date, '%Y-%m-%d')) as year,count(*) as matches
                from odis_matches
                group by year
                order by year; """,
            #Q9
            """select winner,count(*) as win_batting_first
            from odis_matches
            where `Toss_Decision` = 'bat' and winner = `Toss_winner`
            group by winner
            order by win_batting_first desc;""",
            #10
            """ select winner,count(*) as win_fielding_first
            from odis_matches
            where `Toss_Decision` = 'field' and winner = `Toss_winner`
            group by winner
            order by win_fielding_first desc;""",
            #11
            """select count(*) as num_of_normal_matches
                from odis_matches
                where `Result_Type` = 'normal';""",
            #12
            """select count(*) as num_of_normal_matches
                from odis_matches
                where `Result_Type` = 'tie';""",
            #13
            """select count(*) as num_of_normal_matches
                from odis_matches
                where `Result_Type` = 'no result';""",
            #14
            """ select Gender, count(Player_of_Match) as player_of_match_count
                from odis_matches
                group by Gender;""",
            #15
            """select winner,count(*) as wins
                from odis_matches
                where venue like '%Eden Gardens%'
                group by winner
                order by wins desc;""",
            #16
            """ select venue,count(*) as  match_count
                from tests_matches
                group by venue
                order by match_count desc;""",
            #17
            """SELECT Gender, COUNT(*) AS match_count
                FROM tests_matches
                GROUP BY Gender;
                                """,
            #18
            """select Gender,count(Toss_Winner) as Most_Toss_winner
                from T20s_matches
                group by Gender;""",
            #19
            """select winner,count(*) as win_batting_first
            from Tests_matches
            where `Toss_Decision` = 'bat' and winner = `Toss_winner`
            group by winner
            order by win_batting_first desc;""",
            #20
            """ select winner,count(*) as win_batting_first
            from T20s_matches
            where `Toss_Decision` = 'bat' and winner = `Toss_winner`
            group by winner
            order by win_batting_first desc;""",
            #21

 ]

        query_descriptions = [
            "1.Total Number of ODI Matches Played",
            "2.Total Matches Played Per City",
            "3.Most Frequent Match Winners",
            "4.Team Winning the Most Tosses",
            "5.Matches by Toss Decision (Bat/Field)",
            "6.Top 10 Venues by Match Count",
            "7.How many time Playerof the Match in each player",
            "8.ODI Matches by Year",
            "9.If choosing Toss Decision in Batting First won the Team top order wise",
            "10.If choosing Toss Decision in fielding First won the Team top order wise",
            "11.Total Number of Matches with a Result (normal)",
            "12.Total Number of Matches with a Result (Ties)",
            "13.Total Number of Matches with a Result (No Result)",
            "14.The total Num of of matches in  Player of matches in male and female wise",
            "15.Teams Winning Matches at a Specific Venue (e.g., Eden Gardens)",
            "16.Venue-wise Distribution of Matches",
            "17.Number of Matches by Gender wise in tests matches",
            "18.Most Toss_winner Gender Based T20 matches",
            "19.The Number of tests Matches Won by Each Team Batting First",
            "20.The Number of T20s Matches Won by Each Team Batting First",
            
            ]

        # Create a sidebar selectbox for query selection
        selected_query = st.sidebar.selectbox(
            "Select a Query",
            options=[f"Query {i+1}" for i in range(len(queries))],  # Options: Query 1, Query 2, ..., Query 20
            format_func=lambda x: f"{x}: {query_descriptions[int(x.split(' ')[1]) - 1]}"  # Show descriptions in the dropdown
        )

        # Get the index of the selected query
        query_index = int(selected_query.split(" ")[1]) - 1

        # Display the selected query and its description
        st.write(f"### {selected_query}")
        st.write(f"**Description:** {query_descriptions[query_index]}")
        st.write(f"**SQL Query:** `{queries[query_index]}`")

        # Execute the selected query
        try:
            result, columns = execute_query(mydb, queries[query_index])   # Execute the selected query
            st.write("**Result:**")
            st.table(pd.DataFrame(result, columns=columns))  # Display the result as a table with column names
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")  # Display any errors that occur

    elif operation == "Create":
        st.header("Create a New Record")
        table = st.selectbox("Select Table", tables)  # Dropdown for table selection
        columns = st.text_input("Columns (comma-separated)")
        values = st.text_input("Values (comma-separated)")
        if st.button("Create"):
            if table and columns and values:
                columns = [col.strip() for col in columns.split(",")]
                values = [val.strip() for val in values.split(",")]
                create_record(mydb, table, columns, values)
            else:
                st.error("Please fill in all fields.")

    elif operation == "Read":
        st.header("Read Records")
        table = st.selectbox("Select Table", tables)  # Dropdown for table selection
        if st.button("Read"):
            if table:
                result, columns = read_records(mydb, table)
                st.write("**Records:**")
                st.table(pd.DataFrame(result, columns=columns))  # Display the result as a table with column names
                
            else:
                st.error("Please provide a table name.")

    elif operation == "Update":
        st.header("Update a Record")
        table = st.selectbox("Select Table", tables)  # Dropdown for table selection
        if table:
            columns = get_columns(mydb, table)  # Fetch column names for the selected table
            column = st.selectbox("Select Column to Update", columns)  # Dropdown for column selection
            new_value = st.text_input(f"New Value for {column}")
            condition = st.text_input("WHERE condition (e.g., id = 1)")
            if st.button("Update"):
                if table and column and new_value and condition:
                    if "=" not in condition:
                        st.error("Invalid WHERE condition. It must include an '=' operator (e.g., id = 1).")
                    else:
                        update_record(mydb, table, column, new_value, condition)
                else:
                    st.error("Please fill in all fields.")

    elif operation == "Delete":
        st.header("Delete a Record")
        table = st.selectbox("Select Table", tables)  # Dropdown for table selection
        condition = st.text_input("WHERE condition (e.g., id = 1)")
        if st.button("Delete"):
            if table and condition:
                delete_record(mydb, table, condition)
            else:
                st.error("Please fill in all fields.")

# Run the app
if __name__ == "__main__":
    main()