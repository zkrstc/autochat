<template>
    <header class="bg-white shadow-sm">
                <div class="flex justify-between items-center px-8 py-4">
                    <div class="text-xl font-medium">架构设计</div>
                    <div class="relative">
                        <button class="flex items-center space-x-3 !rounded-button">
                            <img src="https://ai-public.mastergo.com/ai/img_res/c7de0a2547793954cd19a41b0e9ca26a.jpg"
                                class="w-10 h-10 rounded-full object-cover" alt="用户头像">
                            <span class="text-gray-700">陈志远</span>
                            <i class="fas fa-chevron-down text-gray-400 text-sm"></i>
                        </button>
                        <div class="absolute right-0 mt-2 w-48 bg-white rounded shadow-lg py-2 hidden">
                            <a href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                                <i class="fas fa-user mr-2"></i>个人设置
                            </a>
                            <a href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                                <i class="fas fa-bell mr-2"></i>消息通知
                            </a>
                            <a href="#" class="block px-4 py-2 text-gray-700 hover:bg-gray-100">
                                <i class="fas fa-sign-out-alt mr-2"></i>退出登录
                            </a>
                        </div>
                    </div>
                </div>
            </header>
  </template>
  
  <script setup>
import { onMounted } from 'vue';

onMounted(() => {
  const button = document.querySelector('button:has(img)');
  const dropdown = document.querySelector('.absolute.right-0');

  if (button && dropdown) {
    button.addEventListener('click', function () {
      dropdown.classList.toggle('hidden');
    });
  }
});
  </script>
  
  <style scoped>
  /* 这里可以添加一些样式 */
  </style>
  