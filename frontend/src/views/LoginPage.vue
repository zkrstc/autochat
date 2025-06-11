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
            <a href="#" @click.prevent="showRegister = true" class="text-primary hover:text-blue-600">立即注册</a>
  
          </p>
        </div>
      </div>
    </div>
  </div>
    <!-- 注册弹窗 -->
  <div
    v-if="showRegister"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-lg p-6 w-96 shadow-lg relative">
      <h2 class="text-xl font-semibold text-gray-800 mb-4">注册新账号</h2>
  
      <input
        v-model="registerUsername"
        type="text"
        placeholder="请输入用户名"
        class="w-full mb-3 p-2 border rounded"
      />
      <input
        v-model="registerPassword"
        type="password"
        placeholder="请输入密码"
        class="w-full mb-4 p-2 border rounded"
      />
  
      <div class="flex justify-end space-x-3">
        <button @click="showRegister = false" class="px-4 py-2 text-gray-600 border rounded">取消</button>
        <button @click="submitRegister" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">注册</button>
      </div>
  
      <p class="text-sm text-red-500 mt-2" v-if="registerError">{{ registerError }}</p>
      <p class="text-sm text-green-500 mt-2" v-if="registerSuccess">{{ registerSuccess }}</p>
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
        const response = await axios.post("http://127.0.0.1:5000/api/login", {
          username: username.value,
          password: password.value,
          rememberPassword: rememberPassword.value,
        });

        // 存储到 localStorage
        localStorage.setItem('user', JSON.stringify({
          id: response.data.user_id,
          username: response.data.username
        }));
        
        if (response.data.message === "Login successful") {
          router.push('/requirements')
  
          // 登录成功后的处理
          console.log("Login successful");
        } else {
          // 登录失败的处理
          console.log("登录失败");
        }
      } catch (error) {
        console.error("登录请求失败:", error);
      }
    };
    const showRegister = ref(false)
  const registerUsername = ref('')
  const registerPassword = ref('')
  const registerError = ref('')
  const registerSuccess = ref('')
  
  const submitRegister = async () => {
    registerError.value = ''
    registerSuccess.value = ''
  
    if (!registerUsername.value || !registerPassword.value) {
      registerError.value = '请输入用户名和密码'
      return
    }
  
    try {
      const response = await axios.post('/api/register', {
        username: registerUsername.value,
        password: registerPassword.value
      })
  
      if (response.data.message === 'Register successful') {
        registerSuccess.value = '注册成功！请返回登录'
        setTimeout(() => {
          showRegister.value = false
          registerUsername.value = ''
          registerPassword.value = ''
        }, 1500)
      }
    } catch (err) {
      registerError.value = err.response?.data?.error || '注册失败'
    }
  }
  
    </script>