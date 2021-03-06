'''---------------------------------
PERSONAL CONTACT MANAGER (PCM)
THIS FILE CONTAINS - THE MAIN PROGRAM
---------------------------------'''

from pcm_classes import DataSource
from copy import deepcopy
from fuzzywuzzy import process
from datetime import date, datetime


'''---------------------------------
FUNCTIONS FOR LOADING DATABASE
---------------------------------'''

def refresh_database() -> None:
    '''use class to read contacts and relations files, and use function to merge into 1 dictionary
    DECLARING GLOBAL VARIABLES HERE TOO !!! WATCH OUT !!!
    '''
    global class_contacts, class_relations, data_contacts, data_relations, data_compiled

    class_contacts = DataSource('contacts',
                                'tbContacts.csv',
                                ['FullName', 'NickName', 'RelationID', 'Phone', 'Email', 'Address', 'Birthday'],
                                'FullName')

    class_relations = DataSource('relations',
                                 'tbRelations.csv',
                                 ['RelationID', 'Relation'],
                                 'Relation')

    data_contacts = class_contacts.csv_to_dictionary()
    data_relations = class_relations.csv_to_dictionary()
    data_compiled = prepare_data(data_contacts, data_relations)


def prepare_data(dict_contacts: dict, dict_relations: dict) -> dict:
    '''Merge Contacts and Relation (2 dictionaries generated by class) to one dictionary,
     and add extra columns'''
    dict_compiled = deepcopy(dict_contacts)

    today = date.today()
    current_year = today.year

    for each in dict_compiled.values():
        bday_string = each['Birthday']
        bday_day, bday_month, bday_week, age = 0, 0, 0, 0

        if bday_string:
            bday_date = datetime.strptime(bday_string, '%d.%m.%Y')
            bday_day = bday_date.day
            bday_week = datetime.strftime(bday_date, "%V")
            bday_month = bday_date.month
            bday_year = bday_date.year
            age = current_year - bday_year

        each['BirthDate'] = int(bday_day)
        each['BirthWeek'] = int(bday_week)
        each['BirthMonth'] = int(bday_month)
        each['Age'] = int(age)

        if each['NickName'] == '':
            each['Name'] = each['FullName'].upper()
        else:
            each['Name'] = each['FullName'].upper() + ' a.k.a. ' + each['NickName'].upper()

        relation_id = each['RelationID']
        for r in dict_relations.values():
            if r['RelationID'] == relation_id:
                each['Relation'] = r['Relation']

    return dict_compiled


'''---------------------------------
FUNCTIONS FOR GENERAL PURPOSES
---------------------------------'''

def error_message(message: str='INVALID ENTRY') -> None:
    '''show error messages'''
    print('-------')
    print(f'>> {message}. TRY AGAIN.')


def program_message(message: str='INPUT ACCEPTED') -> None:
    '''show success messages'''
    print('-------')
    print(f'>> {message}.')


def save_txt(title: str, body: str) -> None:
    '''create a txt file. get title (part of file name) and text body from elsewhere'''
    user_input = str(input(('Enter\n SAVE to generate a TXT file in hard drive'
                            '\n ANY KEY to continue: '))).lower()
    if user_input == 'save':
        current_time = datetime.now().strftime("%Y.%m.%d %H.%M.%S")
        file_name = f"PCM {title} {current_time}.txt"
        with open(file_name, "w", encoding='utf-8') as file:
            file.write(body)
        program_message('TXT FILE SAVED IN HARD DRIVE')
    else:
        program_message('NO ACTION TAKEN')


'''---------------------------------
FUNCTIONS FOR GETTING USER INPUTS
---------------------------------'''

def get_input_nonempty(string: str) -> str:
    '''Get user input (blank NOT allowed), return as string'''
    user_input = str(input((f'Enter {string}: ')))
    while not user_input:
        program_message('This is a compulsory field')
        user_input = str(input((f'Enter {string}: ')))
    return user_input


def get_input_email() -> str:
    '''Get user input aka EMAIL (non blank checks for @ and .), return as string'''
    email = str(input(("Enter EMAIL: ")))
    email_characters = ['@', '.']
    while email != '':
        for character in email_characters:
            if character not in email:
                error_message(f'\'{character}\' missing. Input not accepted')
                email = ''
                break
        email = str(input(("Enter EMAIL: ")))
    return email.lower()


