<script setup lang="ts">
import AppSideBar from './AppSideBar.vue'
</script>

<template>
    <div class="app-layout">
        <aside class="sidebar-container">
            <AppSideBar />
        </aside>

        <main class="main-content">
            <div class="content-container">
                <RouterView v-slot="{Component}">
                    <Transition name="page" mode="out-in">
                        <component :is="Component"/>
                    </Transition>
                </RouterView>
            </div>
        </main>
    </div>

</template>

<style scoped>

.app-layout {
    box-sizing: border-box;
    display: flex;
    min-height: 100vh;
    width: 100%;
    background-color: #F1F3F7
}

.sidebar-container{
    box-sizing: border-box;
    width: 250px;
    min-width: 200px;
    height: 100vh;
    position: sticky;
    top: 0;
    overflow-y: auto;
    flex-shrink: 0;
    background-color: #FFFF;
    border-right: 1px solid #E5E7EB;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.main-content{
    box-sizing: border-box;
    flex:1;
    min-width: 0;
    padding: 18px 20px;
    
}

.content-container{
    box-sizing: border-box;
    width: 100%;
    min-height: calc(100vh - 36px);
    background-color: #FFFF;
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25);
}

.page-enter-active, .page-leave-active{
    transition: 
    opacity 0.2s ease, 
    transform 0.2s ease;
}

.page-enter-from, .page-leave-to{
    opacity: 0;
    transform: translateY(8px);
}

:deep(.page-enter-active), :deep(.page-leave-active){
    transition:
    opacity 0.3s ease,
    transform 0.3s ease;
}

:deep(.page-enter-from), :deep(.page-leave-to){
    opacity: 0;
    transform: translateY(8px);
}
</style>