
<script setup lang="ts">
import BaseButton from '@/components/BaseButton.vue'

withDefaults(
  defineProps<{
    titulo: string
    subtitulo: string
    textoBotao?: string
    varianteBotao?: 'contorno' | 'primario' | 'secundario'
  }>(),
  {
    varianteBotao: 'contorno',
  },
)

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <header class="page-header">
    <div class="conteudo">
      <h1>{{ titulo }}</h1>
      <p>{{ subtitulo }}</p>
    </div>

    <BaseButton
      v-if="textoBotao"
      :variante="varianteBotao"
      @click="$emit('click', $event)"
    >
      {{ textoBotao }}
    </BaseButton>
  </header>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
}

.conteudo {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

h1 {
  margin: 0;
  color: var(--color-text);
  font: 600 22px var(--font-family);
}

p {
  margin: 0;
  color: var(--color-text-muted);
  font: 400 12px var(--font-family);
}

@media (max-width: 600px) {
  .page-header {
    flex-direction: column;
  }
}
</style>
