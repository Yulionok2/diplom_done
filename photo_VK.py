import json
import requests
import os
import time
from tqdm import tqdm

class VKPhoto:
  def __init__(self):
    self.token_VK = input(str('Введите ваш API-token VK: '))
    self.id = input(str('Введите ваш ID VK: '))
    self.token_Ya = input(str('Введите ваш API-token Yandex: '))
    self.file_path = input(str('Названиее папки в котрой будут фото: '))

  def creating_a_directory(self):
    os.mkdir(self.file_path)

  def _get_photos_from_folder(self) -> list:
    file_list = os.listdir(self.file_path)
    return file_list

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
    response = requests.get(url, params=params).json()
    list_photo = response["response"]["items"]
    for file in tqdm(list_photo):
      time.sleep(3)
      self.size = file['sizes'][-1]['type']
      photo_url = file['sizes'][-1]['url']
      file_name = file['likes']['count']
      download_photo = requests.get(photo_url)
      with open(f'{self.file_path}/{file_name}.jpg', 'wb') as f:
        f.write(download_photo.content)

  def create_a_folder(self):
    upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
    headers = {'Content-Type': 'application/json',
            'Authorization': self.token_Ya}
    params = {"path": self.file_path}
    response = requests.put(upload_url, headers = headers, params=params)
  
  def photos_upload(self):
    headers = {'Content-Type': 'application/json',
            'Authorization': self.token_Ya
            }
    log_list = []
    for photo in tqdm(self._get_photos_from_folder()):
      time.sleep(3)
      url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
      params = {'path': f'{self.file_path}/{photo}'}
      get_upload_url = requests.get(url, headers=headers, params=params)
      get_url = get_upload_url.json()
      upload_url = get_url['href']
      file_upload = requests.put(upload_url, data=open(f'{self.file_path}/{photo}', 'rb'), headers=headers)
      status = file_upload.status_code

      download_log = {'file_name': photo, 'size': self.size}
      log_list.append(download_log)

    with open('VKphoto.json', 'a') as file:
      json.dump(log_list, file, indent=2)
    if 500 > status != 400:
      print('Фотографии успешно загружены!')
    else:
      print('Ошибка при загрузке фотографий')


Apivk = VKPhoto()
Apivk.creating_a_directory()
Apivk._get_photos_from_folder()
Apivk.list_photo()
Apivk.create_a_folder()
Apivk.photos_upload()
