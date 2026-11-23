
import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
          component: () => import('@/views/GuardasView.vue')
        },
        {
          path: '/colaboradores',
          component: () => import('@/views/ColaboradoresView.vue')
        },
        {
          path: '/veiculos',
          component: () => import('@/views/VeiculosView.vue')
        },
        {
          path: '/vagas',
          component: () => import('@/views/VagasView.vue')
        },
        {
          path: '/entrada',
          component: () => import('@/views/EntradaView.vue')
        },
        {
          path: '/saida/:idRegistro',
          component: () => import('@/views/SaidaView.vue'),
          props: (rota) => ({ idRegistro: Number(rota.params.idRegistro) })
        },
        {
          path: '/registros',
          component: () => import('@/views/RegistrosView.vue')
        },
        {
          path: '/pagamentos',
          component: () => import('@/views/PagamentosView.vue')
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
  ]
})

const ROTAS_PUBLICAS = ['/login', '/redefinir-senha']

router.beforeEach((rota) => {
  const logado = !!sessionStorage.getItem('token')

  if (!logado && !ROTAS_PUBLICAS.includes(rota.path)) return '/login'
  if (logado && rota.path === '/login') return '/'
})

export default router
