import string
import random
from faker import Factory
from random import randint
import datetime
import pandas as pd

fake = Factory.create()

def get_indian_males():
    gender_names = []
    with open('indian_male.txt') as f:
        names = f.readlines()
    for name in names:
        gender_names.append(name.replace('\n', ''))
    return gender_names

def get_indian_females():
    gender_names = []
    with open('indian_female.txt') as f:
        names = f.readlines()
    for name in names:
        gender_names.append(name.replace('\n', ''))
    return gender_names

indian_males = get_indian_males()
indian_females = get_indian_females()

def get_indian_name(gender, indian_males, indian_females):
    if gender.lower() == 'm':
        return random.choice(indian_males)
    else:
        return random.choice(indian_females)

def get_middle_initials():
    return random.choice(string.ascii_letters).upper()

def get_city(address):
    if '\n' in address and ',' in address:
        return address.split('\n')[1].split(',')[0]
    return ''

def get_ethnicity():
    ethnicities = ['Asian', 'Latino', 'Hispanic', 'Indian', 'African', 'American', 'White', 'Pacific', 'Islander', 'Alaska', 'Native']
    return random.choice(ethnicities)

def get_state_zip(address):
    if '\n' in address and ',' in address and 'APO' not in address:
        if len(address.split('\n')[1].split())>2:
           return address.split('\n')[1].split(',')[1].strip().split()[0], address.split('\n')[1].split(',')[1].strip().split()[1]
        return '', ''
    return '', ''

def get_preferred_communication():
    comm = ['Cell Phone', 'Land Line', 'Email', 'Mail']
    return random.choice(comm)

def get_maritalstatus():
    maritalstatus = ['Married', 'Single', 'Divorced', 'Widowed']
    return random.choice(maritalstatus)

def get_suffix(gender):
    male_suffix = ['Dr.', 'Mr.']
    female_suffix = ['Dr.', 'Mrs.', 'Miss']
    if gender == 'M':
        return random.choice(male_suffix)
    elif gender == 'F':
        return random.choice(female_suffix)
    else:
        return ''

def get_id():
    return str(randint(100000, 999999))

def get_address_line1(address):
    return address.split('\n')[0]

def get_driverlicense():
    return random.choice(string.ascii_letters).upper() + str(randint(1000000, 9999999))

def get_ssn():
    return str(randint(100, 999)) + "-" + str(randint(10, 99)) + "-" + str(randint(1000, 9999))

def get_deceased_flag(dob):
    deceasedyear = [2018, 2017, 2016]
    if dob.day<28:
        death_date = datetime.date(year = random.choice(deceasedyear), month = dob.month, day = dob.day)
    else:
        death_date = datetime.date(year=random.choice(deceasedyear), month=dob.month, day=28)
    deceasedstatus = ['Y', 'N', 'N', 'N', 'N', 'N']
    deceased_flag = random.choice(deceasedstatus)
    if deceased_flag == 'Y':
        if dob.day < 28:
            dob = datetime.date(dob.year - 5, dob.month, dob.day)
        else:
            dob = datetime.date(dob.year - 5, dob.month, 25)
        return deceased_flag, death_date, dob
    return deceased_flag, '', dob

def gen_phone():
    first = str(random.randint(100,999))
    second = str(random.randint(1,888)).zfill(3)
    last = (str(random.randint(1,9998)).zfill(4))
    while last in ['1111','2222','3333','4444','5555','6666','7777','8888']:
        last = (str(random.randint(1,9998)).zfill(4))
    return '{}-{}-{}'.format(first,second, last)

