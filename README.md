#Cricsheet Match Data Analysis Project
#Project Overview
This project analyzes cricket match data from Cricsheet using Python, SQL, and Power BI. The aim is to extract, preprocess, analyze, and visualize match data for various formats (ODI, Test, T20) to uncover performance insights about players and teams.

#Problem Statement
Process cricket match data in JSON format from Cricsheet.

Transform raw data into structured SQL tables.

Perform statistical and performance analysis using SQL.

Visualize insights using Python EDA and Power BI dashboard.

#Technologies Used
Python – JSON parsing, data cleaning, EDA (matplotlib, seaborn, plotly)

Pandas – DataFrame manipulation

#SQL (MySQL) – Database creation and analytical queries

Power BI – Interactive dashboards

Cricsheet JSON Data – Source of match data (ODI, T20, Test)

📁 cricsheet-analysis-project/
│
├── data/                    # Raw JSON match files
├── scripts/
│   ├── json_to_df.py        # JSON to DataFrame conversion
│   ├── insert_to_sql.py     # SQL table creation and data insertion
│   └── eda_visuals.py       # EDA visualizations using matplotlib, seaborn, etc.
│
├── sql/
│   ├── create_tables.sql    # SQL schema definitions
│   └── analysis_queries.sql # 20 SQL queries for insights
│
├── powerbi/
│   └── dashboard.pbix       # Power BI dashboard file
│
├── presentation/            # EDA graphs & insights
│   └── eda_slides.pdf
│
└── README.md                # Project documentation

#Key Features & Insights
Preprocessing: Cleaned and structured JSON match data.

SQL Analysis:

Top batsmen and bowlers by match format.

Win/loss ratios and team performance trends.

Matches with narrowest victory margins.

Python EDA:

Visual comparison of player stats and team trends.

Power BI Dashboard:

Interactive filters for team and player insights.

Visual storytelling with KPIs and match summaries.

#Dataset Info
Source: Cricsheet Match Data

Format: JSON files (ODI, Test, T20 matches)

Contains: Player stats, match metadata, deliveries, innings data.

#Skills Demonstrated
Data cleaning and transformation

SQL data modeling and querying

Exploratory data analysis

Dashboard development with Power BI
