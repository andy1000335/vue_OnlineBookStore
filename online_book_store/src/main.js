import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import Routes from './routes'
import VueResource from 'vue-resource'
import VueCookie from 'vue-cookie'

Vue.config.productionTip = false

// routes
Vue.use(VueRouter)
const router = new VueRouter({
  routes: Routes,
  mode: 'history',
  scrollBehavior() {
    return {
      x: 0,
      y: 0
    }
  }
})

// Cookie
Vue.use(VueCookie)
// http
Vue.use(VueResource)

router.beforeEach((to, from, next) => {
  let identity = VueCookie.get('identity');
  if (identity === 'customer') {
    if (to.name == 'order_manage' || to.name == 'book_manage' || to.name == 'login') {
      next('/')
    } else {
      next();
    }
  }
  else if (identity === 'manager') {
    if (to.name == 'shoppingcart' || to.name == 'account' || to.name == 'login') {
      next('/')
    } else {
      next();
    }
  }
  else {
    if (to.name == 'login' || to.name == 'home' || to.name == 'register' || to.name == 'book') {
      next();
    } else {
      next('/');
    }
  }
})

new Vue({
  vuetify,
  render: h => h(App),
  router: router
}).$mount('#app')