<template>
  <div>
    <div class="header">
      <forum-header></forum-header>
    </div>
    <transition name="fade" mode="out-in">
      <router-view/>
    </transition>
  </div>
</template>

<script>
import Header from '../components/Forum_Header'

export default {
  components: {
    'forum-header':Header,
  },
  data () {
    return {
      id:"",
      nickname:"",
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      try {
        let cookie = this.$cookies.get('now_user')
        this.id = cookie.id
        this.nickname= cookie.nickname
        this.$router.push({name:'welcome'})
      } catch(err) {
        alert('请先登录');
        this.$router.push('/')
      }
    },
  }
}
</script>
<style>
.header {
  position: absolute;
  top: 0;
  width: 100%;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
.box {
  position: relative;
  height: 20vh;
  width: 80vw;
  border-radius: 10px;
  left: 0;
  right: 0;
  margin: 5px auto;
  background: #14836b;
  overflow-y: scroll;
}
.content {
  text-align: left;
  width: 100%;
  word-wrap:break-word;  
  word-break:break-all;
  text-indent: 2em; 
  overflow: scroll;
}
</style>
