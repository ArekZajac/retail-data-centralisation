*Note: This project is a part of a data engineering course and is not intended for real-world use.*

# Multinational Retail Data Centralisation

> ### Scenario
> 
> You work for a multinational company that sells various goods across the globe.
> 
> Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team.
>
> In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location.
>
> Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data.
>
> You will then query the database to get up-to-date metrics for the business.

### Overiew

This project extracts data from the following sources:
- A database stored in AWS RDS
- A PDF stored in an AWS S3 bucket
- A CSV file stored in an AWS S3 bucket
- JSON data stored in an AWS S3 bucket
- JSON data from a REST API

All extracted data is then cleaned using the Pandas library for Python. Once clean, it is imported into a local Postgres database where the data is cast into correct data-types and a star-based schema is developed.


### Project Structure

<pre>
<b>multinational-retail-data-centralisation/</b>
├─ <b>database_utils.py</b>
│  Helper functions for interfacing with databases.
├─ <b>data_extraction.py</b>
│  Code used to extract data from various sources.
├─ <b>data_cleaning.py</b>
│  Specialised functions for cleaning specific data.
├─ <b>casts/</b>
│  The SQL queries required to:
│    - Cast data into correct data types.
│    - Set primary keys.
│    - Set foreign key constraints.
├─ <b>queries/</b>
│  SQL queries to test the local database.
├─ <b>db_backups/</b>
│  Backups of the local database during project milestones.
├─ <b>README.md</b>
├─ <b>LICENSE</b>
</pre>

### Local Database Schema

<div align="center">
  <img src="erd.png" width="1000"/>
</div>
