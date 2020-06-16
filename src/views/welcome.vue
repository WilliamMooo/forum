<template>
  <div>
    <div class="status">
      <p>你好,{{nickname}}</p>
      <button @click="exit">退出登录</button>
    </div>
  </div>
</template>

<script>
export default {
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
      let cookie = this.$cookies.get('now_user')
      this.id = cookie.id
      this.nickname= cookie.nickname
    },
    exit() {
      if (confirm('您是否确定要退出?')) {
        this.$cookies.remove('now_user')
        this.$router.push('/')
      }
    }
  }
}
</script>

<style>

.status {
  color: white;
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
}
.status button {
  margin-top: 100px;
  color: white;
  border: 1px;
  border-radius: 4px;
  outline: none;
  background: transparent;
  outline: none;
  background: #0066d0;
  width: 50%;
  height: 50px;
}
</style>
