<template>
<thead v-if="currentTable === 'задачи'" class="bg-gray-200">
    <tr>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('name')">Задача <span class="arrow-icon"  v-if="sortByField === 'name'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('uuid')">UUID <span class="arrow-icon" v-if="sortByField === 'uuid'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('state')">Статус <span class="arrow-icon" v-if="sortByField === 'state'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('args')">Args <span class="arrow-icon" v-if="sortByField === 'args'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('kwargs')">Kwargs <span class="arrow-icon" v-if="sortByField === 'kwargs'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('result')">Результат <span class="arrow-icon" v-if="sortByField === 'result'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('received')">Получено <span class="arrow-icon" v-if="sortByField === 'received'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('started')">Начато <span class="arrow-icon" v-if="sortByField === 'started'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('runtime')">Время работы <span class="arrow-icon" v-if="sortByField === 'runtime'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('worker')">Создатель <span class="arrow-icon" v-if="sortByField === 'worker'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
    </tr>
  </thead>

  <thead v-else-if="currentTable === 'пользователи'" class="bg-gray-200">
      <tr>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('name')">Рабочий <span class="arrow-icon"  v-if="sortByField === 'name'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('uuid')">Статус <span class="arrow-icon" v-if="sortByField === 'uuid'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('state')">Активные задачи <span class="arrow-icon" v-if="sortByField === 'state'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('kwargs')">Отменённые задачи <span class="arrow-icon" v-if="sortByField === 'kwargs'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('result')">Успешные задачи <span class="arrow-icon" v-if="sortByField === 'result'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
        <th class="relative px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6 cursor-pointer" @click="sortBy('received')">Повторные задачи <span class="arrow-icon" v-if="sortByField === 'received'" :class="[sortOrder === 'asc' ? 'arrow-up' : 'arrow-down']"></span></th>
      </tr>
    </thead>

  </template>

<script setup>
import { defineProps, defineEmits, inject } from 'vue';

const props = defineProps({
  sortByField: String,
  sortOrder: String,
  currentPage: Number,
  currentTable: String
});

const currentTable = inject('currentTable');

const emits = defineEmits(['sortedData']);

const sortBy = (field) => {
  let newSortOrder;
  if (field === props.sortByField) {
    newSortOrder = props.sortOrder === 'asc' ? 'desc' : 'asc';
  } else {
    newSortOrder = 'asc';
  }

  emits('sortedData', { sortByField: field, sortOrder: newSortOrder });
};

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