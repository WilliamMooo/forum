import Vue from 'vue'
import Router from 'vue-router'
import Login from '../views/Login'
import Recover from '../views/Recover'
import Forum from '../views/Forum'
import seeThread from '../views/seeThread'
import deleteForum from '../views/deleteForum'
import welcome from '../views/welcome'
import postThread from '../views/postThread'
import quotation from '../views/quotation'
import strategy from '../views/strategy'

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
          component: seeThread,
        },
        {
          path: '/send',
          name: 'send',
          component: postThread,
        },
        {
          path: '/delete',
          name: 'delete',
          component: deleteForum,
        },
        {
          path: '/quotation',
          name: 'quotation',
          component: quotation,
        },
        {
          path: '/strategy',
          name: 'strategy',
          component: strategy,
        },
      ]
    },
  ]
})
