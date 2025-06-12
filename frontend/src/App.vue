<template>
<div class="flex h-screen">
    <Sidebar />
    <main class="flex-1">
    <SelfPage/>
        <div class="p-8">
            <router-view />
        </div>
    </main>
    <ChatbotFloat />
</div>
</template>

<script>
import SelfPage from './components/SelfPage.vue';
import Sidebar from './components/SiderBar.vue';
import ChatbotFloat from './views/ChatbotFloat.vue';
export default {
  name: 'App',
  components: {
    SelfPage,
    Sidebar,
    ChatbotFloat
  }
};
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>