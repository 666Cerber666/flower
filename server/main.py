from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from typing import Optional
from fastapi.responses import JSONResponse
import logging
import requests
import base64
import sqlite3
from sqlite3 import Connection, Row

from sdevice_flower.flower import FlowerApi

# Создание логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Установка уровня логирования INFO

# Создание обработчика для записи логов в файл
log_file = "flower.log"
file_handler = logging.FileHandler(log_file)

# Формат записи логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)

app = FastAPI()

# Хэширование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Добавление middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE", "OPTIONS"],  # Разрешаем метод GET для вывода цветов
    allow_headers=["Content-Type"],
)

# Создание таблицы users
def create_users_table(conn: Connection):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()

# Создание таблицы flowers
def create_flowers_table(conn: Connection):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flowers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        ip TEXT,
        port TEXT,
        login TEXT,
        password TEXT,
        status TEXT DEFAULT 'disconnected' 
    )
    ''')

    conn.commit()

# Подключение к базе данных и создание пула подключений
def get_db_conn():
    conn = sqlite3.connect('flowers.db', check_same_thread=False)
    conn.row_factory = Row
    create_users_table(conn)
    create_flowers_table(conn)
    return conn

# Модель пользователя
class User(BaseModel):
    username: str
    email: str
    password: str

# Модель для хранения данных формы входа
class UserLogin(BaseModel):
    username: str
    password: str

# Модель цветка
class Flower(BaseModel):
    name: str
    ip: str
    port: str
    login: str
    password: str
    status: Optional[str]  # Сделаем поле необязательным

# Регистрация нового пользователя
@app.post('/register', response_model=User)
async def register_user(user: User, conn: Connection = Depends(get_db_conn)):
    try:
        with conn:
            cursor = conn.cursor()
            hashed_password = hash_password(user.password)
            cursor.execute('''
                INSERT INTO users (username, email, password) VALUES (?, ?, ?)
            ''', (user.username, user.email, hashed_password))
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.email" in str(e):
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
        if "UNIQUE constraint failed: users.username" in str(e):
            raise HTTPException(status_code=400, detail="Ваше имя не уникально")
        else:
            raise HTTPException(status_code=400, detail="Ошибка при регистрации пользователя")
    return user

# Аутентификация пользователя
@app.post("/login", response_model=UserLogin)
async def login_user(user: UserLogin, conn: Connection = Depends(get_db_conn)):
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users WHERE username=?
        ''', (user.username,))
        user_data = cursor.fetchone()
    if user_data:
        if verify_password(user.password, user_data['password']):
            return user  # Возвращаем модель UserLogin
    raise HTTPException(status_code=401, detail="Unauthorized")

async def check_api_connection(ip: str, port: str, login: str, password: str) -> str:
    url = f"http://{ip}:{port}"  # Формируем URL для запроса к API
    try:
        response = requests.get(url, auth=(login, password))
        if response.status_code == 200:
            return "Completed"  # Возвращаем только статус
        else:
            return "Not Completed"  # Возвращаем только статус
    except requests.RequestException:
        return "Not Completed"  # Если возникла ошибка, возвращаем только статус

# Добавление цветка
@app.post("/add_flower")
async def create_flower(flower: Flower, background_tasks: BackgroundTasks):
    async def add_flower_task(flower: Flower):
        conn = sqlite3.connect('flowers.db')
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO flowers (name, ip, port, login, password, status) VALUES (?, ?, ?, ?, ?, ?)
            ''', (flower.name, flower.ip, flower.port, flower.login, flower.password, "In Progress"))
            flower_id = cursor.lastrowid
            conn.commit()
            cursor.close()

            # Устанавливаем статус только после проверки подключения к API
            await update_flower_status(flower_id, flower.ip, flower.port, flower.login, flower.password)
        finally:
            conn.close()

    background_tasks.add_task(add_flower_task, flower)
    return {"message": "Flower addition initiated", "status": "In Progress"}


async def update_flower_status(flower_id: int, ip: str, port: str, login: str, password: str):
    try:
        # Получаем статус подключения к API
        status = await check_api_connection(ip, port, login, password)
        
        # Создаем новое соединение с базой данных
        conn = sqlite3.connect('flowers.db')
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE flowers SET status = ? WHERE id = ?
            ''', (status, flower_id))
            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        print(f"Error updating flower status: {e}")

@app.delete("/delete_flower/{flower_id}")
async def delete_flower(flower_id: int, background_tasks: BackgroundTasks):
    async def remove_flower_task(flower_id: int):
        conn = sqlite3.connect('flowers.db')
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM flowers WHERE id = ?", (flower_id,))
            conn.commit()
            cursor.close()
        finally:
            conn.close()

    background_tasks.add_task(remove_flower_task, flower_id)
    return {"message": "Flower deletion initiated", "status": "In Progress"}


@app.get("/flowers")
async def get_flowers(background_tasks: BackgroundTasks):
    try:
        conn = sqlite3.connect('flowers.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, ip, port, login, status, password FROM flowers')
        flowers_data = cursor.fetchall()
        
        flowers = []
        for flower_id, name, ip, port, login, status, password in flowers_data:
            # Update flower status
            background_tasks.add_task(update_flower_status, flower_id, ip, port, login, password)
            
            flower_dict = {
                "id": flower_id,
                "name": name,
                "ip": ip,
                "port": port,
                "login": login,
                "status": status,
                "password": password
            }
            flowers.append(flower_dict)
        return flowers
    except Exception as e:
        print(f"Error getting flowers: {e}")
        raise
    finally:
        conn.close()

async def fetch_flower_data(flower_id: int, conn: Connection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM flowers WHERE id = ?', (flower_id,))
    flower_data = cursor.fetchone()
    return flower_data

@app.get("/flowers/{flower_id}")
async def get_flower(flower_id: int, conn: Connection = Depends(get_db_conn)):
    try:
        flower_data = await fetch_flower_data(flower_id, conn)
        if flower_data:
            flower = {
                "id": flower_data["id"],
                "name": flower_data["name"],
                "ip": flower_data["ip"],
                "port": flower_data["port"],
                "login": flower_data["login"],
                "password": flower_data["password"]
            }
            
            return flower
        else:
            raise HTTPException(status_code=404, detail="Flower not found")
    except Exception as e:
        print(f"Error getting flower: {e}")
        raise
    finally:
        conn.close()

@app.get("/tasks")
async def get_tasks(flower_id: int, flower_data: dict = Depends(get_flower)):
    try:
        api = FlowerApi(flower_data['login'], flower_data['password'], flower_data['ip'], flower_data['port'])
        tasks = api.get_tasks()  # Подставьте вашу функцию получения задач
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise

