from pprint import pprint
import json
import requests
import time
import tqdm

for i in VKPhoto(range(10)):
    sleep(.01)

class VKPhoto:
    def __init__(self):
        self.token_Ya = input(str('Введите ваш API-token Yandex: '))
        self.token_VK = input(str('Введите ваш API-token VK: '))
        self.id = input(str('Введите ваш ID VK: '))
        self.folder = input(str('Название папки в которой будут сохранены фотографии на Яндекс.Диске: '))
        self.headers_Ya = {'Content - Type': 'application/json',
                           'Authorization': self.token_Ya}

    def list_photo(self):
        """
        Параметры album_id:
        wall — фотографии со стены;
        profile — фотографии профиля;
        saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя.
        """
        url = 'https://api.vk.com/method/photos.get'
        params = {'access_token': self.token_VK,
                  'owner_id': self.id,
                  'album_id': 'profile',
                  'extended': '1',
                  'count': '5',
                  'v': '5.131'
                 }
        res = requests.get(url, params=params).json()
        res.raise_for_status()
        if res.status_code == 201:
            pprint('Запрос отправлен на сервис VK')
        else:
            pprint('Ошибка! Проверьте правильность введенных параметров')
        res = res['response']['items']
        list_photo = []
        for photo in res:
            list_photo.append({'likes': photo['likes']['count'],
                               'url': photo['sizes'][-1]['url'],
                               'size': photo['sizes'][-1]['type'],
                               'date_upload': photo['date']})
        sort_photo = sorted(list_photo, key=lambda x: x['likes'])
        dict_photo = {}
        photo_list_1 = []
        for photo in sort_photo:
            likes = photo['likes']
            size = photo['size']
            if f'{likes}.jpg' not in list(dict_photo.keys()):
                file_name = f'{likes}.jpg'
                dict_photo[file_name] = photo['url']
            else:
                photo_1 = str(likes) + str(photo['date_upload'])
                file_name = f'{photo_1}.jpg'
                dict_photo[file_name] = photo['url']
            photo_list_1.append({'file_name': file_name, 'size': size})
        with open('VKphoto.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(photo_list_1))
        pprint('Фотографии сохранены в json-файл')
        return pprint()

    def create_a_folder(self):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": f'disk/{self.folder}'}
        response = requests.put(upload_url, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            pprint(f'Папка {self.folder} на Яндекс.Диске создана')
        else:
            pprint('Ошибка! Проверьте правильность введенных данных')
        return response.json()

    def get_upload_link(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.headers_Ya
        params = {"path": self.create_a_folder(), "overwrite": "true"}
        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def upload_YA(self):
        href = self.get_upload_link().get("href", "")
        response = requests.post(href, data=open('VKphoto.json', 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Фотографии успешно загружены")
        else:
            print('Ошибка при загрузке фотографий')


Apivk = VKPhoto()
Apivk.list_photo()
Apivk.upload_YA()
