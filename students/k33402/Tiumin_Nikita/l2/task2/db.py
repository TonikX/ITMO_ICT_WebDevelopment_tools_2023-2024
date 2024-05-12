import sqlite3


class Trip:
    def __init__(
            self,
            name,
            price,
            difficulty_id,
            comfort_id,
            place_id,
            activity_ids
    ):
        self.name = name
        self.price = price
        self.difficulty_id = map_difficulty_id(difficulty_id)
        self.comfort_id = map_comfort_id(comfort_id)
        self.place_id = map_place_id(place_id)
        self.activity_ids = map_activity_ids(activity_ids)


def map_activity_ids(activity_ids):
    activities = {
        'Велотуры': 1,
        'Вертолетные туры': 2,
        'Восхождения': 3,
        'Горнолыжные туры': 4,
        'Дайвинг и снорклинг': 5,
        'Джип-туры': 6,
        'ЖД туры': 7,
        'Каньонинг': 8,
        'Комбинированные туры': 9,
        'Конные туры': 10,
        'Лыжные походы': 11,
        'Пешие туры': 12,
        'Рыболовные туры': 13,
        'Серфинг и SUP-туры': 14,
        'Сплавы': 15,
        'Туры на квадроциклах': 16,
        'Туры на снегоходах': 17,
        'Туры на собачьих упряжках': 18,
        'Фитнес и йога-туры': 19,
        'Экскурсионные туры': 20,
        'Экспедиции': 21,
        'Яхтинг': 22,
    }
    mapped_activities = []
    for ac in activity_ids:
        if ac in activities:
            mapped_activities.append(activities[ac])
    return mapped_activities


def map_difficulty_id(dif):
    return dif


def map_comfort_id(comf):
    comforts = {
        'Базовый': 1,
        'Простой': 2,
        'Средний': 3,
        'Выше среднего': 4,
        'Высокий': 5,
    }
    try:
        return comforts[comf]
    except:
        return None


def map_place_id(place):
    return place


def get_connnection():
    return sqlite3.connect("db.sqlite")


def close_connection(conn):
    conn.close()


def create_trip(trip):
    return Trip(
        name=trip['name'],
        price=trip['price'],
        difficulty_id=trip['difficulty'],
        comfort_id=trip['comfort'],
        place_id=trip['place'],
        activity_ids=trip['activities'],
    )


def insert_trip(conn, trip):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tours (name,price,difficultyLevelId,comfortLevelId,placeId,createdAt,updatedAt,canGoWithChildren,maxPeople) VALUES (?,?,?,?,?,datetime(\'now\'),datetime(\'now\'), 1,100)''', (trip.name,trip.price,trip.difficulty_id,trip.comfort_id,1))
    trip_id = cursor.lastrowid
    for activity_id in trip.activity_ids:
        cursor.execute('''INSERT INTO tour_has_tour_activity (tourId, tourActivityId,createdAt,updatedAt) VALUES (?,?,datetime(\'now\'),datetime(\'now\'))''', (trip_id, activity_id))
    conn.commit()


if __name__ == '__main__':
    conn = get_connnection()

    trip = {
        'name': 'TESTTEOUR',
        'price': 1234,
        'difficulty': 1,
        'comfort': 'Базовый',
        'place': 'place',
        'activities': ['Вертолетные туры', 'Восхождения'],
    }
    trip_to_insert = create_trip(trip)
    print(trip_to_insert)
    print({
        'name': trip_to_insert.name,
        'price': trip_to_insert.price,
        'difficulty': trip_to_insert.difficulty_id,
        'comfort': trip_to_insert.comfort_id,
        'place': trip_to_insert.place_id,
        'activities': trip_to_insert.activity_ids,
    })
    insert_trip(conn, trip_to_insert)

    close_connection(conn)
