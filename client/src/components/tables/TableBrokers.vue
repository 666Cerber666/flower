<template>
    <div class="p-4">
      <TableHead :selectedItem="selectedItem" :searchQuery="searchQuery" @update:selectedItem="updateSelectedItem" @update:searchQuery="updateSearchQuery"/>
  
      <div class="overflow-x-auto">
        <table class="w-full border-collapse border">
          <thead class="bg-gray-200">
            <tr>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Name</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">UUID</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">State</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Args</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Kwargs</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Result</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Received</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Started</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Runtime</th>
              <th class="px-4 py-2 sm:py-3 md:py-4 lg:py-5 xl:py-6">Worker</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in filteredData" :key="index" :class="{ 'bg-gray-800 text-white': index % 2 !== 0 }">
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
  
  <script>
import TableHead from '../TableHead.vue';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/vue/20/solid'

export default {
  data() {
    return {
      data: [
        { name: 'Broker 1', uuid: 'UUID 1', state: 'completed', args: 'Args 1', kwargs: 'Kwargs 1', result: 'Result 1', received: 'Received 1', started: 'Started 1', runtime: 'Runtime 1', worker: 'Worker 1' },
        { name: 'Broker 2', uuid: 'UUID 2', state: 'in progress', args: 'Args 2', kwargs: 'Kwargs 2', result: 'Result 2', received: 'Received 2', started: 'Started 2', runtime: 'Runtime 2', worker: 'Worker 2' },
        { name: 'Broker 3', uuid: 'UUID 3', state: 'not completed', args: 'Args 3', kwargs: 'Kwargs 3', result: 'Result 3', received: 'Received 3', started: 'Started 3', runtime: 'Runtime 3', worker: 'Worker 3' }
      ],
      selectedItem: '10',
      searchQuery: '',
      sortByField: '', // Field to sort by
      sortOrder: 'asc' // Sort order (asc/desc)
    };
  },
  components: {
    TableHead,
  },
  computed: {
    filteredData() {
      // Sort data based on selected field and order
      let sortedData = [...this.data];
      if (this.sortByField) {
        sortedData.sort((a, b) => {
          let fieldA = a[this.sortByField].toLowerCase();
          let fieldB = b[this.sortByField].toLowerCase();
          if (fieldA < fieldB) return this.sortOrder === 'asc' ? -1 : 1;
          if (fieldA > fieldB) return this.sortOrder === 'asc' ? 1 : -1;
          return 0;
        });
      }
      return sortedData.filter(item =>
        Object.values(item).some(value =>
          String(value).toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      ).slice(0, this.selectedItem);
    }
  },
  methods: {
    getExecutionStatus(state) {
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
    },
    getStatusClass(state) {
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
    },
    updateSelectedItem(value) {
      this.selectedItem = value;
      this.$emit('selected-item-changed', value);
    },

    updateSearchQuery(searchQuery) {
      this.searchQuery = searchQuery;
    },
    sortBy(field) {
      // Toggle sort order if same field is clicked twice
      if (field === this.sortByField) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortOrder = 'asc';
      }
      this.sortByField = field;

      // Add animation class to rotate the arrow
      const arrow = document.getElementById(`arrow-${field}`);
      arrow.classList.add('rotate-arrow');
      // Remove animation class after animation ends
      setTimeout(() => {
        arrow.classList.remove('rotate-arrow');
      }, 500); // Adjust the duration of animation if needed
    }
  }
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