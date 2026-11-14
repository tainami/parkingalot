import { ref } from 'vue'
import { defineStore } from 'pinia'

import { listarVagas, type Vaga } from '@/services/vagas'

export const useVagasStore = defineStore('vagas', () => {
  const vagas = ref<Vaga[]>([])

  async function carregar() {
    vagas.value = await listarVagas()
  }

  return { vagas, carregar }
})
