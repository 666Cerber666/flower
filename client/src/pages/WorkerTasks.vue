<template>
    <Header />
    <div class="p-6">
      <TableHead :current-page="currentPage" :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery" />
        <div class="flex flex-row-reverse mb-6">
            <button @click="$router.go(-1)" class="md:w-1/6 h-10 w-full bg-violet-600 hover:bg-violet-900 text-center text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 flex items-center justify-center">
            <ChevronLeftIcon class="w-10 h-10"/>
            <p class="font-sans font-medium">Назад</p>
        </button>
        </div>
      

    <div class="overflow-x-auto mb-6">
      <div class="grid grid-cols-1 gap-4 justify-center mb-6">
    <div v-for="(item, index) in latestItemsPaginated" :key="index" :class="{ [getStatusClass(item.state)]: true, 'border bg-gray-100 font-bold': index % 4 !== 0 }" class="flex flex-col sm:grid sm:grid-cols-4 p-4 border border-gray-300 rounded-md shadow-md hover:shadow-lg transition duration-300">
        <router-link :to="getRouterLink(worker, flowerId, item.uuid)"><div class="w-full text-center font-bold p-2">{{ item.name }} </div></router-link>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <div class='status-background rounded-full font-bold p-2'><p :class="[getTextStatusColor(item.state)]">{{item.state}}</p></div>
        </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <div class='status-background rounded-full font-bold p-2'><p>{{formatTimestamp(item.started)}}</p></div>
        </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <button @click="handleStartClick(item.name)" class="bg-violet-600 hover:bg-violet-900 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mr-2" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 0c-5.523 0-10 4.477-10 10s4.477 10 10 10 10-4.477 10-10-4.477-10-10-10zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm5-9l-7 5v-10l7 5z" clip-rule="evenodd" />
                </svg>
                Запустить
            </button>
        </div>
    </div>
</div>

    </div>
    </div>

    <transition name="modal">
    <div v-if="showModal">
        <div class="modal fixed inset-0 bg-black opacity-50" @click="closeModal"></div>
        <div class="fixed modal inset-0 flex items-center justify-center" @click.self="closeModal">
            <div class="bg-white p-8 rounded-lg shadow-xl w-3/6">
                <h2 class="text-2xl font-bold mb-4">Задача запущена</h2>
                <div class="flex justify-end mb-4">
                    <button type="submit" @click="closeModal" class="bg-gray-800 text-white font-bold py-2 px-4 mr-2 rounded hover:bg-indigo-700">Окей</button>
                </div>
            </div>
        </div>
    </div>
</transition>

    <Pagination :selectedItem="selectedItem" :totalPages="totalPagesComputed" :currentPage="currentPage" @page-changed="handlePageChange" />
  </template>
  
  <script setup>
import { ref, computed, onMounted, defineEmits } from 'vue';
import { ChevronLeftIcon } from '@heroicons/vue/20/solid';
import { fetchFlowers, fetchFlowerTasks, applyTask } from '../apiFunctions/api.ts';
import Header from '../components/Header.vue';
import { useRoute } from 'vue-router';
import './../ComponentsStyle/gridstyles.css';
import Pagination from '../components/Pagination.vue';
import TableHead from '../components/TableHead.vue';

const route = useRoute();
const currentTable = ref('задачи');
const isFieldFocusedMap = ref({
    name: false,
    ip: false,
    port: false,
    login: false,
    password: false
});
const selectedItem = ref('10');
const cursorPosition = ref(0);
const currentPage = ref(1);
const showModal = ref(false);
const searchQuery = ref('');
const flowerId = route.query.flowerId;
const worker = route.query.worker;
const flowerData = ref(null);
const isInputFocused = ref(false);
const items = ref([]);
const emit = defineEmits(['update:selectedItem', 'total-pages-changed']);

const getRouterLink = (worker, flowerId, uuid) => {
    return { 
        name: 'TaskInfo', 
        query: { flowerId: flowerId, uuid: uuid }
    };
};

const getStatusClass = (state) => {
    switch (state) {
        case 'SUCCESS':
            return 'border-grid-col-accept';
        case 'STARTED':
            return 'border-grid-col-wait';
        case 'FAILURE':
            return 'border-grid-col-cancel';
        case 'RETRY':
            return 'border-grid-col-wait';
        case 'RECEIVED':
            return 'border-grid-col-rec';
        default:
            return '';
    }
};

