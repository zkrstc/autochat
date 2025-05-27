<template>
  <div class="min-h-screen w-full bg-gray-50 flex items-center justify-center bg-image">
        <div class="bg-white p-8 rounded-lg shadow-xl w-[420px] relative">
            <div class="text-center mb-8">
                <!-- <img src="https://ai-public.mastergo.com/ai/img_res/726384cc65a0f97c97beb2433acac92d.jpg" alt="公司标志"
                    class="w-16 h-16 mx-auto mb-4 object-cover"> -->
                <h2 class="text-2xl font-bold text-gray-800">欢迎登录</h2>
                <p class="text-gray-500 mt-2">登录后开启您的专属服务</p>
            </div>
    <div class="space-y-6">
      <div class="relative">
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="用户名/手机号"
          class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:border-primary text-sm"
        />
        <i
          class="fas fa-times-circle absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 cursor-pointer"
          :class="{ hidden: !username }"
          @click="clearUsername"
        ></i>
      </div>
  
      <div class="relative">
        <input
          :type="showPassword ? 'text' : 'password'"
          id="password"
          v-model="password"
          placeholder="请输入密码"
          class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:border-primary text-sm"
        />
        <i
          class="fas cursor-pointer absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
          :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"
          @click="togglePassword"
        ></i>
      </div>
  
      <div class="flex items-center justify-between text-sm">
        <label class="flex items-center space-x-2 cursor-pointer">
          <input
            type="checkbox"
            id="rememberPassword"
            v-model="rememberPassword"
            class="rounded text-primary"
          />
          <span class="text-gray-600">记住密码</span>
        </label>
        <a href="#" class="text-primary hover:text-blue-600">忘记密码？</a>
      </div>
  
      <button
        @click="handleLogin"
        class="w-full bg-primary text-white py-3 rounded-lg hover:bg-blue-600 transition-colors !rounded-button whitespace-nowrap"
      >
        登录
      </button>
  
      <div class="text-center">
        <p class="text-gray-500 text-sm">
          还没有账号？
          <a href="#" class="text-primary hover:text-blue-600">立即注册</a>
        </p>
      </div>
    </div>
  </div>
</div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import axios from "axios";
  import { useRouter } from 'vue-router'

const router = useRouter()
  const username = ref("");
  const password = ref("");
  const rememberPassword = ref(false);
  const showPassword = ref(false);
  
  const clearUsername = () => {
    username.value = "";
  };
  
  const togglePassword = () => {
    showPassword.value = !showPassword.value;
  };
  
  const handleLogin = async () => {
    if (!username.value || !password.value) {
      alert("请输入用户名和密码");
      return;
    }
  
    try {
      const response = await axios.post("/api/login", {
        username: username.value,
        password: password.value,
        rememberPassword: rememberPassword.value,
      });
  
      if (response.data.message === "登录成功") {
        router.push('/requirements')

        // 登录成功后的处理
        console.log("登录成功");
      } else {
        // 登录失败的处理
        console.log("登录失败");
      }
    } catch (error) {
      console.error("登录请求失败:", error);
    }
  };
  </script>
  