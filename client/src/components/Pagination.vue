<template>
  <div :class="{ 'dark-theme': isDarkTheme }" class="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 fixed bottom-0 left-0 w-full bg-white shadow-md p-4">
    <!-- Навигация для мобильных устройств -->
    <div class="flex flex-1 justify-between sm:hidden">
      <a href="#" class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Previous</a>
      <a href="#" class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">Next</a>
    </div>
    <!-- Навигация для десктопных устройств -->
    <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
      <div>
        <p :class="{ 'dark-theme-text': isDarkTheme }" class="text-sm text-gray-700">
          Показаны
          {{ ' ' }}
          с
          {{ ' ' }}
          <span class="font-medium">{{ startIndex }}</span>
          предмета
          {{ ' ' }}
          по
          {{ ' ' }}
          <span class="font-medium">{{ selectedItem }}</span>
          результатов
          {{ ' ' }}
          на
          {{ ' ' }}
          <span class="font-medium">{{ totalPages }}</span>
          {{ ' ' }}
          страницах
        </p>
      </div>
      <div>
        <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
          <!-- Кнопка "Предыдущая" -->
          <a :class="{ 'dark-theme-text': isDarkTheme }" class="cursor-pointer relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" @click="goToPreviousPage">
            <span class="sr-only">Предыдущая</span>
            <ChevronLeftIcon class="h-5 w-5" aria-hidden="true" />
          </a>
          <!-- Кнопки с номерами страниц -->
          <template v-for="page in totalPages">
            <a href="#" class="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" :class="{ 'bg-indigo-600 text-white': page === currentPage }" @click="goToPage(page)">
              {{ page }}
            </a>
          </template>
          <!-- Кнопка "Следующая" -->
          <a :class="{ 'dark-theme-text': isDarkTheme }" class="cursor-pointer relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0" @click="goToNextPage">
            <span class="sr-only">Следующая</span>
            <ChevronRightIcon class="h-5 w-5" aria-hidden="true" />
          </a>
        </nav>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dark-theme {
  background-color: rgb(2 6 23); /* Тёмный цвет фона для темной темы */
}
.dark-theme-text{
  color: #fff; /* Цвет текста для темной темы */
}
.dark-theme-text:hover{
  color: gray; /* Цвет текста для темной темы */
}
</style>

<script setup>
import { ref, watch, computed, defineProps, defineEmits, onMounted } from 'vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/solid';

const props = defineProps({
  selectedItem: {
    type: String,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
});

const emits = defineEmits(['page-changed']);
const isDarkTheme = ref(false);

// Функция перехода на предыдущую страницу
function goToPreviousPage() {
  if (props.currentPage > 1) {
    emits('page-changed', props.currentPage - 1);
  }
}

// Функция перехода на следующую страницу
function goToNextPage() {
  if (props.currentPage < props.totalPages) {
    emits('page-changed', props.currentPage + 1);
  }
}

// Функция перехода на конкретную страницу
function goToPage(page) {
  emits('page-changed', page);
}

// Вычисляемые свойства для определения индексов начальной и конечной записей на текущей странице
const startIndex = computed(() => (props.currentPage - 1) * parseInt(props.selectedItem) + 1);
const endIndex = computed(() => Math.min(startIndex.value + parseInt(props.selectedItem) - 1, props.totalPages));

// Следим за изменениями props.selectedItem и обновляем itemsPerPage
watch(() => props.selectedItem, (newValue) => {
  props.selectedItem = newValue;
  emits('page-changed', 1); // Переходим на первую страницу при изменении количества элементов на странице
});

onMounted(() => {
  const theme = localStorage.getItem('theme');
  isDarkTheme.value = theme === 'true';
});
</script>