<script setup lang="ts">
import BaseField from '@/components/BaseField.vue'

defineProps<{
  titulo: string
  subtitulo: string
  tituloFormulario: string
  placeholderBusca: string
}>()

const busca = defineModel<string>('busca', { default: '' })
</script>

<template>
  <div class="crud-layout">
    <header>
      <h1>{{ titulo }}</h1>
      <p class="subtitulo">{{ subtitulo }}</p>
    </header>

    <div class="corpo">
      <section class="lista">
        <BaseField v-model="busca" rotulo="Buscar" tipo="search" :placeholder="placeholderBusca" />
        <slot name="tabela" />
      </section>

      <aside class="formulario">
        <h2>{{ tituloFormulario }}</h2>
        <slot name="formulario" />
      </aside>
    </div>
  </div>
</template>

<style scoped>
.crud-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding: 8px 4px;
}

h1 {
  margin: 0;
  color: var(--color-text);
  font: 600 28px var(--font-family);
}

.subtitulo {
  margin: 8px 0 0;
  color: var(--color-text-muted);
  font: 400 14px var(--font-family);
}

.corpo {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: flex-start;
}

.lista {
  flex: 999 1 560px;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.formulario {
  box-sizing: border-box;
  flex: 1 1 300px;
  max-width: 300px;
  padding: 22px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

@media (max-width: 960px) {
  .formulario {
    max-width: none;
  }
}

h2 {
  margin: 0 0 4px;
  color: var(--color-text);
  font: 600 18px var(--font-family);
}
</style>
