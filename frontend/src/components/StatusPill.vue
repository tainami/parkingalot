<script setup lang="ts">
withDefaults(
  defineProps<{
    texto: string
    variante?: 'cinza' | 'azul-claro' | 'laranja' | 'azul' | 'amarelo'
  }>(),
  {
    variante: 'cinza',
  },
)
</script>

<template>
  <span class="status-pill" :class="`status-${variante}`">
    {{ texto }}
  </span>
</template>

<style scoped>
.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 12px;
  border-radius: 20px;
  font: 500 12px var(--font-family);
  white-space: nowrap;
}

.status-cinza {
  background: #e5e7eb;
  color: #4b5563;
}

.status-azul-claro {
  background: #dcecff;
  color: #1e6fd9;
}

.status-laranja {
  background: #ffead5;
  color: #9a4d0b;
}

.status-azul {
  background: #e5efff;
  color: #1e6fd9;
}

.status-amarelo {
  background: #fff2d6;
  color: #8a5a00;
}
</style>