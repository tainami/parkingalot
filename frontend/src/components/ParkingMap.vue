<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, watch } from 'vue'
import ParkingSpot from '@/components/ParkingSpot.vue'
import type { FiltroVagas, VagaMapa } from '@/types/mapa'

const props = withDefaults(
  defineProps<{
    vagas: VagaMapa[]
    filtro?: FiltroVagas
  }>(),
  {
    filtro: 'todas',
  },
)

const selecionada = defineModel<string | null>('selecionada', { default: null })

function separarCodigo(codigo: string) {
  const [, fileira = '', coluna = ''] = codigo.match(/^([A-Za-z]+)(\d+)$/) ?? []
  return { fileira: fileira.toUpperCase(), coluna }
}

const vagasPorCodigo = computed(() => new Map(props.vagas.map((v) => [v.codigo.toUpperCase(), v])))

const fileiras = computed(() =>
  [...new Set(props.vagas.map((v) => separarCodigo(v.codigo).fileira))].filter(Boolean).sort(),
)

const colunas = computed(() =>
  [...new Set(props.vagas.map((v) => separarCodigo(v.codigo).coluna))]
    .filter(Boolean)
    .sort((a, b) => Number(a) - Number(b)),
)

const metade = computed(() => Math.ceil(colunas.value.length / 2))
const ladoEsquerdo = computed(() => colunas.value.slice(0, metade.value))
const ladoDireito = computed(() => colunas.value.slice(metade.value))

const gradeColunas = computed(
  () => `24px repeat(${ladoEsquerdo.value.length}, 62px) 40px repeat(${ladoDireito.value.length}, 62px)`,
)

type Celula = { tipo: 'vaga'; vaga: VagaMapa } | { tipo: 'vazio' } | { tipo: 'corredor' }

const linhas = computed(() =>
  fileiras.value.map((fileira) => {
    const celula = (coluna: string): Celula => {
      const vaga = vagasPorCodigo.value.get(`${fileira}${coluna}`)
      return vaga ? { tipo: 'vaga', vaga } : { tipo: 'vazio' }
    }
    const celulas: Celula[] = [
      ...ladoEsquerdo.value.map(celula),
      { tipo: 'corredor' },
      ...ladoDireito.value.map(celula),
    ]
    return { fileira, celulas }
  }),
)

function estaOculta(vaga: VagaMapa) {
  if (props.filtro === 'todas') return false
  const livre = vaga.estado === 'livre'
  return props.filtro === 'livre' ? !livre : livre
}

function alternar(codigo: string) {
  selecionada.value = selecionada.value === codigo ? null : codigo
}

watch([() => props.filtro, vagasPorCodigo], () => {
  if (!selecionada.value) return
  const vaga = vagasPorCodigo.value.get(selecionada.value.toUpperCase())
  if (!vaga || estaOculta(vaga)) selecionada.value = null
})

function aoTeclar(evento: KeyboardEvent) {
  if (evento.key !== 'Escape' || !selecionada.value || evento.defaultPrevented) return
  selecionada.value = null
}

onMounted(() => window.addEventListener('keydown', aoTeclar))
onBeforeUnmount(() => window.removeEventListener('keydown', aoTeclar))
</script>

<template>
  <div class="mapa">
    <div class="grade">
      <div class="linha cabecalho" :style="{ gridTemplateColumns: gradeColunas }">
        <span />
        <span v-for="c in ladoEsquerdo" :key="c">{{ c }}</span>
        <span />
        <span v-for="c in ladoDireito" :key="c">{{ c }}</span>
      </div>

      <div
        v-for="linha in linhas"
        :key="linha.fileira"
        class="linha"
        :style="{ gridTemplateColumns: gradeColunas }"
      >
        <span class="rotulo">{{ linha.fileira }}</span>

        <template v-for="(celula, i) in linha.celulas" :key="i">
          <ParkingSpot
            v-if="celula.tipo === 'vaga'"
            :codigo="celula.vaga.codigo"
            :estado="celula.vaga.estado"
            :selecionada="selecionada === celula.vaga.codigo"
            :esmaecida="!!selecionada && selecionada !== celula.vaga.codigo"
            :oculta="estaOculta(celula.vaga)"
            @click="alternar"
          />
          <span v-else-if="celula.tipo === 'corredor'" class="corredor" aria-hidden="true" />
          <span v-else />
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
  width: max-content;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.linha {
  display: grid;
  gap: 8px;
  align-items: center;
}

.cabecalho,
.rotulo {
  color: var(--color-text-muted);
  font: 500 12px var(--font-family);
  text-align: center;
}

.cabecalho {
  height: 20px;
}

.corredor {
  width: 1.5px;
  height: 52px;
  margin: -4px auto;
  background: var(--color-corredor);
}
</style>
