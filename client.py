import requests

# Создаем пользователя
# user_response = requests.post(
#     "http://127.0.0.1:5000/api/v1/user",
#     json={
#         "username": "test_user",
#         "password": "password"
#     }
# )
# print(f"user response: {user_response.status_code}, {user_response.json()}")

# Получаем пользователя
# response = requests.get(
#     "http://127.0.0.1:5000/api/v1/user/1")
#
# print(f"user response: {response.status_code}, {response.text}")

# Создаем объявление (предполагаем, что id = 1)
# response = requests.post(
#     "http://127.0.0.1:5000/api/v1/announcement",
#     json={
#         "title": "Суп",
#         "description": "Вкусный",
#         "owner": 1
#     }
# )
# print(f"announcement response: {response.status_code}, {response.json()}")

# Получаем объявление
# response = requests.get(
#     "http://127.0.0.1:5000/api/v1/announcement/2"
# )
#
# print(f"announcement response: {response.status_code}, {response.json()}")

# Удаляем объявление
# response = requests.delete(
#     "http://127.0.0.1:5000/api/v1/announcement/1"
# )
# print(f"announcement response: {response.status_code}, {response.text}")

# Изменяем объявление
# response = requests.patch(
#     "http://127.0.0.1:5000/api/v1/announcement/2",
#     json={
#         "title": "Суп",
#         "description": "Слишком Вкусный!!!",
#         "owner": 1
#     }
# )
#
# print(f"announcement response: {response.status_code}, {response.json()}")