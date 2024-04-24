import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Login from './pages/Login.vue';
import Register from './pages/Register.vue';
import Tables from './pages/Tables.vue';
import WorkerTasks from './pages/WorkerTasks.vue';
import Profile from './pages/Profile.vue';
import TaskInfo from './pages/TaskInfo.vue';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false } // Разрешаем доступ всем пользователям
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false } // Разрешаем доступ всем пользователям
  },
  {
    path: '/Tables',
    name: 'Tables',
    component: Tables,
    meta: { requiresAuth: true } // Требуем аутентификацию для доступа
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true } // Разрешаем доступ всем пользователям
  },
  {
    path: '/WorkerTasks',
    name: 'WorkerTasks',
    component: WorkerTasks,
    meta: { requiresAuth: true } // Разрешаем доступ всем пользователям
  },
  {
    path: '/TaskInfo',
    name: 'TaskInfo',
    component: TaskInfo,
    meta: { requiresAuth: true } // Разрешаем доступ всем пользователям
  },
];

const router = createRouter({
  history: createWebHistory('/'),
  routes
});


router.beforeEach((to, from, next) => {
  const role = localStorage.getItem('role');
  // Проверяем требуется ли аутентификация для доступа к маршруту
  if (to.meta.requiresAuth && role !== 'auth') {
    // Если требуется аутентификация и пользователь не авторизован,
    // перенаправляем на страницу входа
    next('/');
  } else {
    // В противном случае, разрешаем доступ
    next();
  }
});

export default router;

