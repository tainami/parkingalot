<script setup lang="ts">
import { useId } from 'vue'

withDefaults(
  defineProps<{
    rotulo: string
    opcoes: { valor: string; texto: string }[]
    placeholder?: string
    obrigatorio?: boolean
    dica?: string
    disabled?: boolean
  }>(),
  {
    placeholder: 'Selecione',
    obrigatorio: false,
    disabled: false,
  },
)

const valor = defineModel<string>({ default: '' })
const id = useId()
</script>

<template>
  <div class="campo">
    <label class="rotulo" :for="id">
      {{ rotulo }}
      <span v-if="obrigatorio" class="obrigatorio">*</span>
    </label>

    <select :id="id" v-model="valor" :required="obrigatorio" :disabled="disabled">
      <option value="" disabled>{{ placeholder }}</option>
      <option v-for="opcao in opcoes" :key="opcao.valor" :value="opcao.valor">
        {{ opcao.texto }}
      </option>
    </select>

    <span v-if="dica" class="dica">{{ dica }}</span>
  </div>
</template>

<style scoped>
.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rotulo {
  color: var(--color-text-soft);
  font: 600 13px var(--font-family);
}

.dica {
  color: var(--color-text-muted);
  font: 400 12px var(--font-family);
  line-height: 1.5;
}

.obrigatorio {
  color: #dc3545;
}

select {
  box-sizing: border-box;
  width: 100%;
  height: var(--control-height);
  padding: 0 36px 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface)
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%235b6573' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E")
    no-repeat right 12px center;
  color: var(--color-text);
  font: 400 14px var(--font-family);
  appearance: none;
  cursor: pointer;
  outline: none;
}

select:focus {
  border-color: var(--color-primary);
}

select:disabled {
  background-color: var(--color-bg);
  cursor: not-allowed;
  opacity: 0.6;
}
</style>
