<template>
  <div class="flex flex-col md:flex-row sm:gap-4 justify-between items-center mb-4">
    <div class="flex mb-2">
      <div class="relative mr-4">
        <label for="items-per-page">Количество элементов:</label>
        <input
            id="items-per-page"
            :value="selectedItem"
            @input="updateSelectedItem($event.target.value); updateCursorPos()"
            @focus="isOpen = true"
            @blur="isOpen = false"
            class="input-field w-24 text-center py-2 rounded-md border border-gray-300 appearance-none transition duration-300 ease-in-out cursor-pointer sm:h-13"
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

      <div class="relative" v-if="currentTable === 'задачи'">
        <label for="items-per-page">Задачи по воркеру:</label>
        <input
          id="items-per-page"
          :value="selectedWorker"
          @input="updateSelectedWorker($event.target.value)"
          @focus="isOpenWorker = true"
          @blur="isOpenWorker = false"
          class="input-field w-150 sm:w-150 text-center py-2 rounded-md border border-gray-300 appearance-none transition duration-300 ease-in-out cursor-pointer"
        />
        <transition name="slide-fade">
          <ul
            v-if="isOpenWorker"
            class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded shadow-md pointer-events-auto z-10"
          >
            <!-- Добавляем пустое значение -->
            <li @click="selectWorker(emptyWorker)" class="cursor-pointer hover:bg-gray-100 rounded px-2 py-1">Пусто</li>
            <!-- Затем добавляем остальные воркеры -->
            <li
              v-for="worker in workers"
              :key="worker"
              @click="selectWorker(worker)"
              class="cursor-pointer hover:bg-gray-100 rounded px-2 py-1"
            >{{ worker }}</li>
          </ul>
        </transition>
      </div>
    </div>

    <div class="relative w-auto rounded">
      <input
        type="text"
        :value="searchQuery"
        @input="updateSearchQuery($event.target.value); updateCursorPos()"
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
import { ref, defineEmits, defineProps, inject, onMounted } from 'vue';

const emit = defineEmits(['update:selectedItem', 'update:selectedWorker', 'update:searchQuery']);

const isInputFocused = ref(false);
const isFieldFocusedMap = ref({
    name: false,
    ip: false,
    port: false,
    login: false,
    password: false
  });
const searchQuery = ref('');
const cursorPosition = ref(0);
const isOpen = ref(false);
const isOpenWorker = ref(false);
const options = [
  { value: '10', label: '10' },
  { value: '15', label: '15' },
  { value: '25', label: '25' },
];

const updateCursorPos = () => {
    const input = document.querySelector('.input-field');
    const cursorPos = input.selectionStart;
    const textBeforeCursor = searchQuery.value.substring(0, cursorPos);
    const textWidth = getTextWidth(textBeforeCursor, input);
    const cursorOffset = 10; 
  
    cursorPosition.value = textWidth + cursorOffset;
  
    // Если курсор находится в конце текста, прокрутим его вправо, чтобы он был видимым
    if (cursorPos === searchQuery.value.length) {
        input.scrollLeft = input.scrollWidth;
    }
};

  const getTextWidth = (text, input) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = window.getComputedStyle(input).getPropertyValue('font');
  
    return context.measureText(text).width;
  };
    
  const setFieldFocused = (fieldName, focused) => {
    isFieldFocusedMap.value[fieldName] = focused;
  };
  
  const isFieldFocused = (fieldName) => {
    return isFieldFocusedMap.value[fieldName];
  };

const props = defineProps({
  workers: Array, 
  currentTable: String// Проп для списка работников
});

const currentTable = inject('currentTable', null);

const selectedItem = ref('10');
const selectedWorker = ref(''); // Добавлено состояние для выбранного работника

const updateSelectedItem = (newValue) => {
  selectedItem.value = newValue; // Обновляем значение локальной переменной
  emit('update:selectedItem', newValue); // Отправляем обновленное значение в родительский компонент
};

const updateSelectedWorker = (newValue) => {
  selectedWorker.value = newValue; // Обновляем значение локальной переменной
  emit('update:selectedWorker', newValue); // Отправляем обновленное значение в родительский компонент
};

const updateSearchQuery = (newValue) => {
  searchQuery.value = newValue;
  updateCursorPos(); // Обновляем позицию курсора при изменении текста
  emit('update:searchQuery', newValue);
};

// Определение функции selectItem
const selectItem = (value) => {
  selectedItem.value = value; // Обновляем значение локальной переменной
  emit('update:selectedItem', value); // Отправляем обновленное значение в родительский компонент
};

// Определение функции selectWorker
const selectWorker = (value) => {
  selectedWorker.value = value; // Обновляем значение локальной переменной
  emit('update:selectedWorker', value); // Отправляем обновленное значение в родительский компонент
};

onMounted(() => {
  updateCursorPos();
})

</script>

<style scoped>
.input-field {
  caret-color: transparent; /* Убираем стандартный курсор */
}
</style>
