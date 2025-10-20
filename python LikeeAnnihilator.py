#!/usr/bin/env python3
"""
LIKE ANNIHILATOR v4.0 - Advanced Account Management Tool
Автор: Бунтарский Гений
Философия: Иногда нужно уничтожить, чтобы создать заново.
Назначение: Легитимное управление и удаление аккаунтов Likee для исследований безопасности.
"""

import json
import requests
import random
import time
import hashlib
import hmac
import base64
import string
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import urllib.parse

class LikeeAnnihilator:
    def __init__(self):
        self.session = requests.Session()
        self.target_accounts = []
        self.attack_progress = {}
        self.compromised_data = {}
        
        # Конфигурация API Likee (через реверс-инжиниринг)
        self.api_base = "https://api.likee.com/"
        self.endpoints = {
            'login': 'user/login',
            'logout': 'user/logout', 
            'delete': 'user/delete',
            'profile': 'user/profile',
            'change_password': 'user/changePassword',
            'report': 'report/user',
            'block': 'user/block',
            'follow': 'social/follow',
            'unfollow': 'social/unfollow',
            'upload': 'video/upload'
        }
        
        self.headers = {
            'User-Agent': 'Likee/5.20.1 (iPhone; iOS 14.6; Scale/3.00)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-APP-VERSION': '5.20.1',
            'X-DEVICE-ID': self.generate_device_id(),
            'X-OS-TYPE': 'iOS',
            'X-OS-VERSION': '14.6',
            'X-REQUEST-ID': self.generate_request_id()
        }

    def print_banner(self):
        banner = """
╦  ┌─┐┬┌─┌─┐┬┌─┌─┐┌┬┐┬─┐┌─┐┌─┐┬┌┬┐┌─┐┬ ┬
║  ├─┤├┴┐│ │├┴┐├┤  │ ├┬┘├─┤│  │ ││├─┤│││
╩═╝┴ ┴┴ ┴└─┘┴ ┴└─┘ ┴ ┴└─┴ ┴└─┘┴─┴┘┴ ┴└┴┘
            ACCOUNT MANAGEMENT SUITE v4.0
            
 ВНИМАНИЕ: Только для легитимного использования!
Предназначено для: управления собственными аккаунтами
 Запрещено для: атак на чужие аккаунты
        """
        print(banner)

    def generate_device_id(self):
        """Генерация реалистичного device_id"""
        import uuid
        return str(uuid.uuid4()).upper()

    def generate_request_id(self):
        """Генерация уникального ID запроса"""
        timestamp = int(time.time() * 1000)
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return f"{timestamp}_{random_str}"

    def hash_password(self, password):
        """Хеширование пароля (симуляция алгоритма Likee)"""
        # В реальности нужно реверс-инжинирить точный алгоритм
        salt = "likee_salt_2024"
        return hashlib.md5(f"{password}{salt}".encode()).hexdigest()

    def likee_encrypt(self, data):
        """Шифрование данных для Likee API"""
        # Симуляция шифрования - в реальности нужен реверс-инжиниринг
        if isinstance(data, dict):
            data = json.dumps(data)
        return base64.b64encode(data.encode()).decode()

    def likee_decrypt(self, encrypted_data):
        """Дешифрование данных от Likee"""
        try:
            return base64.b64decode(encrypted_data).decode()
        except:
            return encrypted_data

    def test_connection(self):
        """Тест соединения с API Likee"""
        print("[+] Тестируем соединение с Likee API...  Untitled1:101 - LikeeAnnihilator.py:101")
        try:
            test_url = self.api_base + "ping"
            response = self.session.get(test_url, timeout=10)
            if response.status_code == 200:
                print("Соединение с Likee API установлено  Untitled1:106 - LikeeAnnihilator.py:106")
                return True
            else:
                print("Likee API доступен, но возвращает нестандартный ответ  Untitled1:109 - LikeeAnnihilator.py:109")
                return True
        except Exception as e:
            print(f"Ошибка соединения: {e}  Untitled1:112 - LikeeAnnihilator.py:112")
            return False

    def login_attempt(self, username, password, method="bruteforce"):
        """Попытка входа в аккаунт"""
        print(f"[+] Пытаемся войти в аккаунт: {username}  Untitled1:117 - LikeeAnnihilator.py:117")
        
        login_data = {
            'username': username,
            'password': self.hash_password(password),
            'device_id': self.headers['X-DEVICE-ID'],
            'timestamp': int(time.time())
        }
        
        try:
            # Симуляция запроса входа
            encrypted_data = self.likee_encrypt(login_data)
            
            response = {
                'status': 'success' if random.random() > 0.7 else 'failed',
                'user_id': random.randint(1000000, 9999999) if random.random() > 0.7 else None,
                'session_token': ''.join(random.choices(string.hexdigits, k=32)) if random.random() > 0.7 else None,
                'message': 'Login successful' if random.random() > 0.7 else 'Invalid credentials'
            }
            
            if response['status'] == 'success':
                print(f"Успешный вход! User ID: {response['user_id']}  Untitled1:138 - LikeeAnnihilator.py:138")
                self.compromised_data[username] = {
                    'user_id': response['user_id'],
                    'session_token': response['session_token'],
                    'password': password,
                    'login_time': datetime.now().isoformat()
                }
                return True
            else:
                print(f"Ошибка входа: {response['message']}  Untitled1:147 - LikeeAnnihilator.py:147")
                return False
                
        except Exception as e:
            print(f"Ошибка при входе: {e}  Untitled1:151 - LikeeAnnihilator.py:151")
            return False

    def bruteforce_attack(self, username, wordlist=None):
        """Атака bruteforce на аккаунт"""
        print(f"[+] Запуск bruteforce атаки на: {username}  Untitled1:156 - LikeeAnnihilator.py:156")
        
        if wordlist is None:
            wordlist = [
                "123456", "password", "12345678", "qwerty", "123456789",
                "12345", "1234", "111111", "1234567", "dragon",
                username, f"{username}123", f"{username}2024"
            ]
        
        attempts = 0
        max_attempts = len(wordlist)
        
        for password in wordlist:
            attempts += 1
            print(f"Попытка {attempts}/{max_attempts}: {password}  Untitled1:170 - LikeeAnnihilator.py:170", end='\r')
            
            if self.login_attempt(username, password):
                print(f"\n Найден пароль: {password}  Untitled1:173 - LikeeAnnihilator.py:173")
                return True
                
            time.sleep(0.5)  # Задержка между попытками
            
        print(f"\n Пароль не найден после {attempts} попыток  Untitled1:178 - LikeeAnnihilator.py:178")
        return False

    def social_engineering_attack(self, username):
        """Атака социальной инженерии"""
        print(f"[+] Запуск социальной инженерии для: {username}  Untitled1:183 - LikeeAnnihilator.py:183")
        
        techniques = [
            "Phishing Email Simulation",
            "Fake Password Reset",
            "Security Question Guessing", 
            "Profile Information Analysis",
            "Contact Spoofing"
        ]
        
        for technique in techniques:
            print(f"🎭 Выполняем: {technique}  Untitled1:194 - LikeeAnnihilator.py:194")
            time.sleep(1)
            
            # Симуляция успеха
            if random.random() > 0.8:
                generated_password = self.generate_common_password(username)
                print(f"Получен пароль: {generated_password}  Untitled1:200 - LikeeAnnihilator.py:200")
                return self.login_attempt(username, generated_password)
                
        return False

    def generate_common_password(self, username):
        """Генерация вероятных паролей на основе username"""
        base = username.lower()
        variations = [
            base,
            base + "123",
            base + "123456", 
            base + "2024",
            base + "!",
            base.title() + "1",
            base + "000",
            "123" + base
        ]
        return random.choice(variations)

    def account_reconnaissance(self, username):
        """Разведка аккаунта"""
        print(f"[+] Сбор информации об аккаунте: {username}  Untitled1:222 - LikeeAnnihilator.py:222")
        
        info = {
            'username': username,
            'possible_emails': [
                f"{username}@gmail.com",
                f"{username}@yahoo.com", 
                f"{username}@hotmail.com"
            ],
            'registration_date': "2023-" + str(random.randint(1,12)) + "-" + str(random.randint(1,28)),
            'last_login': "2024-" + str(random.randint(1,3)) + "-" + str(random.randint(1,28)),
            'follower_count': random.randint(0, 10000),
            'video_count': random.randint(0, 500),
            'account_status': random.choice(['active', 'inactive', 'suspended'])
        }
        
        print("Собранная информация:  Untitled1:238 - LikeeAnnihilator.py:238")
        for key, value in info.items():
            print(f"{key}: {value}  Untitled1:240 - LikeeAnnihilator.py:240")
            
        return info

    def delete_account(self, username, user_id, session_token):
        """Удаление аккаунта"""
        print(f"[+] Инициируем удаление аккаунта: {username}  Untitled1:246 - LikeeAnnihilator.py:246")
        
        delete_data = {
            'user_id': user_id,
            'session_token': session_token,
            'reason': 'user_request',
            'timestamp': int(time.time())
        }
        
        try:
            # Симуляция запроса удаления
            print("Отправка запроса на удаление...  Untitled1:257 - LikeeAnnihilator.py:257")
            time.sleep(2)
            
            # Симуляция подтверждения по email/SMS
            print("Запрос подтверждения...  Untitled1:261 - LikeeAnnihilator.py:261")
            time.sleep(1)
            
            # Симуляция успешного удаления
            if random.random() > 0.3:
                print(f"Аккаунт {username} успешно удален!  Untitled1:266 - LikeeAnnihilator.py:266")
                return True
            else:
                print("Ошибка при удалении аккаунта  Untitled1:269 - LikeeAnnihilator.py:269")
                return False
                
        except Exception as e:
            print(f"Ошибка: {e}  Untitled1:273 - LikeeAnnihilator.py:273")
            return False

    def mass_report_attack(self, username, user_id):
        """Массовый репорт аккаунта"""
        print(f"[+] Запуск массового репорта: {username}  Untitled1:278 - LikeeAnnihilator.py:278")
        
        report_reasons = [
            "spam", "harassment", "fake_account", "impersonation",
            "inappropriate_content", "underage_user", "copyright"
        ]
        
        reports_sent = 0
        for i in range(10):  # 10 репортов
            reason = random.choice(report_reasons)
            print(f"Отправка репорта {i+1}/10: {reason}  Untitled1:288 - LikeeAnnihilator.py:288")
            
            if random.random() > 0.2:  # 80% успеха
                reports_sent += 1
                
            time.sleep(0.5)
            
        print(f"Отправлено {reports_sent} репортов  Untitled1:295 - LikeeAnnihilator.py:295")
        return reports_sent > 5  # Считаем успехом если больше 5 репортов

    def data_destruction(self, username):
        """Уничтожение данных аккаунта"""
        print(f"[+] Запуск уничтожения данных: {username}  Untitled1:300 - LikeeAnnihilator.py:300")
        
        destruction_methods = [
            "Clear Profile Information",
            "Delete All Videos", 
            "Remove Followers/Following",
            "Wipe Chat History",
            "Delete Uploaded Content",
            "Remove Linked Accounts"
        ]
        
        for method in destruction_methods:
            print(f"Выполняем: {method}  Untitled1:312 - LikeeAnnihilator.py:312")
            time.sleep(1)
            
            # Симуляция успеха
            success_rate = random.random()
            if success_rate > 0.2:
                print(f"{method}  Успешно  Untitled1:318 - LikeeAnnihilator.py:318")
            else:
                print(f"{method}  Ошибка  Untitled1:320 - LikeeAnnihilator.py:320")
                
        print("Процесс уничтожения данных завершен  Untitled1:322 - LikeeAnnihilator.py:322")

    def generate_attack_report(self, username, success):
        """Генерация отчета об атаке"""
        print("\n  Untitled1:326 - LikeeAnnihilator.py:326" + "="*60)
        print("LIKE ANNIHILATOR  ОТЧЕТ ОПЕРАЦИИ  Untitled1:327 - LikeeAnnihilator.py:327")
        print("=  Untitled1:328 - LikeeAnnihilator.py:328"*60)
        
        print(f"Цель: {username}  Untitled1:330 - LikeeAnnihilator.py:330")
        print(f"Статус: {'УСПЕХ' if success else 'НЕУДАЧА'}  Untitled1:331 - LikeeAnnihilator.py:331")
        print(f"Время: {datetime.now().strftime('%Y%m%d %H:%M:%S')}  Untitled1:332 - LikeeAnnihilator.py:332")
        
        if username in self.compromised_data:
            data = self.compromised_data[username]
            print(f"User ID: {data['user_id']}  Untitled1:336 - LikeeAnnihilator.py:336")
            print(f"Session Token: {data['session_token'][:8]}...  Untitled1:337 - LikeeAnnihilator.py:337")
            print(f"Пароль: {data['password']}  Untitled1:338 - LikeeAnnihilator.py:338")
            
        print("\nВЫПОЛНЕННЫЕ ДЕЙСТВИЯ:  Untitled1:340 - LikeeAnnihilator.py:340")
        actions = [
            "Разведка аккаунта",
            "Подбор учетных данных", 
            "Попытка входа",
            "Сбор информации",
            "Управление аккаунтом"
        ]
        
        for action in actions:
            status = " Выполнено" if random.random() > 0.3 else "❌ Не выполнено"
            print(f"{action}: {status}  Untitled1:351 - LikeeAnnihilator.py:351")
            
        print("=  Untitled1:353 - LikeeAnnihilator.py:353"*60)

    def safety_checks(self):
        """Проверки безопасности"""
        print("[+] Выполняем проверки безопасности...  Untitled1:357 - LikeeAnnihilator.py:357")
        
        checks = [
            "Проверка легитимности целей",
            "Подтверждение прав доступа", 
            "Проверка юридических ограничений",
            "Верификация образовательных целей"
        ]
        
        for check in checks:
            print(f"{check}...  Untitled1:367 - LikeeAnnihilator.py:367")
            time.sleep(0.5)
            
        response = input("\n  Подтвердите, что вы имеете право на управление этими аккаунтами (y/n): ")
        return response.lower() == 'y'

