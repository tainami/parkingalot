<script setup lang="ts">
withDefaults(
  defineProps<{
    rotulo: string
    placeholder?: string
    maxlength?:number
    modelValue?: string
    tipo?: 'text' | 'email' | 'password' | 'number' | 'search' | 'date'
    disabled?: boolean
    obrigatorio?: boolean
    dica?: string
  }>(),
  {
    placeholder: 'Digite aqui',
    modelValue: '',
    tipo: 'text',
    disabled: false,
    obrigatorio: false,
  },
)

defineEmits<{
  'update:modelValue': [valor: string]
}>()
</script>

<template>
  <div class="campo">
    <label class="rotulo">
      {{ rotulo }}
      <span v-if="obrigatorio" class="obrigatorio">*</span>
    </label>

    <input
      :type="tipo"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      :maxlength="maxlength"
      :required="obrigatorio"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />

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

input {
  width: 100%;
  height: var(--control-height);
  padding: 0 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  color: var(--color-text);
  font: 400 14px var(--font-family);
  outline: none;
  box-sizing: border-box;
}

input::placeholder {
  color: #7b8494;
}

input:focus {
  border-color: var(--color-primary);
}

input:disabled {
  background: var(--color-bg);
  cursor: not-allowed;
  opacity: 0.6;
}
</style>