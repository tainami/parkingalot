<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'
import BaseField from '@/components/BaseField.vue'
import DataTable from '@/components/DataTable.vue'
import { listarPagamentos, type Pagamento } from '@/services/pagamentos'
import { listarRegistros, type Registro } from '@/services/registros'
import { listarVeiculos, type Veiculo } from '@/services/veiculos'
import { formatarDataEHora, formatarMoeda, formatarPermanencia } from '@/utils/formatar'

const columns = ['ID', 'Registro', 'Placa', 'Documento', 'Permanência', 'Valor', 'Data e hora']

const route = useRoute()

const busca = ref('')

const pagamentos = ref<Pagamento[]>([])
const registros = ref(new Map<number, Registro>())
const veiculos = ref(new Map<string, Veiculo>())

const erro = ref('')

const linhas = computed(() =>
  [...pagamentos.value]
    .sort((a, b) => b.id_pagamento - a.id_pagamento)
    .map((pagamento) => {
      const registro = registros.value.get(pagamento.id_registro)
      const veiculo = registro ? veiculos.value.get(registro.placa) : undefined

      return {
        ID: `#${pagamento.id_pagamento}`,
        Registro: `#${pagamento.id_registro}`,
        Placa: registro?.placa ?? '—',
        Documento: veiculo?.documento_responsavel ?? '—',
        Permanência: registro?.data_saida
          ? formatarPermanencia(registro.data_entrada, registro.data_saida)
          : '—',
        Valor: formatarMoeda(pagamento.valor),
        'Data e hora': formatarDataEHora(pagamento.data_pagamento, pagamento.hora_pagamento),
      }
    }),
)

const linhasFiltradas = computed(() => {
  const termo = busca.value.trim().toUpperCase().replace(/^#/, '')
  if (!termo) return linhas.value

  return linhas.value.filter(
    (linha) => linha.Registro === `#${termo}` || linha.Placa.includes(termo),
  )
})

watch(
  () => route.query.busca,
  (valor) => {
    busca.value = typeof valor === 'string' ? valor : ''
  },
  { immediate: true },
)

onMounted(async () => {
  try {
    const [listaPagamentos, listaRegistros, listaVeiculos] = await Promise.all([
      listarPagamentos(),
      listarRegistros(),
      listarVeiculos(),
    ])

    pagamentos.value = listaPagamentos
    registros.value = new Map(listaRegistros.map((r) => [r.id_registro, r]))
    veiculos.value = new Map(listaVeiculos.map((v) => [v.placa, v]))
  } catch (e) {
    const resposta = (e as { response?: { data?: { error?: string } } }).response
    erro.value = resposta?.data?.error || 'Erro ao carregar pagamentos.'
  }
})
</script>

<template>
  <div class="pagamentos">
    <PageHeader
      titulo="Pagamentos"
      subtitulo="Gerados automaticamente quando um terceiro sai. Esta tela é só de consulta."
    />

    <BaseField
      v-model="busca"
      rotulo="Buscar por registro ou placa"
      tipo="search"
      placeholder="#55 ou HGT4R11"
      class="busca"
    />

    <p v-if="erro" class="erro">{{ erro }}</p>

    <DataTable :columns="columns" :rows="linhasFiltradas" :mostrar-acoes="false">
      <template #celula="{ coluna, valor, row }">
        <span v-if="coluna === 'ID' || coluna === 'Data e hora'" class="apagado">{{ valor }}</span>
        <RouterLink
          v-else-if="coluna === 'Registro'"
          :to="{ path: '/registros', query: { placa: row.Placa } }"
          class="link"
        >
          {{ valor }}
        </RouterLink>
        <strong v-else-if="coluna === 'Placa' || coluna === 'Valor'">{{ valor }}</strong>
        <template v-else>{{ valor }}</template>
      </template>
    </DataTable>
  </div>
</template>

<style scoped>
.pagamentos {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.busca {
  width: 360px;
  max-width: 100%;
}

.apagado {
  color: var(--color-text-muted);
}

.link {
  color: var(--color-primary);
  font-weight: 500;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.erro {
  margin: 0;
  color: var(--color-error);
  font: 400 13px var(--font-family);
}
</style>
