<template>
  <div class="detect-container">
    <el-card shadow="hover" header="车牌识别系统">
      <div class="step-title">1. 上传图片</div>
      <el-upload
        action=""
        :auto-upload="false"
        :on-change="handleChange"
        :show-file-list="false"
        class="uploader-area"
      >
        <img v-if="imageUrl" :src="imageUrl" class="preview-img">
        <div v-else class="placeholder">
          <i class="el-icon-picture"></i>
          <p>上传图片</p>
        </div>
      </el-upload>

      <div class="step-title" style="margin-top:20px;">2. 执行检测</div>
      <el-button type="primary" @click="handleUpload" :loading="loading" style="width:100%">
        开始识别检测
      </el-button>

      <div v-if="resultData.plate_text" class="result-display">
        <el-divider>识别结果</el-divider>
        <p>车牌号码：<span class="plate-num">{{ resultData.plate_text }}</span></p>
      </div>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return { imageUrl: '', fileRaw: null, loading: false, resultData: { plate_text: '' } }
  },
  methods: {
    handleChange(file) {
      this.fileRaw = file.raw;
      const reader = new FileReader();
      reader.readAsDataURL(file.raw);
      reader.onload = (e) => { this.imageUrl = e.target.result; };
    },
    async handleUpload() {
      if (!this.fileRaw) return this.$message.warning('请先上传图片');
      this.loading = true;
      let fd = new FormData();
      fd.append('file', this.fileRaw);
      try {
        // 修改：去掉 /api 前缀
        const res = await axios.post('http://localhost:8000/detect', fd);
        this.resultData = res.data.data;
        this.$message.success('识别成功');
        this.speak(this.resultData.plate_text);
      } catch (e) {
        this.$message.error('识别失败，请检查后端是否开启');
      } finally { this.loading = false; }
    },
    speak(text) {
      window.speechSynthesis.cancel();
      const msg = new SpeechSynthesisUtterance(`识别结果为${text}`);
      msg.lang = 'zh-CN';
      window.speechSynthesis.speak(msg);
    }
  }
}
</script>

<style scoped>
.detect-container { max-width: 400px; margin: 20px auto; }
.step-title { font-weight: bold; color: #666; margin-bottom: 10px; }
.uploader-area { border: 2px dashed #dcdfe6; border-radius: 8px; text-align: center; cursor: pointer; background: #fafafa; min-height: 150px; display: flex; align-items: center; justify-content: center; }
.preview-img { max-width: 100%; max-height: 200px; }
.plate-num { color: #409EFF; font-weight: bold; font-size: 20px; }
.result-display { margin-top: 20px; text-align: center; }
</style>






