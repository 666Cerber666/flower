<template>
  <Header :navigation="navigation" @navigate="handleNavigation" />
  <TableTasks :selectedItem="selectedItem" @selected-item-changed="updateSelectedItem" :total-pages="totalPages" :current-page="currentPage" @page-changed="handlePageChange" v-if="currentTable === 'задачи'" :query="$route.query"/>
  <TableWorkers :selectedItem="selectedItem" @selected-item-changed="selectedItem = $event" :currentPage="currentPage" @page-changed="handlePageChange" v-else-if="currentTable === 'пользователи'" :query="$route.query" />
  <TableBrokers :selectedItem="selectedItem" @selected-item-changed="selectedItem = $event" :currentPage="currentPage" @page-changed="handlePageChange" v-else-if="currentTable === 'заказчики'" :query="$route.query" />
  <Pagination :selected-item="selectedItem" @selected-item-changed="selectedItem = $event" :total-pages="totalPages" :current-page="currentPage" @page-changed="handlePageChange" />
</template>

<script setup>
import { ref } from 'vue';
import Header from '../components/Header.vue';
import TableHead from '../components/TableHead.vue';
import TableTasks from '../components/tables/TableTasks.vue';
import TableWorkers from '../components/tables/TableWorkers.vue';
import TableBrokers from '../components/tables/TableBrokers.vue';
import Pagination from '../components/Pagination.vue';

const currentTable = ref('задачи');
const currentPage = ref(1);
const totalPages = ref(0);
const selectedItem = ref('');

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

const updateSelectedItem = (value) => {
    selectedItem.value = value;
};
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
