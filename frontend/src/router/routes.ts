import { RouteRecordRaw } from 'vue-router'
import { useUserStore } from 'src/stores/UserStore'

const routes: RouteRecordRaw[] = [
  {
    path: '',
    redirect: () => {
      const { user } = useUserStore()
      if (user.username === 'admin') {
        return { name: 'Admin' }
      }
      return { name: 'User' }
    },
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '/user',
        name: 'User',
        component: () => import('pages/UserPage.vue')
      },
      {
        path: '/admin',
        name: 'Admin',
        component: () => import('pages/AdminPage.vue')
      }
    ]
  },
  {
    path: '',
    redirect: { name: 'User' },
    component: () => import('layouts/BaseLayout.vue'),
    children: [
      {
        name: 'Login',
        path: '/login',
        component: () => import('pages/LoginPage.vue')
      },
      {
        name: 'TG',
        path: '/tg-chat',
        component: () => import('pages/RedirectPage.vue')
      },
      {
        path: '/:catchAll(.*)*',
        component: () => import('pages/MissingPage.vue')
      }
    ]
  }
]

export default routes
