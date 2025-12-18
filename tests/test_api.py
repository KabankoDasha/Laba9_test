import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


class TestJsonPlaceholderAPI:
    
    def test_get_post(self):
        """Тест GET-запроса для получения поста"""
        response = requests.get(f"{BASE_URL}/1")
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        assert 'id' in data
        assert 'title' in data
        assert 'body' in data
        assert 'userId' in data
        
        assert data['id'] == 1
        assert data['userId'] == 1
    
    def test_create_post(self):
        """Тест POST-запроса для создания поста"""
        new_post = {
            "title": "Test Post",
            "body": "This is test content",
            "userId": 1
        }
        
        response = requests.post(BASE_URL, json=new_post)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"
        
        data = response.json()
        assert data['title'] == new_post['title']
        assert data['body'] == new_post['body']
        assert data['userId'] == new_post['userId']
        assert data['id'] == 101
    
    def test_update_post(self):
        """Тест PUT-запроса для обновления поста"""
        updated_post = {
            "id": 1,
            "title": "Updated Title",
            "body": "Updated content",
            "userId": 1
        }
        
        response = requests.put(f"{BASE_URL}/1", json=updated_post)
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        data = response.json()
        assert data['title'] == updated_post['title']
        assert data['body'] == updated_post['body']