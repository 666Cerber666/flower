<template>
    <div @click="toggleTheme" class="cursor-pointer flex items-center">
      <div :class="{'bg-gray-400': isDarkTheme, 'bg-yellow-400': !isDarkTheme}" class="relative w-10 h-4 rounded-full overflow-hidden">
        <div :class="{'translate-x-6': isDarkTheme}" class="absolute left-0.5 top-0.5 bg-white w-3 h-3 rounded-full shadow-md transform duration-300"></div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isDarkTheme: false
      };
    },
    mounted() {
      // Проверяем, есть ли в локальном хранилище информация о выбранной теме
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        this.isDarkTheme = JSON.parse(savedTheme);
      }
      // Вызываем метод, чтобы установить цвет фона body
      this.setBodyBackgroundColor();
    },
    methods: {
      toggleTheme() {
        this.isDarkTheme = !this.isDarkTheme;
        // Сохраняем выбранную тему в локальное хранилище
        localStorage.setItem('theme', JSON.stringify(this.isDarkTheme));
        // Вызываем метод, чтобы установить цвет фона body
        this.setBodyBackgroundColor();
      },
      setBodyBackgroundColor() {
        document.body.style.backgroundColor = this.isDarkTheme ? 'rgb(2 6 23)' : '#fff';
      }
    }
  };
  </script>
  
  <style>
  /* Здесь можно добавить дополнительные стили для компонента, если необходимо */
  </style>
  