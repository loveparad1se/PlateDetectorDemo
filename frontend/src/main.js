import Vue from 'vue'
import App from './App.vue'
import router from './router' // 对应你之前的 router/index.js
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

// 关闭生产环境提示
Vue.config.productionTip = false

// 全局注册 ElementUI
Vue.use(ElementUI)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
