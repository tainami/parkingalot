<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, useTemplateRef, watch } from 'vue'
import ParkingSpot from '@/components/ParkingSpot.vue'
import type { FiltroVagas, VagaMapa } from '@/types/mapa'

const props = withDefaults(
  defineProps<{
    vagas: VagaMapa[]
    filtro?: FiltroVagas
    vagasPorFileira?: number
  }>(),
  {
    filtro: 'todas',
    vagasPorFileira: 8,
  },
)

const selecionada = defineModel<number | null>('selecionada', { default: null })

const vagasPorNumero = computed(() => new Map(props.vagas.map((v) => [v.numero, v])))

const gradeColunas = computed(() => `repeat(${props.vagasPorFileira}, minmax(48px, 1fr))`)

type Celula = { tipo: 'vaga'; vaga: VagaMapa } | { tipo: 'vazio' }

const linhas = computed(() => {
  const ordenadas = [...props.vagas].sort((a, b) => a.numero - b.numero)
  const resultado: Celula[][] = []

  for (let i = 0; i < ordenadas.length; i += props.vagasPorFileira) {
    const fileira: Celula[] = ordenadas
      .slice(i, i + props.vagasPorFileira)
      .map((vaga) => ({ tipo: 'vaga', vaga }))
    while (fileira.length < props.vagasPorFileira) fileira.push({ tipo: 'vazio' })
    resultado.push(fileira)
  }

  return resultado
})

function estaOculta(vaga: VagaMapa) {
  if (props.filtro === 'todas') return false
  const livre = vaga.estado === 'livre'
  return props.filtro === 'livre' ? !livre : livre
}

function alternar(numero: number) {
  selecionada.value = selecionada.value === numero ? null : numero
}

watch([() => props.filtro, vagasPorNumero], () => {
  if (selecionada.value === null) return
  const vaga = vagasPorNumero.value.get(selecionada.value)
  if (!vaga || estaOculta(vaga)) selecionada.value = null
})

function aoTeclar(evento: KeyboardEvent) {
  if (evento.key !== 'Escape' || selecionada.value === null || evento.defaultPrevented) return
  selecionada.value = null
}

onMounted(() => window.addEventListener('keydown', aoTeclar))
onBeforeUnmount(() => window.removeEventListener('keydown', aoTeclar))

const mapa = useTemplateRef<HTMLDivElement>('mapa')

function focarVaga(numero: number) {
  mapa.value?.querySelector<HTMLButtonElement>(`[aria-label="Vaga ${numero}"]`)?.focus()
}

defineExpose({ focarVaga })
</script>

<template>
  <div ref="mapa" class="mapa">
    <div class="grade">
      <div
        v-for="(linha, indice) in linhas"
        :key="indice"
        class="linha"
        :style="{ gridTemplateColumns: gradeColunas }"
      >
        <template v-for="(celula, i) in linha" :key="i">
          <ParkingSpot
            v-if="celula.tipo === 'vaga'"
            :numero="celula.vaga.numero"
            :estado="celula.vaga.estado"
            :selecionada="selecionada === celula.vaga.numero"
            :esmaecida="selecionada !== null && selecionada !== celula.vaga.numero"
            :oculta="estaOculta(celula.vaga)"
            @click="alternar"
          />
          <span v-else aria-hidden="true" />
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mapa {
  overflow-x: auto;
}

.grade {
  min-width: max-content;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.linha {
  display: grid;
  gap: 8px;
  align-items: center;
}
</style>
