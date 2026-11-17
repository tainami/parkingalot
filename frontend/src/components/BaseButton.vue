
<script setup lang="ts">
withDefaults(
  defineProps<{
    variante?: 'contorno' | 'primario' | 'secundario'
    icone?: boolean
    disabled?: boolean
  }>(),
  {
    variante: 'secundario',
    icone: false,
    disabled: false,
  },
)

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <button
    type="button"
    class="botao"
    :class="variante"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <span v-if="icone" class="icone">+</span>
    <slot />
  </button>
</template>

<style scoped>
.botao {
  min-height: var(--control-height);
  padding: 0 18px;
  border-radius: var(--radius-md);
  font: 500 14px var(--font-family);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: background 0.2s, border-color 0.2s;
}

.icone {
  font-size: 22px;
  font-weight: 300;
  line-height: 1;
}

.primario {
  background: var(--color-primary);
  color: var(--color-surface);
  border: 1px solid var(--color-primary);
}

.primario:hover:not(:disabled) {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
}

.contorno {
  background: var(--color-surface);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}

.contorno:hover:not(:disabled) {
  background: #edf4ff;
}

.secundario {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}

.secundario:hover:not(:disabled) {
  background: var(--color-bg);
}

.botao:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
