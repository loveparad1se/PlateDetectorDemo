<template>
  <div style="padding: 20px;">
    <el-input 
      v-model="search" 
      placeholder="输入车牌号关键字搜索..." 
      @input="getHistory" 
      style="width:300px; margin-bottom:20px"
      clearable
    ></el-input>

    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="create_time" label="时间" width="180"></el-table-column>
      
      <el-table-column prop="plate_text" label="车牌号">
        <template slot-scope="scope">
          <el-tag effect="dark">{{ scope.row.plate_text }}</el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="username" label="人员"></el-table-column>
      
      <el-table-column label="操作" width="120">
        <template slot-scope="scope">
          <el-button 
            type="danger" 
            size="mini" 
            icon="el-icon-delete"
            @click="del(scope.row.id)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HistoryView',
  data() {
    return {
      search: '',
      tableData: []
    }
  },
  created() {
    this.getHistory()
  },
  methods: {
    // 获取历史记录
    async getHistory() {
      try {
        const res = await axios.get(`http://localhost:8000/history?keyword=${this.search}`);
        // 这里的 res.data 已经是转换好的对象数组
        this.tableData = res.data;
      } catch (error) {
        console.error("获取数据失败:", error);
      }
    },
    // 删除记录
    async del(id) {
      this.$confirm('此操作将永久删除该记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await axios.delete(`http://localhost:8000/history/${id}`);
        this.$message.success('删除成功');
        this.getHistory();
      }).catch(() => {});
    }
  }
}
</script>

<style scoped>
.el-table {
  margin-top: 10px;
}
</style>


