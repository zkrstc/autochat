<template>
    <div class="p-8">
                <!-- 需求选择区 -->
                <div class="flex items-center mb-6 space-x-4">
                    <div class="text-lg font-medium">需求选择：</div>
                    <select id="projectSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="updateDatabaseDesigns()">
                        <option value="1">智能客服系统 v1.0</option>
                        <option value="2">数据分析平台 v2.0</option>
                        <option value="3">企业协同办公系统 v3.0</option>
                        <option value="4">电商管理平台 v1.5</option>
                    </select>

                    <div class="text-lg font-medium ml-8">数据库设计：</div>
                    <select id="dbDesignSelect"
                        class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
                        onchange="showTables()">
                        <option value="">请先选择需求</option>
                    </select>
                </div>

                <!-- 表展示区 -->
                <div class="bg-white rounded-lg shadow p-6 mb-6">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <i class="fas fa-table text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">数据表设计</h3>
                        </div>
                        <div class="flex space-x-2">
                            <button class="px-4 py-2 bg-primary text-white !rounded-button" onclick="exportSQL()">
                                <i class="fas fa-file-export mr-2"></i>导出SQL
                            </button>
                            <button class="px-4 py-2 border border-gray-300 !rounded-button" onclick="printDesign()">
                                <i class="fas fa-print mr-2"></i>生成数据库
                            </button>
                        </div>
                    </div>

                    <div id="tablesContainer" class="space-y-6">
                        <!-- 表结构将在这里动态生成 -->
                        <div class="text-center text-gray-500 py-10">
                            <i class="fas fa-database text-4xl mb-2"></i>
                            <p>请选择需求和数据库设计查看表结构</p>
                        </div>
                    </div>
                </div>

                <!-- SQL预览区 -->
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div class="flex items-center">
                            <i class="fas fa-code text-primary text-xl"></i>
                            <h3 class="ml-2 text-lg font-medium">SQL预览</h3>
                        </div>
                        <div class="flex space-x-2">
                            <button class="px-4 py-2 bg-primary text-white !rounded-button" onclick="copySQL()">
                                <i class="far fa-copy mr-2"></i>复制SQL
                            </button>
                        </div>
                    </div>
                    <pre id="sqlPreview" class="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm font-mono sql-code"
                        style="height: 300px;">
-- SQL语句将在这里显示
-- 请先选择数据库设计</pre>
                </div>
            </div>
  </template>
  
  <script>
  export default {
    name: 'DatabaseDesign'
  }
  </script>
  