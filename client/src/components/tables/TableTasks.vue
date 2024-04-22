<template>
  <div class="p-4">
    <TableHead @update:selectedWorker="updateSelectedWorker" :current-page="currentPage" :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery" :workers="workers.length ? workers : []"/>

    <div class="overflow-x-auto">
      <table class="w-full border-collapse border mb-16">
        <TableTH :currentPage="currentPage" :sortByField="sortByField" :sortOrder="sortOrder" @sortedData="updateSortedData"/>
        <tbody>
          <tr v-for="(item, index) in filteredData" :key="index" :class="{ 'bg-gray-100': index % 2 !== 0 }">
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.name }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.uuid }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">
              <div class='rounded-full flex justify-center font-bold text-black' :class="getStatusClass(item.state)">{{ item.state }}</div>
            </td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.args }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.kwargs }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.result }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ formatTimestamp(item.received) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ formatTimestamp(item.started) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ formatRuntime(item.runtime) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.worker }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineProps, defineEmits, watch } from 'vue';
import { useRoute } from 'vue-router';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/vue/20/solid';
import TableHead from '../TableHead.vue';
import TableTH from './componentsTables/TableTH.vue';
import { fetchFlower, fetchFlowerTasks } from '../../apiFunctions/api.ts';
import axios from 'axios';

const apidata = ref([]);
const route = useRoute();
const flowerData = ref(null);
const flowerId = route.query.flowerId;
const searchQuery = ref('');
const sortedData = ref([]);
const sortByField = ref('name'); // Field to sort by
const sortOrder = ref('asc'); // Sort order (asc/desc)
const selectedItem = ref('10');
const workers = ref([]);
const selectedWorker = ref('');

const props = defineProps({
  currentPage: Number,
});

const emit = defineEmits(['update:selectedItem', 'total-pages-changed']);

const getStatusClass = (state) => {
  switch (state) {
    case 'SUCCESS':
      return 'text-green-500'; // Зеленый цвет для успешного выполнения
    case 'FAILURE':
      return 'text-red-500'; // Красный цвет для неудачного выполнения
    case 'STARTED':
      return 'text-yellow-500'; // Желтый цвет для задач, которые находятся в процессе выполнения
    default:
      return ''; // По умолчанию, если статус не определен, вернем пустую строку
  }
};

const updateSelectedWorker = (newValue) => {
  selectedWorker.value = newValue; // Обновляем значение selectedWorker
};

const totalPages = computed(() => {
    const selectedItemValue = parseInt(selectedItem.value);
    const totalItems = Object.values(apidata.value).length;
    if (totalItems <= selectedItemValue) {
        return 1; // Вернуть 1, если количество элементов меньше или равно selectedItem
    } else {
        return Math.ceil(totalItems / selectedItemValue);
    }
});

const updateSearchQuery = (query) => {
    searchQuery.value = query;
};

const updateSelectedItem = (value) => {
  selectedItem.value = value; // Обновляем значение selectedItem
};

const updateSortedData = ({ sortByField: newSortByField, sortOrder: newSortOrder }) => {
    sortByField.value = newSortByField;
    sortOrder.value = newSortOrder;

    const entries = Object.entries(apidata.value);
    entries.sort(([keyA, valueA], [keyB, valueB]) => {
        const fieldA = (valueA[newSortByField] || '').toLowerCase();
        const fieldB = (valueB[newSortByField] || '').toLowerCase();
        if (fieldA < fieldB) return newSortOrder === 'asc' ? -1 : 1;
        if (fieldA > fieldB) return newSortOrder === 'asc' ? 1 : -1;
        return 0;
    });

    const sortedObject = Object.fromEntries(entries);
    sortedData.value = sortedObject;
};

const paginatedData = computed(() => {
    const startIndex = (props.currentPage - 1) * parseInt(selectedItem.value);
    const endIndex = startIndex + parseInt(selectedItem.value);
    const dataArray = Object.values(apidata.value);
    return dataArray.slice(startIndex, endIndex);
});

const combinedData = computed(() => {
    const startIndex = (props.currentPage - 1) * parseInt(selectedItem.value);
    const endIndex = startIndex + parseInt(selectedItem.value);
    const dataArray = Object.values(sortedData.value);
    const paginatedArray = dataArray.slice(startIndex, endIndex);
    return paginatedArray;
});

const filteredData = computed(() => {
    if (!searchQuery.value.trim() && !selectedWorker.value) {
        // Если строка поиска пуста и выбранный воркер не установлен, верните все данные
        return combinedData.value;
    } else {
        // Иначе фильтруйте данные на основе searchQuery и/или selectedWorker
        const query = searchQuery.value.trim().toLowerCase();
        const worker = selectedWorker.value.toLowerCase();
        return combinedData.value.filter(item => {
            // Фильтруйте данные по значениям полей name и worker
            const nameMatches = item.name.toLowerCase().includes(query);
            const workerMatches = worker ? item.worker.toLowerCase() === worker : true; // Если выбран воркер, проверяем его соответствие
            return nameMatches && workerMatches;
        });
    }
});

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

const formatRuntime = (runtime) => {
  const hours = Math.floor(runtime / 3600);
  const minutes = Math.floor((runtime % 3600) / 60);
  const seconds = Math.floor(runtime % 60);
  
  return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
};


onMounted(async () => {
    const responseData = await fetchFlowerTasks(flowerId);
    apidata.value = responseData;
    updateSortedData({ sortByField: sortByField.value, sortOrder: sortOrder.value });
    flowerData.value = await fetchFlower(flowerId);
    updateSortedData({ sortByField: 'state', sortOrder: 'success' });
    emit('total-pages-changed', totalPages.value);
    emit('update:selectedItem', selectedItem.value);

    // Заполнение списка workers
    const uniqueWorkers = new Set();
    Object.values(apidata.value).forEach(item => {
        uniqueWorkers.add(item.worker);
    });
    workers.value = Array.from(uniqueWorkers);

});


watch(selectedItem, (newValue, oldValue) => {
  selectedItem.value = newValue;
  emit('update:selectedItem', newValue);
  emit('total-pages-changed', totalPages.value);
});

</script>

<style scoped>
.arrow-icon {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 5px solid transparent;
  border-right: 5px solid transparent;
}

.arrow-up {
  border-bottom: 5px solid black;
}

.arrow-down {
  border-top: 5px solid black;
}

.rotate-arrow {
  animation: rotateArrow 0.5s forwards;
}

@keyframes rotateArrow {
  from {
    transform: translateY(-50%) rotate(0deg);
  }
  to {
    transform: translateY(-50%) rotate(180deg);
  }
}
</style>
