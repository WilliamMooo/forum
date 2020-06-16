import Vue from 'vue'
import Router from 'vue-router'
import Login from '../views/Login'
import Recover from '../views/Recover'
import Forum from '../views/Forum'
import seeForum from '../views/seeForum'
import deleteForum from '../views/deleteForum'
import welcome from '../views/welcome'
import sendForum from '../views/sendForum'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'login',
      component: Login
    },
    {
      path: '/Recover',
      name: 'Recover',
      component: Recover
    },
    {
      path: '/Forum',
      name: 'Forum',
      component: Forum,
      children: [
        {
          path: '/',
          name: 'welcome',
          component: welcome,
        },
        {
          path: '/see',
          name: 'see',
          component: seeForum,
        },
        {
          path: '/send',
          name: 'send',
          component: sendForum,
        },
        {
          path: '/delete',
          name: 'delete',
          component: deleteForum,
        },
      ]
    },
  ]
})
