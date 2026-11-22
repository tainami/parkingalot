<script setup lang="ts">

defineEmits<{
    click: []
}>()

</script>

<template>
    <button class="icon-button edit-button" 
            type="button"  
            title="Editar"
            @click="$emit('click')">
        <svg
            viewBox="0 0 24 24"
            class="button-icon"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
        >
            <path d="M12 20h9"/>
            <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L8 18l-4 1 1-4Z"/>
        </svg>


    </button>
</template>

<style scoped>
.icon-button{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    background-color: #FFFFFF;
    border: 1px solid #bfc5ca;
    border-radius: 6px;
    cursor: pointer;
    transition:
    background-color 0.2s ease,
    color 0.2s ease,
    transform 0.15s ease;
}

.edit-button {
    color: #2879E8;
    border-color: #bfc5ca;
}

.edit-button:hover{
    background-color: #2879E8;
    color: #FFFFFF;
}

.edit-button:active{
    transform: scale(1.05);
}

.button-icon{
    width: 18px;
    height: 18px;
}

</style>