def get_input_relation() -> str:
    '''Ask user to choose relation by entering Relation ID'''
    show_relations(data_relations)
    while True:
        relation_id = get_input_nonempty('RELATION ID (from above)')
        try:
            check = data_relations[int(relation_id)].get('RelationID')
            break
        except (ValueError, KeyError):
            relation_id = ''
            error_message()
    return relation_id


def get_input_new_contact() -> list:
    '''to add/edit contacts, ask user to enter data for all fields'''
    full_name = get_input_nonempty('FULL NAME').title()
    nick_name = str(input(("Enter NICK NAME: "))).title()
    phone = str(input(("Enter PHONE (include codes): ")))
    email = get_input_email()
    address = str(input(("Enter ADDRESS: "))).title()
    birthday = str(input(("Enter BIRTHDAY (dd.mm.yyy): ")))
    relation_id = get_input_relation()
    return [full_name, nick_name, relation_id, phone, email, address, birthday]


def get_input_new_relation() -> list:
    '''to add/edit relations, ask user to enter data for all fields'''
    relation_ID = str(next(reversed(data_relations.keys())) + 1)
    relation = get_input_nonempty('RELATION').title()
    return [relation_ID, relation]


'''---------------------------------
FUNCTIONS FOR SHOWING RECORDS
---------------------------------'''

def show_contact(data_source: dict, record_number: int):
    '''Show individual contact data in a presentable manner'''

    name = data_source[record_number].get('Name', '--')
    phone = data_source[record_number].get('Phone', '--')
    email = data_source[record_number].get('Email', '--')
    address = data_source[record_number].get('Address', '--')
    birthday = data_source[record_number].get('Birthday', '--')
    relation = data_source[record_number].get('Relation', '--')

    output_string = '\t-------'
    if record_number == 99999:
        output_string += f'\n\t>> Record:\t\t{name}'
    else:
        output_string += f'\n\t>> Record {record_number}:\t{name}'
    output_string += f'\n\t\t\t\t\tRelation: {relation}' \
                     f'\n\t\t\t\t\tPhone:    {phone}' \
                     f'\n\t\t\t\t\tEmail:    {email}' \
                     f'\n\t\t\t\t\tAddress:  {address}' \
                     f'\n\t\t\t\t\tBirthday: {birthday}' \
                     f'\n\t-------'

    return record_number, output_string


def show_relations(data_source: dict) -> None:
    '''Show relations data in a presentable manner'''
    print('\t-------')
    print('\tRELATIONS')
    for value in data_source.values():
        print('\t' + value['RelationID'] + ': ' + value['Relation'])
    print('\t-------')


'''---------------------------------
FUNCTIONS FOR ADD, EDIT & DELETE
---------------------------------'''

def execute_update(update_type: str, action: str, id: int=99999) -> None:
    '''based on user selection, prepare the data, and use class functions to modify CSVs'''
    actions = {
        '1': {'class': class_contacts, 'input': get_input_new_contact, 'title': 'CONTACT'},
        '2': {'class': class_relations, 'input': get_input_new_relation, 'title': 'RELATION'},
    }

    try:
        if update_type == 'add new' or update_type == 'edit':
            print(f"-------\n>> {update_type.upper()} {actions[action].get('title')}")

            input_fields = actions[action].get('input')()
            record = actions[action].get('class').csv_update_preparation(input_fields)

            x = {id: actions[action].get('class').csv_update_preparation(input_fields)}
            if action == '1':
                x = prepare_data(x, data_relations)
                record_number, string = show_contact(x, id)
                print(string)
            else:
                show_relations(x)

        user_input = str(input(('Enter'
                                '\n SAVE to save changes'
                                '\n ANY KEY to continue withtout saving: '))).lower()
        if user_input == 'save':
            if update_type == 'add new':
                actions[action].get('class').csv_add_row(record)

            elif update_type == 'edit':
                data_contacts[id] = record
                actions[action].get('class').csv_overwrite(data_contacts)

            elif update_type == 'delete':
                del data_contacts[id]
                actions[action].get('class').csv_overwrite(data_contacts)

            refresh_database()
            program_message('DATABASE UPDATED')

        else:
            program_message('NOT SAVED')

    except (TypeError, KeyError):
        error_message()


