<template>
  <div class="p-8">
    <!-- 需求选择 -->
    <div class="flex items-center justify-between mb-6">
      <div class="w-1/2 pr-4">
        <label class="block text-gray-700 mb-2">需求选择：</label>
        <select v-model="selectedRequirement"
          class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
          @change="handleRequirementSelected(selectedRequirement)">
          <option disabled value="">请选择需求</option>
          <option v-for="req in requirements" :key="req.id" :value="req.id">
            {{ req.name }} v{{ req.version }}
          </option>
        </select>
      </div>

      <!-- 模块选择 -->
      <div class="w-1/2 pl-4">
        <label class="block text-gray-700 mb-2">模块选择：</label>
        <select v-model="selectedModule"
          class="border border-gray-300 rounded-button px-4 py-2 min-w-[200px] focus:outline-none focus:ring-2 focus:ring-primary"
          :disabled="!selectedRequirementId" @change="handleModuleSelected(selectedModule)">
          <option disabled value="">请选择模块</option>
          <option v-for="module in architectureModules" :key="module" :value="module">
            {{ module }}
          </option>
        </select>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center">
          <i class="fas fa-code text-primary text-xl"></i>
          <h3 class="ml-2 text-lg font-medium">代码预览</h3>
        </div>
        <div class="flex space-x-2">
          <button @click="copyCombinedCode" class="px-4 py-2 bg-primary text-white !rounded-button">
            <i class="far fa-copy mr-2"></i>复制代码
          </button>
          <button @click="generateCode" class="px-4 py-2 border border-gray-300 !rounded-button">
            <i class="fas fa-print mr-2"></i>
            {{ isGenerating ? '生成中...' : '生成代码' }}
          </button>
        </div>
      </div>

      <pre v-if="moduleCodes.length > 0" class="..." style="height: 600px;">
        <div v-for="(code, index) in moduleCodes" :key="index" class="mb-6 text-left">
  <div class="text-sm text-gray-500 mb-1">// {{ code.language }} 代码</div>
  <pre class="p-4 bg-gray-100 rounded-md overflow-x-auto"><code class="block whitespace-pre text-left">{{ code.code }}</code></pre>
    </div>
    </pre>
    <pre v-else class="..." style="height: 600px;">
        // 请选择需求和模块查看代码
      </pre>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus'
export default {
  name: 'ModulesPage',
  data() {
    return {
      requirements: [],
      selectedRequirement: '',
      selectedRequirementId: '',
      architecture: null,
      architectureModules: [],
      selectedModule: '',
      moduleCodes: [],
      loading: false,
      error: null,
      selectedArchitectureId: '',
      isGenerating: false
    };
  },
  mounted() {
    this.fetchRequirements();
  },
  methods: {
    // 选择需求
    handleRequirementSelected(id) {
      this.selectedRequirementId = id;
      this.fetchArchitecture(id);
      this.resetModuleSelection();
    },
    // 获取架构信息
    async fetchArchitecture(requirementId) {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/architectures/${requirementId}`);
        if (response.data.status === 'success') {
          this.architecture = JSON.parse(response.data.data.architecture_json);
          this.selectedArchitectureId = response.data.data.id;
          this.architectureModules = this.architecture.modules || [];
        } else {
          throw new Error(response.data.message || 'Failed to fetch architecture');
        }
      } catch (error) {
        console.error('Error fetching architecture:', error);
        this.error = error.message;
        this.architectureModules = [];
      } finally {
        this.loading = false;
      }
    },
    // 选择模块
    handleModuleSelected(moduleName) {
      if (!this.selectedRequirementId || !moduleName) return;
      this.fetchModuleCodes(this.selectedArchitectureId, moduleName);
    },
    // 获取模块代码
    async fetchModuleCodes(architectureId, moduleName) {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.get('http://127.0.0.1:5000/api/module_code', {
          params: {
            architecture_id: architectureId,
            module_name: moduleName
          }
        });
        this.moduleCodes = response.data;
      } catch (error) {
        console.error('Error fetching module codes:', error);
        this.error = error.response?.data?.error || error.message;
        this.moduleCodes = [];
      } finally {
        this.loading = false;
      }
    },
    async fetchRequirements() {
      const res = await axios.get('http://127.0.0.1:5000/api/requirements/list');
      this.requirements = res.data;
    },
    async onRequirementChange() {
      const res = await axios.post('/api/modules/generate', {
        requirement_id: this.selectedRequirementId
      });
      this.modules = res.data;
      this.selectedModuleCode = '';
    },
    onModuleChange(event) {
      const moduleId = parseInt(event.target.value);
      const mod = this.modules.find(m => m.id === moduleId);
      this.selectedModuleCode = mod ? mod.code : '// 无模块代码';
    },
    copyCode() {
      navigator.clipboard.writeText(this.selectedModuleCode);
    },
    // 重置模块选择
    resetModuleSelection() {
      this.selectedModule = '';
      this.moduleCodes = [];
    },
    async generateCode() {
      if (!this.selectedModule || !this.selectedArchitectureId||!this.selectedRequirementId) {
        ElMessage.warning('请先选择模块和需求')
        return
      }
      this.isGenerating = true
      this.loading = true
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/modules/generate', {
          module_name: this.selectedModule,
          requirement_id: this.selectedRequirementId,
          architecture_id: this.selectedArchitectureId
        })

        ElMessage.success('代码生成成功，已保存到数据库')
        console.log(response.data)
      } catch (error) {
        console.error(error)
        ElMessage.error('生成失败：' + (error.response?.data?.error || '未知错误'))
      } finally {
        this.loading = false
        this.isGenerating = false
        this.fetchModuleCodes(this.selectedArchitectureId, this.selectedModule)
      }
    }
  }

}

</script>