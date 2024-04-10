<template>
    <div class="flex flex-col sm:flex-row justify-between items-center mb-4">
      <div class="relative mb-2">
        <label for="items-per-page">Количество элементов:</label>
        <input id="items-per-page"
               :value="selectedItem"
               @input="updateSelectedItem"
               @change="emitSelectedItem"
               @focus="isOpen = true"
               @blur="isOpen = false"
               class="w-24 sm:w-32 text-center py-2 rounded-md border border-gray-300 appearance-none transition duration-300 ease-in-out cursor-pointer">
        <transition name="slide-fade">
            <ul v-if="isOpen"
            class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-300 rounded shadow-md pointer-events-auto z-10">
            <li v-for="option in options"
                :key="option.value"
                @click="selectItem(option.value)"
                class="cursor-pointer hover:bg-gray-100 rounded px-2 py-1">{{ option.label }}</li>
          </ul>
        </transition>
      </div>
  
      <div class="relative w-full sm:w-auto">
        <input type="text"
               :value="searchQuery"
               @input="updateSearchQuery"
               placeholder="Поиск..."
               class="px-2 py-1 border border-gray-300 rounded-md rounded-l-none pr-8 w-full sm:w-64 shadow-md transition-shadow transition-colors duration-300 focus:outline-none focus:border-blue-100 focus:bg-gray-800 focus:shadow-lg focus:text-white">
        <svg xmlns="http://www.w3.org/2000/svg"
             class="absolute right-2 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400"
             fill="none"
             viewBox="0 0 24 24"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l5-5m0 0l-5-5m5 5H4"/>
        </svg>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      selectedItem: {
        type: String,
        required: true,
      },
      searchQuery: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        isOpen: false,
        options: [
          { value: '10', label: '10' },
          { value: '15', label: '15' },
          { value: '25', label: '25' },
        ],
      };
    },
    methods: {
      updateSelectedItem(event) {
        const newValue = event.target.value;
        this.$emit('update:selectedItem', event.target.value);
        this.isOpen = false;
      },
      updateSearchQuery(event) {
        this.$emit('update:searchQuery', event.target.value);
      },
      selectItem(value) {
        this.$emit('update:selectedItem', value);
        this.isOpen = false;
      },
      emitSelectedItem() {
      this.$emit('selected-item-changed', this.selectedItem);
    }
    },
  };
  </script>
  