'''---------------------------------
FUNCTIONS FOR SEARCH
---------------------------------'''

def execute_search(user_input: str) -> None:
    '''based on  user input,  either directly show requested record or conduct search'''
    try:
        if user_input == '':
            error_message()
        elif 'show' in user_input:
            x = int(user_input[4:])
            if x is False:
                record_number, string = show_contact(data_compiled, int(user_input.split(' ')[1]))
                print(string)
                post_search(record_number, string)
            else:
                record_number, string = show_contact(data_compiled, x)
                print(string)
                post_search(record_number, string)
        else:
            search_records(user_input, 'Name')
    except (ValueError, KeyError):
        error_message()


def search_records(search_string: str, field: str) -> None:
    '''Go through saved dictionary to find matching names (full name + nickname) @65% match'''
    search_list = []

    for index, person in data_compiled.items():
        text = (str(index) + ': ' + person[field])
        search_list.append(text)

    matches = process.extract(search_string.upper(), search_list, limit=20)
    search_result = []

    for match in matches:
        if match[1] >= 65:
            search_result.append(match[0])

    count = len(search_result)
    show_search_result(count, search_result)


def show_search_result(count, search_result) -> None:
    '''Show the matching records as a list'''
    print('-------')
    print(f'>> {count} SIMILAR RECORD(S) FOUND')
    if count == 0:
        pass
    else:
        print(f'>> {search_result}')


def post_search(record_number: int, string: str) -> None:
    '''after showing result, ask user if wants to save it, edit it, or delete it, or nothing.'''
    user_input = str(input(('Enter'
                            '\n SAVE to save in a TXT file'
                            '\n EDIT to edit record'
                            '\n DELETE to delete record'
                            '\n ANY KEY to continue: '))).lower()
    if user_input == 'save':
        save_txt('Search Result', string)
    elif user_input == 'edit':
        execute_update(user_input, '1', record_number)
    elif user_input == 'delete':
        execute_update(user_input, '1', record_number)
    else:
        program_message('NO ACTION TAKEN')


'''---------------------------------
FUNCTIONS FOR BIRTHDAYS
---------------------------------'''

def execute_birthday(user_input: str) -> None:
    '''execute necessary action based on user input'''
    today = date.today()
    current_day = today.strftime('%d.%m.%Y')
    current_week = datetime.strftime(today, "%V")
    current_month = today.month
    actions = {
        '1': {'filter': 'Birthday', 'threshold': current_day, 'title': f'TODAY ({current_day})', },
        '2': {'filter': 'BirthWeek', 'threshold': current_week, 'title': f'THIS WEEK (w{current_week})', },
        '3': {'filter': 'BirthMonth', 'threshold': current_month, 'title': f'THIS MONTH (m{current_month})', },
        '4': {},
    }
    try:
        filter = actions[user_input].get('filter')
        threshold = actions[user_input].get('threshold')
        title = actions[user_input].get('title')

        birthday_dict = generate_birthdays(filter, threshold)
        if len(birthday_dict) > 0:
            birthday_string = show_birthdays(birthday_dict, title)
            print(birthday_string)
            save_txt('Birthdays', birthday_string)
        else:
            program_message(f'NO BIRTHDAYS {title}')
    except (TypeError, KeyError):
        error_message()


def generate_birthdays(filter: str, threshold: int) -> dict:
    '''based on user filter, generate a DICTIONARY of contacts with birthdays'''
    bday_dict = {}
    i = 1
    for each in data_compiled.values():
        if each[filter] == threshold:
            bday_dict[i] = {
                'BirthDate': each['BirthDate'],
                'Birthday': each['Birthday'],
                'Name': each['Name'],
                'Age': each['Age'],
                'Relation': each['Relation'],
                'Phone': each['Phone'],
                'Email': each['Email'],}
        i += 1
    return dict(sorted(bday_dict.items(), key=lambda element: element[1]['BirthDate']))


def show_birthdays(bday_dict: dict, title: str) -> str:
    '''Prepare data in a presentable manner - into a string'''
    joined_string = f"\t-------\n\tBIRTHDAYS {title}"
    for each in bday_dict.values():
        joined_string += f"\n\t{each['Birthday']}" \
                         f"\t{each['Name']}" \
                         f" -- turning {each['Age']} ({each['Relation']})"
    joined_string += f"\n\t-------"
    return joined_string


