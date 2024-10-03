

# База данных задач
temp_db = {
    "task":[
        {
            "id": 1,
            "title": "ДЗ1",
            "description": "Сделать дз1",
            "dueTo": "2021-12-31",
            "priority_id": 1,
            "tags":[
                {
                    "id": 1,
                    "name": "Спорт"
                },
                {
                    "id": 2,
                    "name": "Обучение"
                }
            ]
        },
        {
            "id": 2,
            "title": "ДЗ2",
            "description": "Сделать дз2",
            "dueTo": "2022-12-31",
            "priority_id": 2,
            "tags":[
                {
                    "id": 2,
                    "name": "Обучение"
                }
            ]
        }
    ],
    "priority": [
        {
            "id": 1,
            "name": "Срочно"
        },
        {
            "id": 2,
            "name": "Несрочно"
        }
    ]
}
