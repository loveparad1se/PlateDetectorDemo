<template>
  <div>
    <el-input v-model="search" placeholder="输入关键字搜索..." @input="getHistory" style="width:250px; margin-bottom:10px"></el-input>
    <el-table :data="tableData" border>
      <el-table-column prop="create_time" label="时间"></el-table-column>
      <el-table-column prop="plate_text" label="车牌号"></el-table-column>
      <el-table-column prop="username" label="人员"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="danger" size="mini" @click="del(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HistoryView',
  data() { return { search: '', tableData: [] } },
  created() { this.getHistory() },
  methods: {
    async getHistory() {
      // 修改：去掉 /api 前缀
      const res = await axios.get(`http://localhost:8000/history?keyword=${this.search}`);
      this.tableData = res.data;
    },
    async del(id) {
      // 修改：使用正确的路径 /history/{id}
      await axios.delete(`http://localhost:8000/history/${id}`);
      this.getHistory();
    }
  }
}
</script>

