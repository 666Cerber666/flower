import { createApp } from 'vue';
import './style.css';
import './index.css';
import App from './App.vue';
import router from './router'; // Импортируем экземпляр маршрутизатора из файла router.ts

const app = createApp(App);
app.use(router); // Используем маршрутизатор
app.mount('#app');
