# Krakow Bike Traffic Analysis

Final project for the course [Tools Supporting Data Analysis in Python](https://usosweb.fuw.edu.pl/kontroler.php?_action=katalog2/przedmioty/pokazPrzedmiot&kod=1000-1M20NPD)

## Overview

This Python package provides comprehensive analysis tools for bicycle traffic patterns in Krakow from 2017 to 2021. The package examines correlations between bicycle traffic intensity and various weather factors including temperature, air quality, and precipitation.

## Features

- **Data Analysis**: Correlation analysis between weather conditions and bicycle traffic using pandas and numpy
- **Data Visualization**: Charts and plots generated with matplotlib and seaborn
- **Automated Reporting**: HTML report generation that automatically opens in your browser
- **Flexible Time Periods**: Analyze data for any custom date range within the available dataset
- **Comprehensive Testing**: Full test coverage using pytest
- **Documentation**: Jupyter notebook with usage examples and function demonstrations

## Installation

Clone this repository and install the package using pip:

```bash
git clone [repository-url]
pip install path/to/krakowbike-project
```

## Usage

### Generate Complete Report

Create a comprehensive analysis report with default settings:

```bash
genreport -p path/to/krakowbike-project -o path/to/output/directory
```

### Customize Your Analysis

You can customize the report generation with the following options:

- **Custom report name**: Add `-r report_name` (default: `krakow_bike_report`)
- **Custom start date**: Add `-s 2018-01-01` to specify analysis start date
- **Custom end date**: Add `-e 2020-08-31` to specify analysis end date

Example with custom parameters:
```bash
genreport -p path/to/krakowbike-project -o path/to/output/directory -r my_custom_report -s 2018-06-01 -e 2019-12-31
```

## Data Coverage

The analysis covers bicycle traffic data from **January 2017 to December 2021**, allowing you to explore traffic patterns across different seasons and weather conditions in Krakow.

## Project Structure

- **Unit Tests**: Comprehensive test suite built with pytest
- **Example Notebook**: Jupyter notebook demonstrating package functionality
- **HTML Reports**: Automatically generated and browser-launched analysis reports
- **Data Visualization**: Professional charts and graphs for data interpretation

## Requirements

- Python 3.9 or higher

For a complete list of dependencies, see `requirements.txt`.
