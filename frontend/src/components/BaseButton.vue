<script setup lang="ts">
defineProps<{
  variante?: 'primario' | 'secundario'
}>()
</script>

<template>
  <button type="button" class="botao" :class="variante ?? 'secundario'">
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
}

.primario {
  background: var(--color-primary);
  color: var(--color-surface);
  border: 1px solid var(--color-primary);
}

.primario:hover {
  background: var(--color-primary-hover);
}

.secundario {
  background: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
}
</style>
