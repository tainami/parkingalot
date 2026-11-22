<script setup lang="ts">
withDefaults(
  defineProps<{
    rotulo: string
    placeholder?: string
    maxlength?:number
    modelValue?: string
    tipo?: 'text' | 'email' | 'password' | 'number' | 'search'
    disabled?: boolean
    obrigatorio?: boolean
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
  </div>
</template>

<style scoped>
.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rotulo {
  color: var(--color-text-muted);
  font: 500 12px var(--font-family);
}

.obrigatorio {
  color: #dc3545;
}

input {
  width: 100%;
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-surface);
  color: var(--color-text);
  font: 400 12px var(--font-family);
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