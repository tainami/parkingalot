import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // TODO: adicionar as rotas conforme as telas forem criadas
  routes: [{ path: '/', component: () => import('@/views/MapaView.vue') }],
})

export default router
