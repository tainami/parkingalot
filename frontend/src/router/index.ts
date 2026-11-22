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
        },
        {
          path: '/guardas',
          component:()=>import('@/views/GuardasView.vue')
        },
        {
          path: '/colaboradores',
          component: () => import('@/views/ColaboradoresView.vue')
        },
        {
          path: '/vagas',
          component:()=>import('@/views/VagasView.vue')
        }

      ]
    },
    {
      path: '/login', 
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/redefinir-senha',
      component: () => import('@/views/RedefinirSenhaView.vue')
    }
  ],

})

export default router
