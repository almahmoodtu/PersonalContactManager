# PersonalContactManager
PersonalContactManager™ is a personalised and fun project that manages a database of personal contacts.

This Readme provides a brief overview of the program created using Python. Please refer to annotations and comments within the codes for details.



## The problem

I like to maintain a file (usually in a spreadsheet) where I compile key information of my personal contacts:
* name
* relationship
* phone
* email
* address
* birthday

Hence, the requirement is to set up a Python program that:
1. perform standard database functions (add, edit, delete, merge, query and reports)
2. search records using "approximate match of strings" (to accomodate typos, unknown spellings, etc.) 
3. store data in CSV files (to ensure compatibility with other tools such as SQL, etc.)



## Program structure

![PersonalContactManager](https://drive.google.com/uc?export=view&id=1bIniJqO_hUhXBb5LoUPO8p5Y_hkf2OnF)

The program directory contains four files. Description of the files in the directory are summarised as follows:

#### CSV files `tbContacts.csv`, `tbRelations.csv`:
Using the relational database model, the two files are connected using a primary and secondary key.

![PersonalContactManager](https://drive.google.com/uc?export=view&id=1q2gdopt59qYIIYLmtUHamfze2OYK170Y)

#### Python file `pcm_classes.py`:
This file contains a class that reads and edits CSV files.

#### Python file `pcm_program.py`:
This file contains the main program which in addition to its own functions and variables, uses the class in `pcm_classes.py`. 



## Libraries

To search records using "approximate match of strings", the program uses "Fuzzy String Matching" which requires the installation of `Levenshtein` and `FuzzyWuzzy`. (For details: [Levenshtein](https://pypi.org/project/python-Levenshtein/) and [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/)).

Moreover, please ensure that your Python also already contains `copy`, `datetime` and `csv`.

```python
from fuzzywuzzy import process
from copy import deepcopy
from datetime import date, datetime
from csv import DictWriter
```

## The program

![PersonalContactManager](https://drive.google.com/uc?export=view&id=1rNmsc3oOalLrbMxiHs_jriC4d1fRizWa)

Run the file `pcm_program.py`. The program performs the following tasks:

#### SEARCH:
* Search using
  * search string
  * or an ID if known
* Edit and delete the searched record
* Save the displayed record in a TXT file

#### ADD NEW RECORD:
* Add a new contact
* Add a new relation

#### VIEW RECORDS:
* Filter contacts using relations 
* Save the displayed records in a TXT file

#### VIEW BIRTHDAYS:
* Birthdays that are
  * today
  * this week
  * this month
* Save the displayed records in a TXT file



## List of functions

Below is a list of functions used in the program.

In the file `pcm_classes.py`:
* `class DataSource` to read and update CSV files using dictionaries, contains the class functions:
  * `csv_to_dictionary`, `csv_update_preparation`, `csv_add_row`, `csv_overwrite`

In the file `pcm_program.py`:
* functions for loading the database:
  * `refresh_database`, `prepare_data`
* functions used for general purposes:
  * `error_message`, `program_message`, `save_txt`
* functions for getting user inputs:
  * `get_input_nonempty`, `get_input_email`, `get_input_relation`, `get_input_new_contact`, `get_input_new_relation`
* functions for showing records:
  * `show_contact`, `show_relations`
* functions for add, edit & delete:
  * `execute_update`
* functions for search:
  * `execute_search`, `search_records`, `show_search_result`, `post_search`
* functions for brithdays:
  * `execute_birthday`, `generate_birthdays`, `show_birthdays`
* functions for views:
  * `execute_view`, `show_view`
* sub programs running in while loops:
  * `main_add`, `main_search`, `main_view`, `main_birthday`
* main program running in a while loop:
  * `main_program`



## Questions/suggestions?

Please feel free to share your feedback. Thank you very much for your collaboration! 🤜🤛
