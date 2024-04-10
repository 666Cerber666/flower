<template>
  <Header :navigation="navigation" @navigate="handleNavigation"/>
  <TableTasks @selected-item-changed="updateSelectedItem"  :currentPage="currentPage" @page-changed="handlePageChange" v-if="currentTable === 'задачи'"/>
  <TableWorkers @selected-item-changed="updateSelectedItem" :currentPage="currentPage" @page-changed="handlePageChange" v-else-if="currentTable === 'пользователи'" />
  <TableBrokers @selected-item-changed="updateSelectedItem" :currentPage="currentPage" @page-changed="handlePageChange" v-else-if="currentTable === 'заказчики'" />
  <Pagination :selected-item="selectedItem" @update:selectedItem="updateSelectedItem" @page-changed="handlePageChange" :totalPages="totalPages" />
</template>

<script setup>
import { ref, computed } from 'vue';
import Header from './components/Header.vue';
import TableTasks from './components/tables/TableTasks.vue';
import TableWorkers from './components/tables/TableWorkers.vue';
import TableBrokers from './components/tables/TableBrokers.vue';
import Pagination from './components/Pagination.vue';

const currentTable = ref('задачи');
const currentPage = ref(1);
const items = ref([15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15]);
const selectedItem = ref('10')

const updateSelectedItem = (value) => {
  selectedItem.value = value;
};

const totalPages = computed(() => Math.ceil(items.value.length / parseInt(selectedItem.value)));

const navigation = ref([
  { name: 'Задачи', current: true },
  { name: 'Пользователи', current: false },
  { name: 'Заказчики', current: false },
]);

const handleNavigation = (item) => {
  console.log(`Navigated to ${item.name}`);
  currentTable.value = item.name.toLowerCase();
  navigation.value.forEach(navItem => {
    navItem.current = navItem.name === item.name;
  });
};

const handlePageChange = (page) => {
  console.log(`Navigated to page ${page}`);
  currentPage.value = page;
};

const updateSearchQuery = (value) => {
  // Обработка обновления поискового запроса
};
</script>


<style scoped>
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