'''---------------------------------
FUNCTIONS FOR VIEWS
---------------------------------'''

def execute_view() -> None:
    '''execute necessary action based on user input'''
    r_id = get_input_relation()
    r_text = data_relations[int(r_id)].get('Relation')
    filtered_dict = {}
    i = 1
    for key, value in data_compiled.items():
        if value['RelationID'] == r_id:
            filtered_dict[i] = value
            i += 1
    output = show_view(r_text, dict(sorted(filtered_dict.items(), key=lambda element: element[1]['Name'])))
    print(output)
    save_txt('Filtered Contacts', output)


def show_view(title: str, filtered_data: dict) -> str:
    '''Prepare data in a presentable manner - into a string'''
    joined_string = f"\t-------\n\tCONTACT LIST: {title.upper()}"
    for each in filtered_data.values():
        joined_string += f"\n\t  {each['Name']}" \
                         f"\n\t\t\tBDay: {each['Birthday']}, Tel: {each['Phone']}, Email: {each['Email']}, Address: {each['Address']}"
    joined_string += f"\n\t-------"
    return joined_string


'''---------------------------------
SUB PROGRAMS
---------------------------------'''

def main_add() -> None:
    '''THE ADD PROGRAM'''
    while True:
        refresh_database()
        print('***************')
        user_input = str(input(('ADD NEW RECORD\nEnter'
                                '\n 1 to add CONTACT'
                                '\n 2 to add RELATION'
                                '\n or QUIT to quit: '))).lower()
        try:
            actions = {
                '1': '1',
                '2': '2',
            }
            if 'quit' in user_input:
                break
            else:
                execute_update('add new', actions.get(user_input))
        except (TypeError, KeyError):
            error_message()
    program_message('ADD RECORD CLOSED')


def main_search() -> None:
    '''THE SEARCH PROGRAM'''
    while True:
        refresh_database()
        print('***************')
        user_input = str(input('SEARCH CONTACTS\nEnter'
                               '\n SHOW <ID> to see record'
                               '\n <SEARCH TEXT> to search'
                               '\n or QUIT to quit: ')).lower()
        if 'quit' in user_input:
            break
        else:
            execute_search(user_input)
    program_message('SEARCH CLOSED')


def main_view() -> None:
    '''THE VIEW PROGRAM'''
    while True:
        refresh_database()
        print('***************')
        user_input = str(input('VIEW CONTACTS SORTED BY RELATION\nEnter'
                               '\n ANY KEY to continue'
                               '\n or QUIT to quit: ')).lower()
        if 'quit' in user_input:
            break
        else:
            execute_view()
    program_message('VIEWS CLOSED')


def main_birthday() -> None:
    '''THE BIRTHDAY PROGRAM'''
    while True:
        refresh_database()
        print('***************')
        user_input = str(input('VIEW BIRTHDAYS\nEnter'
                               '\n 1 to see birthdays TODAY'
                               '\n 2 to see birthdays THIS WEEK'
                               '\n 3 to see birthdays THIS MONTH'
                               #'\n 4 to see birthdays OTHER MONTH'
                               '\n or QUIT to quit: ')).lower()
        if 'quit' in user_input:
            break
        else:
            execute_birthday(user_input)
    program_message('BIRTHDAYS CLOSED')


def main_program() -> None:
    '''THE MAIN PROGRAM in a while loop'''
    while True:
        refresh_database()
        print('****************************************')
        print('PERSONAL CONTACT MANAGER - Trial Version')
        print('****************************************')
        user_input = str(input(('Enter'
                                '\n 1 to SEARCH'
                                '\n 2 to ADD NEW RECORD'
                                '\n 3 to VIEW RECORDS'
                                '\n 4 to VIEW BIRTHDAYS'
                                '\n or QUIT to quit: ')))
        try:
            actions = {
                '1': main_search,
                '2': main_add,
                '3': main_view,
                '4': main_birthday,
            }
            if 'quit' in user_input:
                program_message('PROGRAM TERMINATED')
                break
            else:
                actions.get(user_input)()
        except (TypeError, KeyError):
            error_message()


'''---------------------------------
MAIN PROGRAM
---------------------------------'''

main_program()


'''---------------------------------
THE END
---------------------------------'''