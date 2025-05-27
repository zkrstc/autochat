<template>
    <div class="p-8">
                <!-- 新增需求选择区 -->
                <div class="flex items-center mb-6 space-x-4">
                    <div class="text-lg font-medium">需求选择：</div>
                    <select id="projectSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="updateVersions()">
                        <option value="1">智能客服系统 v1.0</option>
                        <option value="2">数据分析平台 v2.0</option>
                        <option value="3">企业协同办公系统 v3.0</option>
                        <option value="4">电商管理平台 v1.5</option>
                    </select>
                </div>

                <div class="bg-white rounded-lg shadow p-6 mb-6">
                    <h2 class="text-lg font-medium mb-6">版本历史</h2>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead>
                                <tr class="bg-gray-50">
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">版本号</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">更新内容</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">更新时间</th>
                                    <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">操作</th>
                                </tr>
                            </thead>
                            <tbody id="versionsTable">
                                <!-- 版本历史将在这里动态生成 -->
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- 分页部分 -->
                <div class="flex justify-between items-center mt-4">
                    <div class="flex items-center">
                        <span class="text-sm text-gray-700">显示</span>
                        <select id="pageSizeSelect"
                            class="border border-gray-300 rounded-button px-2 py-1 mx-2 focus:outline-none focus:ring-2 focus:ring-primary"
                            onchange="updateVersions()">
                            <option value="6">6</option>
                            <option value="12">12</option>
                            <option value="18">18</option>
                        </select>
                        <span class="text-sm text-gray-700">条</span>
                    </div>
                    <div class="flex items-center">
                        <button id="prevPageButton"
                            class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                            <i class="fas fa-angle-left"></i>
                        </button>
                        <span id="currentPage" class="mx-4 text-sm text-gray-700">1</span>
                        <button id="nextPageButton"
                            class="px-3 py-1 border border-gray-300 rounded-md hover:bg-gray-200 focus:outline-none focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
                            <i class="fas fa-angle-right"></i>
                        </button>
                    </div>
                </div>
            </div>
  </template>
  
  <script>
  export default {
    name: 'HistoryPage'
  }
  </script>
  