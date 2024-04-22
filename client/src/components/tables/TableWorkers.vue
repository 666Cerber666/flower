<template>
  <div class="p-4">
    <TableHead @update:selectedWorker="updateSelectedWorker" :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery" :workers="workers.length ? workers : []"/>

    <div class="overflow-x-auto">
      <table class="w-full border-collapse border mb-16">
        <TableTH :currentPage="currentPage" :sortByField="sortByField" :sortOrder="sortOrder" @sortedData="updateSortedData"/>
        <tbody>
          <tr v-for="(worker, index) in uniqueWorkers" :key="index" :class="{ 'bg-gray-100': index % 2 !== 0 }">
            <router-link :to="getRouterLink(worker, flowerId)"><td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ worker }}</td></router-link>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center" :class="{ 'text-green-500': isOnline(worker), 'text-red-500': !isOnline(worker) }">{{ isOnline(worker) ? 'Online' : 'Offline' }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ getStartedCountForWorker(worker) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ getFailedCountForWorker(worker) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ getSuccessCountForWorker(worker) }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ getRetriedCountForWorker(worker) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineProps, defineEmits, watch } from 'vue';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/vue/20/solid';
import TableHead from '../TableHead.vue';
import TableTH from './componentsTables/TableTH.vue';
import { fetchFlower, fetchFlowerTasks } from '../../apiFunctions/api.ts';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const apidata = ref([]);
const workerKeys = ref([]);
const filteredData = ref([]);
const responseData = ref(null);
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

const getRouterLink = (worker, flowerId) => {
        return { 
            name: 'WorkerTasks', 
            query: { flowerId: flowerId, worker: worker }
        };
};

const emit = defineEmits(['update:selectedItem', 'total-pages-changed']);

// Функция для группировки данных по worker
const groupDataByWorker = () => {
  const grouped = {};
  apidata.value.forEach(item => {
    const worker = item.worker;
    if (!grouped[worker]) {
      grouped[worker] = [];
    }
    grouped[worker].push(item);
  });
  return grouped;
};

const updateSelectedWorker = (newValue) => {
  selectedWorker.value = newValue; // Обновляем значение selectedWorker
};

const totalPages = computed(() => {
  const selectedItemValue = parseInt(selectedItem.value);
  const totalItems = uniqueWorkers.length;
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

const groupedData = computed(() => {
  return groupDataByWorker();
});

const getSuccessCountForWorker = (worker) => {
  return apidata.value.filter(item => item.state === "SUCCESS" && item.worker === worker).length;
};

const getStartedCountForWorker = (worker) => {
  return apidata.value.filter(item => item.state === "STARTED" && item.worker === worker).length;
};

const getFailedCountForWorker = (worker) => {
  return apidata.value.filter(item => item.state === "FAILURE" && item.worker === worker).length;
};

const getRetriedCountForWorker = (worker) => {
  return apidata.value.filter(item => item.retried != null && item.worker === worker).length;
};

const isOnline = (worker) => {
  return (
    getSuccessCountForWorker(worker) > 0 ||
    getStartedCountForWorker(worker) > 0 ||
    getFailedCountForWorker(worker) > 0 ||
    getRetriedCountForWorker(worker) > 0
  );
};

const formatTimestamp = (timestamp) => {
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

const uniqueWorkers = computed(() => {
  const unique = new Set(); // Используем Set для хранения уникальных значений
  apidata.value.forEach(item => {
    unique.add(item.worker); // Добавляем значение worker в Set
  });
  return Array.from(unique); // Преобразуем Set обратно в массив
});


onMounted(async () => {
  responseData.value = await fetchFlowerTasks(flowerId); 
  if (responseData.value) {
    apidata.value = Object.values(responseData.value); 
    workerKeys.value = Object.keys(responseData.value);
    console.log(responseData.value); 
    updateSortedData({ sortByField: sortByField.value, sortOrder: sortOrder.value });
    flowerData.value = await fetchFlower(flowerId);
    updateSortedData({ sortByField: 'name', sortOrder: 'success' });
    emit('total-pages-changed', totalPages.value);
    emit('update:selectedItem', selectedItem.value);
  }
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
