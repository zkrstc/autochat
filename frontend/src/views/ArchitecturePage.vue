<template>
    <div class="p-8">
                <!-- 需求选择和生成按钮 -->
                <div class="flex items-center justify-between mb-6">
                    <div class="flex items-center space-x-4">
                        <div class="text-lg font-medium">需求选择：</div>
                        <select id="projectSelect"
                            class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary">
                            <option value="1">智能客服系统 v1.0</option>
                            <option value="2">数据分析平台 v2.0</option>
                            <option value="3">企业协同办公系统 v3.0</option>
                            <option value="4">电商管理平台 v1.5</option>
                        </select>
                    </div>
                    <button id="generateBtn"
                        class="px-6 py-2 bg-primary text-white !rounded-button hover:bg-blue-600 transition-colors">
                        <i class="fas fa-magic mr-2"></i>生成架构
                    </button>
                </div>

                <!-- 架构展示区域 -->
                <div class="bg-white rounded-lg shadow p-6 mb-6">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <i class="fas fa-sitemap text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">系统架构图</h3>
                        </div>
                        <div class="flex space-x-2">
                            <button class="px-4 py-2 border border-gray-300 !rounded-button">
                                <i class="fas fa-download mr-2"></i>下载
                            </button>
                        </div>
                    </div>

                    <div id="architectureContainer" class="architecture-diagram">
                        <div class="text-center">
                            <i class="fas fa-sitemap text-4xl mb-2"></i>
                            <p>请选择需求并点击"生成架构"按钮</p>
                        </div>
                    </div>
                </div>

                <!-- 技术栈和模块划分 -->
                <div class="grid grid-cols-2 gap-6">
                    <!-- 技术栈 -->
                    <div class="bg-white rounded-lg shadow p-6">
                        <div class="flex items-center mb-4">
                            <i class="fas fa-code-branch text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">推荐技术栈</h3>
                        </div>
                        <div id="techStackContainer" class="space-y-3">
                            <div class="text-center text-gray-500 py-10">
                                <i class="fas fa-cog text-4xl mb-2"></i>
                                <p>架构生成后将显示推荐技术栈</p>
                            </div>
                        </div>
                    </div>

                    <!-- 模块划分 -->
                    <div class="bg-white rounded-lg shadow p-6">
                        <div class="flex items-center mb-4">
                            <i class="fas fa-tasks text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">模块划分</h3>
                        </div>
                        <div id="modulesContainer" class="space-y-3">
                            <div class="text-center text-gray-500 py-10">
                                <i class="fas fa-project-diagram text-4xl mb-2"></i>
                                <p>架构生成后将显示模块划分</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
  </template>
  
  <script>
  export default {
    name: 'ArchitecturePage'
  }
  </script>
  