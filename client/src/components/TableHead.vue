<template>
  <div class="flex flex-col sm:flex-row justify-between items-center mb-4">
    <div class="relative mb-2">
      <label for="items-per-page">Количество элементов:</label>
      <input
        id="items-per-page"
        :value="selectedItem"
        @input="updateSelectedItem($event.target.value)"
        @focus="isOpen = true"
        @blur="isOpen = false"
        class="input-field w-24 sm:w-32 text-center py-2 rounded-md border border-gray-300 appearance-none transition duration-300 ease-in-out cursor-pointer"
      />
      <transition name="slide-fade">
        <ul
          v-if="isOpen"
          class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded shadow-md pointer-events-auto z-10"
        >
          <li
            v-for="option in options"
            :key="option.value"
            @click="selectItem(option.value)"
            class="cursor-pointer hover:bg-gray-100 rounded px-2 py-1"
          >{{ option.label }}</li>
        </ul>
      </transition>
    </div>

    <div class="relative w-full sm:w-auto rounded">
      <input
        type="text"
        :value="searchQuery"
        @input="updateSearchQuery($event.target.value)"
        @focus="isInputFocused = true"
        @blur="isInputFocused = false"
        placeholder="Поиск..."
        class="input-field px-2 py-1 border border-gray-300 rounded-md rounded-l-none pr-8 w-full sm:w-64 shadow-md transition-shadow transition-colors duration-300 focus:outline-none focus:border-gray-100 focus:bg-gray-100 focus:shadow-lg"
      />
      <div class="cursor" v-if="isInputFocused" :style="{ left: cursorPosition + 'px' }"></div>
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="absolute right-2 top-5 transform -translate-y-1/2 h-6 w-6 text-gray-400"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l5-5m0 0l-5-5m5 5H4"/>
      </svg>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['update:selectedItem', 'update:searchQuery']);

const isInputFocused = ref(false);
const cursorPosition = ref(0);
const isOpen = ref(false);
const options = [
  { value: '10', label: '10' },
  { value: '15', label: '15' },
  { value: '25', label: '25' },
];

const selectedItem = ref('10');

const updateSelectedItem = (newValue) => {
  selectedItem.value = newValue; // Обновляем значение локальной переменной
  emit('update:selectedItem', newValue); // Отправляем обновленное значение в родительский компонент
};

const updateSearchQuery = (newValue) => {
  emit('update:searchQuery', newValue);
};

// Определение функции selectItem
const selectItem = (value) => {
  selectedItem.value = value; // Обновляем значение локальной переменной
  emit('update:selectedItem', value); // Отправляем обновленное значение в родительский компонент
};

</script>

<style scoped>
.input-field {
  caret-color: transparent; /* Убираем стандартный курсор */
}
</style>
