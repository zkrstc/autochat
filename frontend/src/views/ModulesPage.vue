<template>
   <div class="p-8">
                <div class="flex items-center mb-6 space-x-4">
                    <div class="text-lg font-medium">需求选择：</div>
                    <select id="projectSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="updateModules()">
                        <option value="1">智能客服系统 v1.0</option>
                        <option value="2">数据分析平台 v2.0</option>
                        <option value="3">企业协同办公系统 v3.0</option>
                        <option value="4">电商管理平台 v1.5</option>
                    </select>
                    <div class="text-lg font-medium ml-8">模块选择：</div>
                    <select id="moduleSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="showCode()">
                    </select>
                    
                </div>
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <i class="fas fa-code text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">代码预览</h3>
                        </div>
                        <div class="flex space-x-2">
                            <button class="px-4 py-2 bg-primary text-white !rounded-button" onclick="copyCode()">
                                <i class="far fa-copy mr-2"></i>复制代码
                            </button>
                            <button class="px-4 py-2 border border-gray-300 !rounded-button">
                                <i class="fas fa-download mr-2"></i>生成代码
                            </button>
                        </div>
                    </div>
                    <pre id="codeBlock" class="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono"
                        style="height: 600px;">// 请选择需求和模块查看代码</pre>
                </div>
            </div>
  </template>
  
  <script>
  export default {
    name: 'ModulesPage',
    data() {
      return {
        modules: [
          { id: 1, name: 'Module A' },
          { id: 2, name: 'Module B' },
          { id: 3, name: 'Module C' }
        ]
      }
    }
  }
  </script>
  