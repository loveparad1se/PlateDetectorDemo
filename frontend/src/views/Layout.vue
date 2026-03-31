<template>
  <el-container style="height: 100vh">
    <el-header style="background:#409EFF; color:#fff; line-height:60px">车牌识别系统</el-header>
    <el-container>
      <el-aside width="200px" style="background:#f4f4f4">
        <el-menu :default-active="$route.path" router>
          <el-menu-item index="/detect">车牌检测</el-menu-item>
          <el-menu-item index="/history">历史记录</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main><router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>
<script>export default { name: 'MainLayout' }</script>
