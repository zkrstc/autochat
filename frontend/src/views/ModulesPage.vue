<template>
  <div class="p-8">

    <select v-model="selectedRequirementId" @change="onRequirementChange" class="...">
      <option disabled value="">请选择需求</option>
      <option v-for="req in requirements" :value="req.id" :key="req.id">
        {{ req.name }} v{{ req.version }}
      </option>
    </select>

    <select @change="onModuleChange" class="...">
      <option disabled selected>请选择模块</option>
      <option v-for="mod in modules" :value="mod.id" :key="mod.id">{{ mod.name }}</option>
    </select>



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
      <pre id="codeBlock" class="..." style="height: 600px;">
  {{ selectedModuleCode || '// 请选择需求和模块查看代码' }}
</pre>

    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ModulesPage',
  data() {
    return {
      requirements: [],
      selectedRequirementId: null,
      modules: [],
      selectedModuleCode: ''
    };
  },
  mounted() {
    this.fetchRequirements();
  },
  methods: {
    async fetchRequirements() {
      const res = await axios.get('/api/requirements/list');
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
    }
  }

}

</script>