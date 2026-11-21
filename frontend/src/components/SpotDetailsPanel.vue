<script setup lang="ts">
import BaseButton from '@/components/BaseButton.vue'
import StatusPill from '@/components/StatusPill.vue'
import type { Movimentacao, OcupacaoVaga, VagaMapa } from '@/types/mapa'

withDefaults(
  defineProps<{
    vaga?: VagaMapa | null
    ocupacao?: OcupacaoVaga | null
    totalVagas: number
    vagasOcupadas: number
    movimentacoes?: Movimentacao[]
  }>(),
  {
    vaga: null,
    ocupacao: null,
    movimentacoes: () => [],
  },
)

defineEmits<{
  limparSelecao: []
  registrarEntrada: [codigo: string]
  registrarSaida: [codigo: string]
}>()
</script>

<template>
  <aside class="painel" aria-label="Detalhes da vaga">
    <template v-if="!vaga">
      <div>
        <p class="rotulo">Pátio agora</p>
        <p class="destaque">{{ vagasOcupadas }} de {{ totalVagas }} vagas ocupadas</p>
      </div>
      <p class="dica">Clique em uma vaga ou busque pela placa para ver os detalhes.</p>
    </template>

    <template v-else>
      <div class="topo">
        <div class="linha">
          <p class="rotulo">Vaga selecionada</p>
          <button type="button" class="limpar" @click="$emit('limparSelecao')">Limpar seleção</button>
        </div>
        <div class="linha titulo">
          <p class="destaque">Vaga {{ vaga.codigo }}</p>
          <StatusPill
            :texto="vaga.estado === 'livre' ? 'Livre' : 'Ocupada'"
            :variante="vaga.estado === 'livre' ? 'cinza' : 'azul-claro'"
          />
        </div>
      </div>

      <template v-if="vaga.estado !== 'livre'">
        <dl v-if="ocupacao" class="dados">
          <dt>Placa</dt>
          <dd class="negrito">{{ ocupacao.placa }}</dd>
          <dt>Veículo</dt>
          <dd>{{ ocupacao.veiculo }}</dd>
          <dt>Vínculo</dt>
          <dd>{{ ocupacao.vinculo }}</dd>
          <dt>Responsável</dt>
          <dd>{{ ocupacao.responsavel }}</dd>
          <dt>Entrada</dt>
          <dd>{{ ocupacao.entrada }}</dd>
          <dt>Guarda</dt>
          <dd>{{ ocupacao.guarda }}</dd>
        </dl>
        <p v-if="vaga.estado === 'terceiro'" class="aviso">
          Veículo de terceiro: o pagamento é calculado automaticamente ao registrar a saída.
        </p>
        <BaseButton variante="contorno" class="largo" @click="$emit('registrarSaida', vaga.codigo)">
          Registrar saída
        </BaseButton>
      </template>

      <template v-else>
        <p class="texto">Esta vaga está disponível. Registre a entrada de um veículo para ocupá-la.</p>
        <BaseButton variante="contorno" class="largo" @click="$emit('registrarEntrada', vaga.codigo)">
          Registrar entrada
        </BaseButton>
      </template>
    </template>

    <template v-if="movimentacoes.length">
      <hr class="divisor" />
      <p class="subtitulo">Últimas movimentações</p>
      <ul class="movimentacoes">
        <li v-for="m in movimentacoes" :key="`${m.placa}-${m.hora}`">
          <span><strong>{{ m.placa }}</strong> <span class="apagado">{{ m.descricao }}</span></span>
          <span class="apagado">{{ m.hora }}</span>
        </li>
      </ul>
    </template>
  </aside>
</template>

<style scoped>
.painel {
  box-sizing: border-box;
  padding: 24px;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  background: var(--color-surface);
  box-shadow: 0 6px 24px rgba(27, 37, 89, 0.08);
  display: flex;
  flex-direction: column;
  gap: 18px;
  font-family: var(--font-family);
  color: var(--color-text);
}

p {
  margin: 0;
}

.rotulo {
  color: var(--color-text-muted);
  font-size: 12px;
  font-weight: 500;
}

.destaque {
  font-size: 22px;
  font-weight: 600;
}

.dica {
  padding: 12px 14px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  color: var(--color-text-soft);
  font-size: 13px;
  line-height: 1.5;
}

.topo {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.linha {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.titulo {
  justify-content: flex-start;
  flex-wrap: wrap;
}

.limpar {
  margin-right: -6px;
  padding: 4px 6px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  color: var(--color-primary);
  font: 500 13px var(--font-family);
  white-space: nowrap;
  cursor: pointer;
}

.limpar:hover {
  color: var(--color-primary-hover);
  text-decoration: underline;
}

.limpar:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.dados {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 10px 12px;
  margin: 0;
  font-size: 14px;
}

.dados dt {
  color: var(--color-text-muted);
}

.dados dd {
  margin: 0;
}

.negrito {
  font-weight: 600;
}

.aviso {
  padding: 12px 14px;
  border-radius: var(--radius-md);
  background: var(--color-aviso-bg);
  color: var(--color-aviso-text);
  font-size: 13px;
  line-height: 1.5;
}

.texto {
  color: var(--color-text-soft);
  font-size: 14px;
  line-height: 1.6;
}

.largo {
  width: 100%;
}

.divisor {
  height: 1px;
  margin: 0;
  border: 0;
  background: var(--color-border);
}

.subtitulo {
  color: var(--color-text-soft);
  font-size: 13px;
  font-weight: 600;
}

.movimentacoes {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
  font-size: 13px;
}

.movimentacoes li {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.apagado {
  color: var(--color-text-muted);
}
</style>
