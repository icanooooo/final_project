import requests
import random
import pytz

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

local_tz = pytz.timezone('Asia/Jakarta')

def generate_name():
    response = requests.get('https://randomuser.me/api/?nat=AU')

    if response.status_code == 200:
        user_data = response.json()['results'][0]
        full_name = f"{user_data['name']['first']} {user_data['name']['last']}"

        return full_name
    
    else:
        return f"error: {response.text}"
    
def choose_random_genre():
    genres = ['Drama', 'Science Fiction', 'Romance', 'Biography', 'Self-help', 'Japanese Manga',
              'Psychological', 'Fantasy', 'History', 'Anti Establishement', 'Action', 'Military_Fiction',
              'Adventure', 'Comedy', 'Dark Comedy', 'Crime/Mystery', 'Cyberpunk', 'Kafkaesque',
              'Asian Literature', 'Gothic Literature', 'Tutorial', 'Education', 'Game Guides']
    
    genre = random.choice(genres)

    return genre

def get_birthday():
    start_date = datetime.strptime('1950-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2010-01-01', '%Y-%m-%d')

    delta = end_date - start_date
    random_days = random.randint(0, delta.days)

    random_date = start_date + timedelta(days=random_days)

    return random_date

def generate_member_data(last_id_number): #Menerima hanya int
    data = []

    for i in range(20):
        user_data = {}
        user_data['id'] = last_id_number + 1 + i
        user_data['name'] = generate_name()
        user_data['date_of_birth'] = get_birthday()
        user_data['created_at'] = datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')
        user_data['updated_at'] = user_data['created_at']

        data.append(user_data)

    return data

def generate_book_data(last_id_number): # Hanya menerima int
    response = requests.get('https://openlibrary.org/subjects/english.json?limit=400')

    if response.status_code == 200:
        all_books = []

        for i in range (25):
            response_data = response.json()["works"][i+last_id_number]

            data = {}

            data['id'] = last_id_number + i + 1
            data['title'] = response_data['title']
            data['author_name'] = generate_name()
            data['genre'] = choose_random_genre()
            data['release_year'] = response_data['first_publish_year']
            data['stock'] = random.randint(10, 20)
            data['created_at'] = datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')
            data['updated_at'] = data['created_at']

            all_books.append(data)

        return all_books

    else:
        return f"Error: {response.text}"
    
def generate_rent_data(book_id_list, member_id_list, last_id_number): # Hanya menerima list
    rent_data = []
    
    for i in range(10):
        data = {}

        rent_day = datetime.now(ZoneInfo('Asia/Jakarta')) - timedelta(random.randint(2,4))
        return_day = datetime.now(ZoneInfo('Asia/Jakarta')) + timedelta(random.randint(2,4))

        if isinstance(book_id_list[0], list):
            book_id_list = [books[0] for books in book_id_list]

        if isinstance(member_id_list[0], list):
            member_id_list = [member[0] for member in member_id_list]

        data['id'] = len(last_id_number) + i + 1
        data['book_id'] = random.choice(book_id_list)
        data['library_member_id'] = random.choice(member_id_list)
        data['rent_date'] = rent_day.strftime('%Y-%m-%d %H:%M:%S')
        data['return_date'] = return_day.strftime('%Y-%m-%d %H:%M:%S')
        data['created_at'] = datetime.now(ZoneInfo('Asia/Jakarta')).strftime('%Y-%m-%d %H:%M:%S')
        data['updated_at'] = data['created_at']

        rent_data.append(data)

    return rent_data
