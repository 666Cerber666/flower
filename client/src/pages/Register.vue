<template>
    <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company" />
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Создание аккаунта</h2>
      </div>
  
      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" @submit.prevent="registerUser">
            <div>
            <label for="username" class="block text-sm font-medium leading-6 text-gray-900">Имя пользователя</label>
            <div class="mt-2">
              <input v-model="formData.username" id="username" name="username" type="text" autocomplete="username" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Почтовый адрес</label>
            <div class="mt-2">
              <input v-model="formData.email" id="email" name="email" type="email" autocomplete="email" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
  
          <div>
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Пароль</label>
            </div>
            <div class="mt-2">
              <input v-model="formData.password" id="password" name="password" type="password" autocomplete="current-password" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
            </div>
          </div>

          <div class="text-red-500">
            {{ error_message }}
          </div>
  
          <div>
            <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">Создать</button>
          </div>
        </form>
  
        <p class="mt-10 text-center text-sm text-gray-500">
          Уже есть аккаунт?
          {{ ' ' }}
          <router-link to="/" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Войди в свой аккаунт</router-link>
        </p>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter(); // Move useRouter inside setup

const error_message = ref('');
const formData = ref({
  email: '',
  password: ''
});

const registerUser = async () => {
  try {
    const response = await axios.post('http://localhost:8000/register', formData.value);

    if (response.status >= 200 && response.status < 300) {
      console.log('Пользователь успешно зарегистрирован:', response.data);
      router.push('/');
    } else {
      console.error('Ошибка при регистрации пользователя:', response.statusText);
      error_message.value = 'Ошибка при регистрации пользователя: ' + response.statusText;
    }
  } catch (error) {
    if (error.response && error.response.status === 400 && error.response.data.detail === "Пользователь с таким email уже существует") {
      error_message.value = 'Пользователь с таким email уже существует';
    } 
    else if (error.response && error.response.status === 400 && error.response.data.detail === "Ваше имя не уникально") {
      error_message.value = 'Пользователь с таким именем уже существует';
    }
    else {
      error_message.value = 'Пользователь с таким email уже существует';
    }
  }
}
</script>
