import axios, { AxiosResponse } from 'axios';

const baseURL = 'http://localhost:8000/';

interface Flower {
  id: number;
  name: string;
  ip: string;
  port: string;
  login: string;
  status: string;
  password: string;
}

export const fetchFlowers = async (): Promise<Flower[]> => {
  try {
    const response: AxiosResponse<Flower[]> = await axios.get(`${baseURL}flowers`);
    return response.data;
  } catch (error) {
    console.error('Error fetching flowers:', error);
    throw error;
  }
};

export const addFlower = async (flower: Flower): Promise<Flower> => {
  try {
    const response: AxiosResponse<Flower> = await axios.post(`${baseURL}add_flower`, flower);
    return response.data;
  } catch (error) {
    console.error('Error adding flower:', error);
    throw error; // Добавьте эту строку, чтобы пробросить ошибку выше
  }
};


export const deleteFlower = async (flowerId: string): Promise<void> => {
  try {
    const response: AxiosResponse<void> = await axios.delete(`${baseURL}delete_flower/${flowerId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting flower:', error);
    throw error;
  }
};

export const fetchFlower = async (flowerId: string) => {
  let flowerData; // переместили объявление сюда

  try {
    const flowerResponse = await axios.get(`${baseURL}flowers/${flowerId}`);
    flowerData = flowerResponse.data; // присвоили значение здесь
    return flowerData; // возвращаем flowerData
  } catch (error) {
    console.error('Error fetching flower tasks:', error);
    throw error;
  }
};

export const fetchFlowerTasks = async (flowerId: string) => {
  try {
    // Выполняем запрос к серверу для получения задач
    const response = await axios.get(`${baseURL}tasks?flower_id=${flowerId}`, {
    });

    // Проверяем успешность запроса
    if (response.status === 200) {
      // Возвращаем данные о задачах
      return response.data;
    } else {
      // Если запрос не успешен, возвращаем пустой массив задач
      return [];
    }
  } catch (error) {
    console.error('Error fetching flower tasks:', error);
    throw error;
  }
};


