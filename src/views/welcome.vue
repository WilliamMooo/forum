<template>
  <div>
    <div class="status">
      <p>你好,{{nickname}}</p>
      <div>
        <p>今日你的发帖次数为{{post_count_today}}</p>
        <p>最活跃的用户为{{active_user}}(id:{{active_user_id}}),共发了{{active_user_post_count}}帖</p>
      </div>
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
      post_count_today:'',
      active_user:'',
      active_user_id:'',
      active_user_post_count:''
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
      let dict = { params:{'now_user':this.id} }
      let headers = {  header:{ "Content-Type":"application/json; charset=utf-8" } }
      let url="http://107.150.125.214:8080/stock_forum/backend/getPostCount.php"
      this.$http.get(url,dict,headers).then((response)=>{
        let msg = response.data['msg']
        this.post_count_today = msg['now_user_count']
        this.active_user_id = msg['acticve_user_id']
        this.active_user = msg['acticve_user_name']
        this.active_user_post_count = msg['acticve_user_count']
      })
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
  background: #14836b;
  width: 50%;
  height: 50px;
}
</style>
