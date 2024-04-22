<template>
    <Header />
    <div class="p-6">
      <TableHead :current-page="currentPage" :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery" />

    <div class="overflow-x-auto mb-6">
      <div class="grid grid-cols-1 gap-4 justify-center">
    <div v-for="(item, index) in latestItems" :key="index" :class="{ [getStatusClass(item.state)]: true, 'border bg-gray-100 font-bold': index % 4 !== 0 }" class="grid grid-cols-4 p-4 border border-gray-300 rounded-md shadow-md hover:shadow-lg transition duration-300">
        <div class="w-full text-center font-bold p-2">{{ item.name }} </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <div class='status-background rounded-full font-bold p-2'><p :class="[getTextStatusColor(item.state)]">{{item.state}}</p></div>
        </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <div class='status-background rounded-full font-bold p-2'><p>{{formatTimestamp(item.started)}}</p></div>
        </div>
        <div class="w-full text-center font-bold flex items-center justify-center">
            <button @click="handleStartClick(item.id)" class="bg-violet-600 hover:bg-violet-900 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 flex items-center justify-center">
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
    <Pagination :selectedItem="selectedItem" :totalPages="totalPagesComputed" :currentPage="currentPage" @page-changed="handlePageChange" />
  </template>
  
  <script setup>
  import { ref, computed, onMounted, defineEmits } from 'vue';
  import { fetchFlowers, fetchFlowerTasks } from '../apiFunctions/api.ts';
  import Header from '../components/Header.vue';
  import { useRoute } from 'vue-router';
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
  const searchQuery = ref('');
  const flowerId = route.query.flowerId;
  const flowerData = ref(null);
  const isInputFocused = ref(false);
  const items = ref([]);
  const emit = defineEmits(['update:selectedItem', 'total-pages-changed']);
  
  const getStatusClass = (state) => {
      switch (state) {
          case 'SUCCESS':
              return 'border-grid-col-accept';
          case 'STARTED':
              return 'border-grid-col-wait';
          case 'FAILURE':
              return 'border-grid-col-cancel';
          case 'RECEIVED':
              return 'border-grid-col-wait';
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
          default:
              return '';
      }
  };
  
  const updateSelectedItem = (value) => {
      selectedItem.value = value;
  };

  const updateSearchQuery = (query) => { // Определяем метод updateSearchQuery
    searchQuery.value = query;
  };
  
  const handleError = (error) => {
      console.error(error);
      // Дополнительная обработка ошибок
  };
  
  const totalPagesComputed = computed(() => {
      if (!items.value) return 0; // Проверяем, определен ли массив items
      return Math.ceil(items.value.length / parseInt(selectedItem.value));
  });
  
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

const latestItems = computed(() => {
    // Сначала сортируем элементы в обратном порядке, чтобы последние выполненные элементы были первыми
    const sortedItems = items.value.slice().reverse();

    // Затем группируем элементы по item.name
    const groupedItems = sortedItems.reduce((groups, item) => {
        const groupName = item.name;
        if (!groups[groupName]) {
            groups[groupName] = [];
        }
        groups[groupName].push(item);
        return groups;
    }, {});

    // Выбираем только последний элемент из каждой группы
    const latest = Object.values(groupedItems).map(group => group.reduce((latestItem, currentItem) => {
        // Если текущий элемент позже по времени, чем последний сохраненный, используем его
        if (!latestItem || currentItem.timestamp > latestItem.timestamp) {
            return currentItem;
        } else {
            return latestItem;
        }
    }, null));

    // Фильтруем найденные последние элементы по поисковому запросу и отсеиваем пустые элементы
    const query = searchQuery.value.trim().toLowerCase();
    if (!query) {
        // Если запрос пуст, возвращаем все найденные последние элементы без фильтрации пустых элементов
        return latest.filter(item => item.name);
    } else {
        // Иначе фильтруем последние элементы по запросу и отсеиваем пустые элементы
        return latest.filter(item => item.name && item.name.toLowerCase().includes(query));
    }
});

  onMounted(() => {
      fetchFlowerTasks(flowerId).then((data) => {
          // После успешной загрузки данных, преобразуем объект в массив и обновляем значение items
          items.value = Object.values(data);
      }).catch((error) => {
          // Обработка ошибки при загрузке данных
          console.error('Error fetching flower tasks:', error);
      });
      emit('total-pages-changed', totalPagesComputed.value);
      emit('update:selectedItem', selectedItem.value);
  });
  
  </script>
  
  <style scoped>
.custom-button {
    background-color: rgb(109 40 217);
    color: white;
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    transition: 0.3s;
    border: none;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
}

.input-field {
  caret-color: transparent; /* Убираем стандартный курсор */
}

.custom-button:hover {
  background-color: rgb(76 29 149);
}

.border-grid-col-cancel{
  border-right: 10px solid red;
}

.border-grid-col-wait{
  border-right: 10px solid indigo;
}

.border-grid-col-accept{
  border-right: 10px solid green;
}

.border-grid-col-cancel:hover{
  transition: 0.3s ;
  border-right: 30px solid red;
  border-radius: 15px;
}

.border-grid-col-wait:hover{
  transition: 0.3s ;
  border-right: 30px solid indigo;
  border-radius: 15px;
}

.border-grid-col-accept:hover{
  transition: 0.3s ;
  border-right: 30px solid green;
  border-radius: 15px;
}

  .status-background {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%; /* Занимает всю высоту ячейки */
  width:100%;
}

label.focused {
  color: rgb(67 56 202);
  font-size:18px ;
  transition: ease 0.3s;
  transform: translateY(-5px);
}

.modal button {
    padding: 10px 20px;
    margin-left: 10px;
    transition: all 0.3s;
}

  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }

  .modal {
  z-index: 9999; /* Установите здесь необходимый вам z-index */
  }

  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.vue:hover {
    filter: drop-shadow(0 0 2em #42b883aa);
  }

  .modal-enter-active, .modal-leave-active {
  transition: opacity 0.5s;
    }

    .modal-enter, .modal-leave-to {
    opacity: 0;
    }

.cursor {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  left: 10px; /* Расположение палочки слева от текста */
  height: 20px; /* Высота палочки */
  width: 2px; /* Ширина палочки */
  background-color: black;
  animation: blink 1s infinite; /* Анимация мигания */
}

@keyframes blink {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
  </style>