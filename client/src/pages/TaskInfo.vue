<template>
    <Header />
    <div class="p-6 flex flex-row gap-4 w-full overflow-x-auto">
      <div class="flex flex-row-reverse mb-6">
            <button @click="$router.go(-1)" class="w-full h-10 bg-violet-600 hover:bg-violet-900 text-center text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300 flex items-center justify-center">
            <ChevronLeftIcon class="w-10 h-10"/>
            <p class="font-sans font-medium">Назад</p>
        </button>
        </div>
        <div class="w-full">
            <div class="w-4/5 gap-4 grid">
                <div v-for="(value, key, index) in filteredItems" :key="index" class="grid grid-cols-2 p-4 border border-gray-300 rounded-md shadow-md hover:shadow-lg transition duration-300">
                    <div class="sm:w-1/3 border-r-2 border-indigo-500 text-center font-bold p-2">{{ key }} </div>
                    <div class="sm:w-full w-450 text-left rounded-full font-bold p-2">
                        <p class="font-sans font-medium" :class="getTextStatusColor(key)">{{ getFormattedValue(key, value) }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

  <script setup>
  import { ChevronLeftIcon } from '@heroicons/vue/20/solid';
  import { ref, onMounted } from 'vue';
  import { fetchTaskInfo } from '../apiFunctions/api.ts';
  import Header from '../components/Header.vue';
  import './../ComponentsStyle/gridstyles.css';
  import { useRoute } from 'vue-router';
  
  const route = useRoute();
  const filteredItems = ref({});
  const flowerId = route.query.flowerId;
  const taskUuid = route.query.uuid;
  
  const handleError = (error) => {
    console.error(error);
    // Дополнительная обработка ошибок
  };
  
  const filterEmptyValues = (data) => {
    const filtered = {};
    for (const key in data) {
      if (data[key] !== null && data[key] !== undefined && data[key] !== '') {
        filtered[key] = data[key];
      }
    }
    return filtered;
  };
  
  const getStatusClass = (state) => {
    switch (state) {
      case 'SUCCESS':
        return 'border-grid-col-accept';
      case 'STARTED':
        return 'border-grid-col-wait';
      case 'FAILURE':
        return 'border-grid-col-cancel';
      case 'RETRY':
        return 'border-grid-col-wait';
      case 'RECEIVED':
        return 'border-grid-col-rec';
      default:
        return '';
    }
  };
  
  const getTextStatusColor = (key) => {
    switch (key) {
      case 'state':
        return getStatusColor(filteredItems.value[key]);
      case 'timestamp':
        return 'text-indigo-700'; // Цвет для timestamp
      // Добавьте дополнительные случаи для других ключей, если необходимо
      default:
        return '';
    }
  };
  
  const getStatusColor = (state) => {
    switch (state) {
      case 'SUCCESS':
        return 'text-green-500';
      case 'STARTED':
        return 'text-indigo-700';
      case 'FAILURE':
        return 'text-red-500';
      case 'RECEIVED':
        return 'text-yellow-500';
      case 'RETRY':
        return 'text-yellow-500';
      default:
        return '';
    }
  };
  
  const getFormattedValue = (key, value) => {
    switch (key) {
      case 'state':
        return value; // Не требуется форматирование для ключа state
      case 'timestamp':
        return formatTimestamp(value);
    case 'received':
        return formatTimestamp(value);
    case 'started':
        return formatTimestamp(value);
    case 'failed':
        return formatTimestamp(value);
    case 'retried':
        return formatTimestamp(value); // Форматирование для timestamp
      case 'runtime':
        return formatRuntime(value); // Форматирование для runtime
      // Добавьте дополнительные случаи для других ключей, если необходимо
      default:
        return value;
    }
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
  
  const formatRuntime = (runtime) => {
    const hours = Math.floor(runtime / 3600);
    const minutes = Math.floor((runtime % 3600) / 60);
    const seconds = Math.floor(runtime % 60);
    
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  };
  
  onMounted(() => {
    fetchTaskInfo(flowerId, taskUuid)
      .then((data) => {
        filteredItems.value = filterEmptyValues(data);
      })
      .catch((error) => {
        console.error('Error fetching flower tasks:', error);
      });
  });
  </script>
  