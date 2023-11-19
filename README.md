*Note: This project is a part of a data engineering course and is not intended for real-world use.*

# Multinational Retail Data Centralisation

### Overview

As part of a multinational company selling a wide array of goods globally, the current challenge involves scattered sales data across various sources, hindering accessibility and analysis. The project aims to centralize this data, creating a unified, easily analyzable repository. The initial step involves developing a system to consolidate existing company data into a singular database, establishing a single source of truth for sales information. Subsequent phases will focus on querying this database to extract up-to-date business metrics, enhancing data-driven decision-making within the organization.

This project extracts data from the following sources:
- A database stored in AWS RDS
- A PDF stored in an AWS S3 bucket
- A CSV file stored in an AWS S3 bucket
- JSON data stored in an AWS S3 bucket
- JSON data from a REST API

All extracted data is then cleaned using the Pandas library for Python. Once clean, it is imported into a local Postgres database where the data is cast into correct data-types and a star-based schema is developed.

### Dependencies

In order to install all dependencies, run `pip install -r requirements.txt` in the project directory. This will install the following packages:

- boto3
- pandas
- python-dotenv
- Requests
- SQLAlchemy
- tabula_py

*Note: A populated .env file is required for this project to funtion.*

### Project Structure

<pre>
<b>multinational-retail-data-centralisation/</b>
├─ <b>database_utils.py</b>
│  Helper functions for interfacing with databases.
├─ <b>data_extraction.py</b>
│  Code used to extract data from sources.
├─ <b>data_cleaning.py</b>
│  Specialised functions for cleaning extracted data.
├─ <b>casts/</b>
│  The SQL queries required to:
│    - Cast data into correct data types.
│    - Set primary keys.
│    - Set foreign key constraints.
├─ <b>tests/</b>
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

### Tests