def generate_records(gender, race_type = 'non-indian'):
    person = fake.simple_profile(sex=gender)
    record = ''
    id = get_id()
    city = ''
    state = ''
    zip = ''
    if ' AE ' not in person['address']:
        email = person['mail']
        middle_name = get_middle_initials()
        if race_type == 'indian':
            name = get_indian_name(gender, indian_males, indian_females)
            print("name:", name)
            first_name = name.split()[0]
            last_name = name.split()[1]
        else:
            name = person['name']
            first_name = person['name'].split()[0]
            last_name = ""
        sex = person['sex']
        city = get_city(person['address'])
        state, zip = get_state_zip(person['address'])
        country = "USA"
        if len(name.split())==2:
            name = ' '.join([name.split()[0], middle_name, name.split()[1]])
        address_line1 = get_address_line1(person['address'])
        dob = person['birthdate']
        driverlicense = get_driverlicense()
        martial_status = get_maritalstatus()
        suffix = get_suffix(sex)
        phone_cell = gen_phone()
        phone_fax = gen_phone()
        phone_home = gen_phone()
        ssn = get_ssn()
        preferred_communication = get_preferred_communication()
        ethnicity = get_ethnicity()
        if len(person['name'].split()) > 1 and race_type != 'indian':
            last_name = person['name'].split()[len(person['name'].split()) - 1]

        deceased_flag, death_date, dob = get_deceased_flag(dob)
        if state != '':
            record = id + "|" + name + "|" + first_name + "|" + middle_name + "|" + last_name + "|" + suffix + "|" + martial_status + "|" + preferred_communication + "|" + ethnicity + "|" + email+ "|" + sex + "|"+ address_line1 + "|" + city + "|" + state +"|" + zip + "|" + country + "|" + driverlicense + "|" + str(dob) + "|" + deceased_flag + "|" + str(death_date) + "|" + phone_cell + "|" + phone_fax + "|" + phone_home + "|" + ssn
    return record, city, state, zip

def create_call_record(id):
    attempted_datetime_random = random.choice(attempted_datetime)
    attempted_datetime_random = attempted_datetime_random.replace('2019', random.choice(['2018', '2019']))
    attempted_datetime_day = attempted_datetime_random[attempted_datetime_random.rfind('-'):attempted_datetime_random.index(' ')]
    attempted_datetime_random = attempted_datetime_random.replace(attempted_datetime_day, random.choice(['-01', '-02', '-03', '-04', '-05', '-06', '-07', '-08', '-09', '-10', '-11', '-12']))
    attempted_datetime_sec = attempted_datetime_random[attempted_datetime_random.rfind(':'):]
    attempted_datetime_random = attempted_datetime_random.replace(attempted_datetime_sec, ":" + str(random.choice(range(10, 59))))
    phone_source_random = random.choice(phone_source)
    call_result_random = random.choice(call_result)
    phone_type_random = random.choice(phone_type)
    record = str(id) + "|" + phone_type_random + "|" + phone_source_random + "|" + call_result_random + "|" + str(attempted_datetime_random)
    return record

def is_excluded_location(locations, city, state, zip):
    if city.lower() in locations or state.lower() in locations or zip.lower() in locations:
        return True
    else:
        return False

def get_anon_data(rows, male_per = 0.5, exclude_locations = [], race_type = 'non-indian'):
    header = "id|name|first_name|middle_name|last_name|suffix|martial_status|preferred_communication|ethnicity|email|sex|address_line1|city|state|zip|country|driverlicense|dob|deceased_flag|death_date|phone_cell|phone_fax|phone_home|ssn"
    ids_generated = []
    male_rows = (int)(male_per * rows)
    female_rows = rows - male_rows
    records = {}
    count = 0
    data = []
    while (count != male_rows):
        male_record, city, state, zip = generate_records('M', race_type)
        if male_record != '' and not is_excluded_location(exclude_locations, city, state, zip):
            data.append(male_record)
            count = count + 1
    records["male_n"]  = count
    count = 0
    while (count != female_rows):
        female_record, city, state, zip = generate_records('F', race_type)
        if female_record != '' and not is_excluded_location(exclude_locations, city, state, zip):
            data.append(female_record)
            count = count + 1
    records["female_n"] = count
    records["data"] = data
    records["delimiter"] = "|"
    records["exclusion"] = exclude_locations
    return records
