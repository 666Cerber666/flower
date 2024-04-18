<template>
  <div class="p-4">
    <TableHead :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery"/>

    <div class="overflow-x-auto">
      <table class="w-full border-collapse border">
        <TableTH :sortByField="sortByField" :sortOrder="sortOrder" @sortedData="updateSortedData"/>
        <tbody>
          <tr v-for="(item, index) in combinedData" :key="index" :class="{ 'bg-gray-100': index % 2 !== 0 }">
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.name }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.uuid }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">
              <div :class="[getStatusClass(item.state), 'rounded-full flex justify-center font-bold text-black']">{{ getExecutionStatus(item.state) }}</div>
            </td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.args }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.kwargs }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.result }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.received }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.started }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.runtime }}</td>
            <td class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 text-center">{{ item.worker }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, defineProps, defineEmits } from 'vue';
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
const selectedItem = ref('')

const props = defineProps({
  currentPage: Number // Определение типа пропса
});

const emit = defineEmits(['update:selectedItem', 'total-pages-changed']);

const totalPages = computed(() => {
    const selectedItemValue = parseInt(props.selectedItem);
    const totalItems = Object.values(apidata.value).length;
    return Math.ceil(totalItems / selectedItemValue);
});

const getExecutionStatus = (state) => {
    switch (state) {
        case 'completed':
            return 'Completed';
        case 'in progress':
            return 'In Progress';
        case 'not completed':
            return 'Not Completed';
        default:
            return state;
    }
};

const getStatusClass = (state) => {
    switch (state) {
        case 'completed':
            return 'bg-green-200';
        case 'in progress':
            return 'bg-yellow-200';
        case 'not completed':
            return 'bg-red-200';
        default:
            return '';
    }
};

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
    const startIndex = (props.currentPage - 1) * parseInt(props.selectedItem);
    const endIndex = startIndex + parseInt(props.selectedItem);
    const dataArray = Object.values(apidata.value);
    return dataArray.slice(startIndex, endIndex);
});

const combinedData = computed(() => {
    const startIndex = (props.currentPage - 1) * parseInt(props.selectedItem);
    const endIndex = startIndex + parseInt(props.selectedItem);
    const dataArray = Object.values(sortedData.value);
    const paginatedArray = dataArray.slice(startIndex, endIndex);
    return paginatedArray;
});

onMounted(async () => {
    apidata.value = await fetchFlowerTasks(flowerId);
    updateSortedData({ sortByField: sortByField.value, sortOrder: sortOrder.value });
    flowerData.value = await fetchFlower(flowerId);
    updateSortedData({ sortByField: 'state', sortOrder: 'success' });
    emit('total-pages-changed', totalPages.value);
    emit('update:selectedItem', props.selectedItem);
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
