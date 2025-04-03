# JSON Cleaner

A tool for cleaning and transforming NCAA school staff directory data from irregular JSON formats into a standardized structure.

## Overview

This script parses NCAA school staff directories with varying formats and transforms them into a consistent structure with the following fields for each staff member:

- `school`: School name
- `sport`: Sport category
- `full_name`: Staff member's full name
- `position`: Staff member's position
- `phone`: Phone number
- `email`: Email address
- `first_name`: First name
- `last_name`: Last name

## Usage

1. Place your input JSON file in the `data/` directory
2. Update the input and output file paths in the script if needed
3. Run the script:

```bash
python json_cleaning.py
```

## Features

- Handles inconsistent formatting across different schools' staff directories
- Extracts phone numbers from text using regex
- Removes social media handles and usernames from position fields
- Separates names and positions using pattern matching
- Cleans up year references in names (like '22)
- Extracts first and last names from full names 