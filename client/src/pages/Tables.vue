<template>
  <Header :navigation="navigation" @navigate="handleNavigation" />
  <TableTasks :selectedItem="selectedItem" @update:selectedItem="updateSelectedItem" @total-pages-changed="updateTotalPages" :current-table="currentTable"  @page-changed="handlePageChange" :current-page="currentPage" v-if="currentTable === 'задачи'" :query="$route.query"/>
  <TableWorkers :selectedItem="selectedItem" @update:selectedItem="updateSelectedItem" @total-pages-changed="updateTotalPages" :current-table="currentTable" @page-changed="handlePageChange" :current-page="currentPage" v-else-if="currentTable === 'пользователи'" :query="$route.query" />
  <Pagination :selectedItem="selectedItem" :totalPages="totalPagesComputed" :currentPage="currentPage" @page-changed="handlePageChange" />
</template>

<script setup>
import { onMounted, ref, watch, computed, provide } from 'vue';
import Header from '../components/Header.vue';
import TableTasks from '../components/tables/TableTasks.vue';
import TableWorkers from '../components/tables/TableWorkers.vue';
import Pagination from '../components/Pagination.vue';

const currentTable = ref('задачи');
const currentPage = ref(1);
const selectedItem = ref('10');

const navigation = ref([
  { name: 'Задачи', current: true },
  { name: 'Пользователи', current: false },
]);

const handleNavigation = (item) => {
  currentTable.value = item.name.toLowerCase();
  navigation.value.forEach(navItem => {
    navItem.current = navItem.name === item.name;
  });
};

const handlePageChange = (page) => {
  currentPage.value = page;
};

const updateSelectedItem = (value) => {
    selectedItem.value = value;
};

const totalPagesTasks = ref(0);
const totalPagesWorkers = ref(0);
const totalPagesBrokers = ref(0);

const totalPagesComputed = computed(() => {
  if (currentTable.value === 'задачи') {
    return totalPagesTasks.value;
  } else if (currentTable.value === 'пользователи') {
    return totalPagesWorkers.value;
  } else if (currentTable.value === 'заказчики') {
    return totalPagesBrokers.value;
  }
});

const updateTotalPages = (pages) => {
  if (currentTable.value === 'задачи') {
    totalPagesTasks.value = pages;
  } else if (currentTable.value === 'пользователи') {
    totalPagesWorkers.value = pages;
  } else if (currentTable.value === 'заказчики') {
    totalPagesBrokers.value = pages;
  }
};

provide('currentTable', currentTable);

onMounted(() => {
  updateTotalPages(totalPagesComputed.value);
});

watch(selectedItem, (newValue, oldValue) => {
  selectedItem.value = newValue;
});

</script>

<style>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
