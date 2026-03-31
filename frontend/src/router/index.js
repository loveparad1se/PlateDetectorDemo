import Vue from 'vue'
import Router from 'vue-router'
// 导入布局母版
import Layout from '../views/Layout.vue'

Vue.use(Router)

export default new Router({
  // 去掉 # 号可以使用 mode: 'history'，但开发环境下默认即可
  routes: [
    {
      path: '/',
      component: Layout,
      redirect: '/detect', // 默认跳转到检测页面
      children: [
        {
          path: 'detect',
          name: 'DetectView',
          component: () => import('../views/Detect.vue')
        },
        {
          path: 'history',
          name: 'HistoryView',
          component: () => import('../views/History.vue')
        }
      ]
    }
  ]
})
