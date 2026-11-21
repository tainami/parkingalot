<script setup lang="ts">
import type { EstadoVaga } from '@/types/mapa'

withDefaults(
  defineProps<{
    codigo: string
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
  click: [codigo: string]
}>()
</script>

<template>
  <button
    type="button"
    class="vaga"
    :class="[estado, { selecionada, esmaecida, oculta }]"
    :aria-label="`Vaga ${codigo}`"
    :aria-pressed="selecionada"
    :tabindex="oculta ? -1 : undefined"
    @click="$emit('click', codigo)"
  >
    <template v-if="selecionada">{{ codigo }}</template>
  </button>
</template>

<style scoped>
.vaga {
  height: 44px;
  padding: 0;
  border: 0;
  border-radius: 6px;
  font: 600 13px var(--font-family);
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
