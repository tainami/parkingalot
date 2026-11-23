<script setup lang="ts">
import { RouterLink } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'

defineProps<{
  titulo: string
  subtitulo: string
  erro?: string
}>()
</script>

<template>
  <div class="operacao">
    <RouterLink to="/" class="voltar">Voltar ao mapa</RouterLink>

    <PageHeader :titulo="titulo" :subtitulo="subtitulo" />

    <p v-if="erro" class="erro" role="alert">{{ erro }}</p>

    <section class="card">
      <slot />

      <div v-if="$slots.acoes" class="acoes">
        <slot name="acoes" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.operacao {
  display: flex;
  flex-direction: column;
  gap: 20px;
  color: var(--color-text);
  font-family: var(--font-family);
}

.voltar {
  align-self: flex-start;
  margin-bottom: -8px;
  color: var(--color-primary);
  font: 500 14px var(--font-family);
  text-decoration: none;
}

.voltar:hover {
  text-decoration: underline;
}

.erro {
  margin: 0;
  color: var(--color-error);
  font-size: 13px;
}

.card {
  box-sizing: border-box;
  width: 100%;
  max-width: 704px;
  padding: 24px;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-surface);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.acoes {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}
</style>