const getTextStatusColor = (state) => {
    switch (state) {
        case 'SUCCESS':
            return 'text-green-700';
        case 'STARTED':
            return 'text-indigo-700';
        case 'FAILURE':
            return 'text-red-500';
        case 'RECEIVED':
            return 'text-yellow-500';
        case 'RETRY':
            return 'text-yellow-500';  
        default:
            return '';
    }
};

const updateSelectedItem = (value) => {
    selectedItem.value = value;
};

const updateSearchQuery = (query) => { 
    searchQuery.value = query;
};

const closeModal = () => {
    showModal.value = false; // Устанавливаем showModal в значение false для закрытия модального окна
  };

const handleError = (error) => {
    console.error(error);
    // Дополнительная обработка ошибок
};

const handlePageChange = (page) => {
    console.log(`Navigated to page ${page}`);
    currentPage.value = page;
};

const formatTimestamp = (timestamp) => {
    if (timestamp === null) {
        return null;
    }
    
    const date = new Date(timestamp * 1000);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

const refreshTasks = async () => {
    try {
        // Выполняем запрос на сервер, чтобы получить обновленный список задач
        const data = await fetchFlowerTasks(flowerId);
        // Обновляем переменную, хранящую список задач
        items.value = Object.values(data);
    } catch (error) {
        console.error('Error refreshing tasks:', error);
        // Обработка ошибок, если необходимо
    }
};

const handleStartClick = async (itemName) => {
    try {
        // Выполняем запрос на сервер, чтобы запустить задачу
        await applyTask(flowerId, itemName); // Заменяем itemId на itemName
        // Обновляем список задач после успешного запуска
        showModal.value = true;
        await refreshTasks();
    } catch (error) {
        console.error('Error starting task:', error);
        // Обработка ошибок, если необходимо
    }
};

  
const latestItemsPaginated = computed(() => {
    const startIndex = (currentPage.value - 1) * parseInt(selectedItem.value);
    const endIndex = startIndex + parseInt(selectedItem.value);
    const sortedItems = items.value.slice().reverse();
    const groupedItems = sortedItems.reduce((groups, item) => {
        const groupName = item.name;
        if (!groups[groupName]) {
            groups[groupName] = [];
        }
        groups[groupName].push(item);
        return groups;
    }, {});

    const latest = Object.values(groupedItems).map(group => group.reduce((latestItem, currentItem) => {
        if (!latestItem || currentItem.timestamp > latestItem.timestamp) {
            return currentItem;
        } else {
            return latestItem;
        }
    }, null));

    const query = searchQuery.value.trim().toLowerCase();
    if (!query) {
        return latest.filter(item => item.name && item.worker === worker).slice(startIndex, endIndex);
    } else {
        return latest.filter(item => item.name && item.worker === worker && item.name.toLowerCase().includes(query)).slice(startIndex, endIndex);
    }
});


const latestItems = computed(() => {
    const sortedItems = items.value.slice().reverse();
    const groupedItems = sortedItems.reduce((groups, item) => {
        const groupName = item.name;
        if (!groups[groupName]) {
            groups[groupName] = [];
        }
        groups[groupName].push(item);
        return groups;
    }, {});

    const latest = Object.values(groupedItems).map(group => group.reduce((latestItem, currentItem) => {
        if (!latestItem || currentItem.timestamp > latestItem.timestamp) {
            return currentItem;
        } else {
            return latestItem;
        }
    }, null));

    const query = searchQuery.value.trim().toLowerCase();
    if (!query) {
        return latest.filter(item => item.name && item.worker === worker);
    } else {
        return latest.filter(item => item.name && item.worker === worker && item.name.toLowerCase().includes(query));
    }
});

const totalPagesComputed = computed(() => {
    if (!items.value) return 0; // Проверяем, определен ли массив items
    return Math.ceil(latestItems.value.length / parseInt(selectedItem.value));
});

onMounted(async () => {
    try {
        await fetchFlowerTasks(flowerId);
        await refreshTasks(flowerId);
        emit('total-pages-changed', latestItems.value.length);
        emit('update:selectedItem', selectedItem.value);
    } catch (error) {
        console.error('Error fetching and refreshing tasks:', error);
    }
});
</script>
