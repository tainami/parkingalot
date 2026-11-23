<script setup lang="ts">
import type { EstadoVaga } from '@/types/mapa'

withDefaults(
  defineProps<{
    numero: number
    estado: EstadoVaga
    selecionada?: boolean
    esmaecida?: boolean
    oculta?: boolean
  }>(),
  {
    selecionada: false,
    esmaecida: false,
    oculta: false,
  },
)

defineEmits<{
  click: [numero: number]
}>()
</script>

<template>
  <button
    type="button"
    class="vaga"
    :class="[estado, { selecionada, esmaecida, oculta }]"
    :aria-label="`Vaga ${numero}`"
    :aria-pressed="selecionada"
    :tabindex="oculta ? -1 : undefined"
    @click="$emit('click', numero)"
  >
    {{ numero }}
  </button>
</template>

<style scoped>
.vaga {
  aspect-ratio: 62 / 44;
  min-height: 36px;
  max-height: 72px;
  padding: 0;
  border: 0;
  border-radius: 6px;
  font: 500 13px var(--font-family);
  cursor: pointer;
  transition: opacity 0.15s;
}

.livre {
  background: var(--color-vaga-livre);
  color: var(--color-text);
}

.colaborador {
  background: var(--color-vaga-colaborador);
  color: var(--color-surface);
}

.selecionada {
  font-weight: 700;
}

.colaborador.selecionada {
  background: var(--color-primary);
}

.terceiro {
  background: var(--color-vaga-terceiro);
  color: var(--color-text);
}

.esmaecida {
  opacity: 0.3;
}

.oculta {
  opacity: 0.08;
  pointer-events: none;
}

.vaga:focus-visible {
  outline: 3px solid var(--color-text);
  outline-offset: 2px;
}
</style>
