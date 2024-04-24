<template>
    <Header />
    <div class="p-6">
      <div class="flex justify-between items-center mb-4 gap-4">
        <div class="relative w-auto rounded">
          <input
              type="text"
              v-model="searchQuery"
              @input="updateCursorPos"
              @focus="isInputFocused = true"
              @blur="isInputFocused = false"
              placeholder="Поиск..."
              class="input-field px-2 py-1 border border-gray-300 rounded-md rounded-l-none pr-8 w-full sm:w-full shadow-md transition-shadow transition-colors duration-300 focus:outline-none focus:border-gray-100 focus:bg-gray-100 focus:shadow-lg"
            />
          <div class="cursor" v-if="isInputFocused" :style="{ left: cursorPosition + 'px' }"></div>
          <svg xmlns="http://www.w3.org/2000/svg"
              class="absolute right-2 top-5 transform -translate-y-1/2 h-6 w-6 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l5-5m0 0l-5-5m5 5H4"/>
          </svg>
        </div>
        <div>
          <button @click="showModal = true" class="bg-violet-600 hover:bg-violet-900 w-full text-white font-bold py-2 px-4 rounded hover:bg-indigo-700">Добавить Flower</button>
        </div>
      </div>

    <div class="overflow-x-auto mb-6">
      <div class="grid grid-cols-1 gap-4 justify-center">
        <div v-for="(item, index) in filteredItems" :key="index" :class="{ [getStatusClass(item.status)]: true, 'border bg-gray-100 font-bold': index % 2 !== 0 }" class="grid grid-cols-3 p-4 border border-gray-300 rounded-md shadow-md hover:shadow-lg transition duration-300">
          <router-link :to="getRouterLink(item)" class="w-full text-center font-bold p-2">{{ item.name }}</router-link>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <div class='status-background rounded-full font-bold p-2'><p :class="[getTextStatusColor(item.status)]">{{item.status}}</p></div>
        </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <button @click="handleDeleteClick(item.id)" class="bg-violet-600 hover:bg-violet-900 text-white font-bold py-2 px-4 sm:w-auto rounded focus:outline-none focus:shadow-outline transition duration-300 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2 hidden sm:block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                Удалить
              </button>
        </div>
    </div>
</div>

    </div>

        <transition name="modal">
              <div>
              <div v-if="showModal" @click="closeModal" class="modal fixed inset-0 bg-black opacity-50">
              </div>
              <div v-if="showModal" class="fixed modal inset-0 flex items-center justify-center" @click.self="closeModal">
                <div class="bg-white p-8 rounded-lg shadow-xl w-1/2 sm:w-full">
                <h2 class="text-2xl font-bold mb-4">Добавить Flower</h2>
                <form @submit.prevent="addFlowerItem">
                    <div class="mb-4 flex flex-col">
                    <label for="name" class="text-gray-700 text-sm font-bold mb-2 flex items-start" :class="{ 'focused': isFieldFocused('name') }">Название:</label>
                    <input type="text" @focus="setFieldFocused('name', true)" @blur="setFieldFocused('name', false)" v-model="newFlower.name" id="name" name="name" class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    </div>
                    <div class="mb-4">
                    <label for="name" class="text-gray-700 text-sm font-bold mb-2 flex items-start" :class="{ 'focused': isFieldFocused('ip') }">IP:</label>
                    <input type="text" @focus="setFieldFocused('ip', true)" @blur="setFieldFocused('ip', false)" v-model="newFlower.ip" id="ip" name="ip" class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    </div>
                    <div class="mb-4">
                    <label for="name" class="text-gray-700 text-sm font-bold mb-2 flex items-start" :class="{ 'focused': isFieldFocused('port') }">PORT:</label>
                    <input type="text" @focus="setFieldFocused('port', true)" @blur="setFieldFocused('port', false)" v-model="newFlower.port" id="port" name="port" class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    </div>
                    <div class="mb-4">
                    <label for="name" class="text-gray-700 text-sm font-bold mb-2 flex items-start" :class="{ 'focused': isFieldFocused('login') }">LOGIN:</label>
                    <input type="text" @focus="setFieldFocused('login', true)" @blur="setFieldFocused('login', false)" v-model="newFlower.login" id="login" name="login" class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    </div>
                    <div class="mb-4">
                    <label for="name" class="text-gray-700 text-sm font-bold mb-2 flex items-start" :class="{ 'focused': isFieldFocused('password') }">PASSWORD:</label>
                    <input type="text" @focus="setFieldFocused('password', true)" @blur="setFieldFocused('password', false)" v-model="newFlower.password" id="password" name="password" class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline">
                    </div>
                    <div class="flex justify-end mb-4 flex-col sm:flex-row">
                      <button type="submit" class="bg-gray-800 text-white font-bold py-2 px-4 mr-2 rounded mb-2 sm:mb-0 sm:mr-2 hover:bg-indigo-700">Добавить</button>
                      <button @click="closeModal" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded sm:mb-0 sm:mr-2">Отмена</button>
                    </div>
                </form>
              </div>
                </div>
            </div>
        </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { fetchFlowers, addFlower, deleteFlower } from '../apiFunctions/api.ts';
  import Header from '../components/Header.vue';
  import { useRouter } from 'vue-router';
  import Pagination from '../components/Pagination.vue';
  import './../ComponentsStyle/gridstyles.css';
  
  const props = defineProps({
    filteredItems: Array
  });
  
  const router = useRouter();
  const currentTable = ref('задачи');
  const isFieldFocusedMap = ref({
    name: false,
    ip: false,
    port: false,
    login: false,
    password: false
  });
  const cursorPosition = ref(0);
  const currentPage = ref(1);
  const searchQuery = ref('');
  const flowerData = ref(null);
  const isInputFocused = ref(false);
  const items = ref([]);
  const showModal = ref(false);
  const newFlower = ref({
    name: '',
    ip: '',
    port: '',
    login: '',
    password: '',
    status: ''
  });
  
  const getRouterLink = (item) => {
    if (item.status === 'Not Completed') {
        return '';
    } else {
        return { 
            name: 'Tables', 
            query: { flowerId: item.id }
        };
    }
};
  
  const updateCursorPos = () => {
    const input = document.querySelector('.input-field');
    const cursorPos = input.selectionStart;
    const textBeforeCursor = searchQuery.value.substring(0, cursorPos);
    const textWidth = getTextWidth(textBeforeCursor, input);
    const cursorOffset = 10; // Отступ от левого края input
  
    cursorPosition.value = textWidth + cursorOffset;
  };
  
  const getTextWidth = (text, input) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    context.font = window.getComputedStyle(input).getPropertyValue('font');
  
    return context.measureText(text).width;
  };
  
  const closeModal = () => {
    showModal.value = false; // Устанавливаем showModal в значение false для закрытия модального окна
  };
  
  const setFieldFocused = (fieldName, focused) => {
    isFieldFocusedMap.value[fieldName] = focused;
  };
  
  const isFieldFocused = (fieldName) => {
    return isFieldFocusedMap.value[fieldName];
  };
  
  const updateSelectedItem = (value) => {
    selectedItem.value = value;
  };
  
  const clearNewFlower = () => {
    newFlower.value.name = '';
    newFlower.value.connection_status = '';
    newFlower.value.ip = '';
    newFlower.value.port = '';
    newFlower.value.login = '';
    newFlower.value.password = '';
  };
  
  const addNewFlowerToList = (flower) => {
    items.value.push(flower);
  };
  
  const handleError = (error) => {
    console.error(error);
    // Дополнительная обработка ошибок
  };
  
  const totalPages = computed(() => {
  if (!items.value) return 0; // Проверяем, определен ли массив items
  return Math.ceil(items.value.length / parseInt(selectedItem.value));
});

  
  const handlePageChange = (page) => {
    console.log(`Navigated to page ${page}`);
    currentPage.value = page;
  };
  
  const fetchFlowersList = () => {
  fetchFlowers()
    .then((response) => {
      items.value = response;
    })
    .catch(handleError);
};