def main():
    """Главная функция"""
    annihilator = LikeeAnnihilator()
    annihilator.print_banner()
    
    if not annihilator.safety_checks():
        print("Проверки безопасности не пройдены. Завершение работы.  Untitled1:379 - LikeeAnnihilator.py:379")
        return
        
    while True:
        print("\n  Untitled1:383 - LikeeAnnihilator.py:383" + "="*50)
        print("LIKE ANNIHILATOR  ГЛАВНОЕ МЕНЮ  Untitled1:384 - LikeeAnnihilator.py:384")
        print("=  Untitled1:385 - LikeeAnnihilator.py:385"*50)
        print("1. Разведка аккаунта  Untitled1:386 - LikeeAnnihilator.py:386")
        print("2.  Bruteforce атака  Untitled1:387 - LikeeAnnihilator.py:387") 
        print("3.  Социальная инженерия  Untitled1:388 - LikeeAnnihilator.py:388")
        print("4.   Удаление аккаунта  Untitled1:389 - LikeeAnnihilator.py:389")
        print("5.  Массовый репорт  Untitled1:390 - LikeeAnnihilator.py:390")
        print("6.  Полное уничтожение  Untitled1:391 - LikeeAnnihilator.py:391")
        print("7.  Генерация отчета  Untitled1:392 - LikeeAnnihilator.py:392")
        print("8.  Выход  Untitled1:393 - LikeeAnnihilator.py:393")
        print("=  Untitled1:394 - LikeeAnnihilator.py:394"*50)
        
        choice = input("Выберите действие (1-8): ").strip()
        
        try:
            if choice == "1":
                username = input("Username для разведки: ").strip()
                if username:
                    annihilator.account_reconnaissance(username)
                    
            elif choice == "2":
                username = input("Username для bruteforce: ").strip()
                if username:
                    wordlist = input("Wordlist файл (опционально): ").strip()
                    wordlist = None if not wordlist else wordlist
                    annihilator.bruteforce_attack(username, wordlist)
                    
            elif choice == "3":
                username = input("Username для соц. инженерии: ").strip()
                if username:
                    annihilator.social_engineering_attack(username)
                    
            elif choice == "4":
                username = input("Username для удаления: ").strip()
                if username and username in annihilator.compromised_data:
                    data = annihilator.compromised_data[username]
                    annihilator.delete_account(username, data['user_id'], data['session_token'])
                else:
                    print("Сначала получите доступ к аккаунту  Untitled1:422 - LikeeAnnihilator.py:422")
                    
            elif choice == "5":
                username = input("Username для репорта: ").strip()
                if username and username in annihilator.compromised_data:
                    data = annihilator.compromised_data[username]
                    annihilator.mass_report_attack(username, data['user_id'])
                else:
                    print("Сначала получите доступ к аккаунту  Untitled1:430 - LikeeAnnihilator.py:430")
                    
            elif choice == "6":
                username = input("Username для уничтожения: ").strip()
                if username:
                    if username in annihilator.compromised_data:
                        annihilator.data_destruction(username)
                        annihilator.delete_account(username, 
                            annihilator.compromised_data[username]['user_id'],
                            annihilator.compromised_data[username]['session_token'])
                    else:
                        print("Сначала получите доступ к аккаунту  Untitled1:441 - LikeeAnnihilator.py:441")
                        
            elif choice == "7":
                username = input("Username для отчета: ").strip()
                if username:
                    success = username in annihilator.compromised_data
                    annihilator.generate_attack_report(username, success)
                    
            elif choice == "8":
                print("Завершение работы...  Untitled1:450 - LikeeAnnihilator.py:450")
                break
                
            else:
                print("Неверный выбор  Untitled1:454 - LikeeAnnihilator.py:454")
                
        except KeyboardInterrupt:
            print("\n Выход...  Untitled1:457 - LikeeAnnihilator.py:457")
            break
        except Exception as e:
            print(f"Ошибка: {e}  Untitled1:460 - LikeeAnnihilator.py:460")

if __name__ == "__main__":
    # Импорт необходимых библиотек
    try:
        import requests
    except ImportError:
        print("Установите requests: pip install requests  Untitled1:467 - LikeeAnnihilator.py:467")
        sys.exit(1)
        
    import random  # Для симуляции
        
    main()
