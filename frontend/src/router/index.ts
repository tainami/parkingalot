import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // TODO: adicionar as rotas conforme as telas forem criadas
  routes: [
    { 
      path: '/', 
      component: AppLayout,
      children: [
        {
          path: '',
          component: () => import('@/views/MapaView.vue')
        }
      ]
    },
    {
      path: '/login', 
      component: () => import('@/views/LoginView.vue')
    },

  ],

})

export default router
