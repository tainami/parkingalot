<script setup lang="ts">
import EditButton from './EditButton.vue'
import DeleteButton from './DeleteButton.vue'

withDefaults(defineProps<{
    columns: string[]
    rows: Record<string, any>[]
    mostrarExcluir?: boolean
    mostrarAcoes?: boolean
}>(), {
    mostrarExcluir: true,
    mostrarAcoes: true,
})


defineEmits<{
    editar: [row: any]
    excluir: [row: any]
}>()

</script>

<template>
    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column">
                        {{ column }}
                    </th>
                    <th v-if="mostrarAcoes">Ações</th>
                </tr>
            </thead>

                <tbody>
                    <tr v-for="(row, index) in rows" :key="index">
                        <td v-for="column in columns" :key="column">
                            <slot name="celula" :coluna="column" :valor="row[column]" :row="row">
                            <span
                                v-if="column === 'Status' && ['Ocupada', 'Livre'].includes(row[column])"
                                :class="[
                                    'status-badge',
                                   row[column] === 'Ocupada' ? 'status-ocupada' : 'status-livre'
                                ]"
                            >
                                {{ row[column] }}
                            </span>

                            <template v-else>
                                {{ row[column] }}
                            </template>
                            </slot>
                        </td>
                        <td v-if="mostrarAcoes" class="actions">
                            <EditButton @click="$emit('editar', row)" />
                            <DeleteButton
                             v-if="mostrarExcluir"
                             @click="$emit('excluir', row)" />
                        </td>
                    </tr>

                    <tr v-if="rows.length === 0">
                        <td :colspan="columns.length + (mostrarAcoes ? 1 : 0)" class="no-data">
                            Nenhum dado disponível
                        </td>
                    </tr>
                </tbody>
        </table>
    </div>
</template>

<style scoped>

.table-container{
    width: 100%;
    overflow-x: auto;
    border-radius: 8px;
    border: 1px solid #bfc5ca;
}

.data-table{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.data-table th{
    padding: 14px 16px;
    background-color: #F1F3F7;
    color: #172554;
    font-size: 14px;
    font-weight: 600;
}

.data-table td{
    padding: 14px 16px;
    border-bottom: 1px solid #E5E7EB;
    color: #172554;
    font-size: 14px;
}

.actions{
    white-space: nowrap;
    gap: 8px;
    display: flex;
    align-items: center;
}

.no-data{
    text-align: center;
    color: #64748B;
}

.status-badge{

    display: inline-flex;
    align-items: center;
    padding: 5px 12px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 500;
}

.status-ocupada{
    background-color: #F1F3F5;
    border-color: #d1d5d8;
    color: #4b5563;
}

.status-livre{
    background-color: #eff6ff;
    border-color: #bfd8fe;
    color: var(--color-primary)
}


</style>