const deleteFlowerItem = (flowerId) => {
  deleteFlower(flowerId)
    .then(response => {
      fetchFlowersList(); // После успешного удаления обновляем список цветов
    })
    .catch(error => {
      console.error('Error deleting flower:', error);
    });
};
  
  const handleDeleteClick = (flowerId) => {
    if (confirm("Вы уверены, что хотите удалить этот цветок?")) {
      deleteFlowerItem(flowerId);
    }
  };
  
  const getStatusClass = (status) => {
    switch (status) {
      case 'Completed':
        return 'border-grid-col-accept';
      case 'In Progress':
        return 'border-grid-col-wait';
      case 'Not Completed':
        return 'border-grid-col-cancel';
      default:
        return '';
    }
  };
  
  const getTextStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'text-green-700';
      case 'In Progress':
        return 'text-indigo-700';
      case 'Not Completed':
        return 'text-red-500';
      default:
        return '';
    }
  };
  
  const addFlowerItem = () => {
    // Проверяем, что все поля заполнены
    if (!newFlower.value.name || !newFlower.value.ip || !newFlower.value.port || !newFlower.value.login || !newFlower.value.password) {
        console.error("Please fill in all fields.");
        return;
    }

    // Вызываем функцию добавления цветка из нашего модуля api.js
    addFlower(newFlower.value)
        .then(response => {
            showModal.value = false;
            // Обновляем статус нового цветка на основе ответа от сервера
            newFlower.value.status = response.status;
            console.log(newFlower);
            addNewFlowerToList(newFlower.value); // Сначала добавляем новый цветок в список
            clearNewFlower(); // Затем очищаем форму
            fetchFlowersList();
        })
        .catch(handleError);
};

  
const filteredItems = computed(() => {
    const query = searchQuery.value.trim().toLowerCase();
    if (!query) {
      return items.value; // Если поисковой запрос пустой, возвращаем все элементы
    } else {
      // Фильтруем элементы по названию (или любому другому полю, которое вы хотите использовать)
      return items.value ? items.value.filter(item => item.name.toLowerCase().includes(query)) : [];
    }
});

  
  const updateSearchQuery = (event) => {
    searchQuery.value = event.target.value;
    updateCursorPos(); // Обновляем также позицию курсора при изменении текста
  };
  
  onMounted(() => {
    fetchFlowersList();
    updateCursorPos();
  });
  </script>