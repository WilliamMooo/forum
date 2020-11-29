<template>
  <div class="main">
    <div>
      <span class="theme">
        <input placeholder="请输入主题" type="text"  maxlength="30" v-model="theme" />
      </span>
    </div>
    <div class="text">
      <textarea placeholder="请输入正文" cols="30" rows="10" v-model="text"></textarea>
    </div>
    <button @click="send">发布</button>
  </div>
</template>

<script>
export default {
  data () {
    return {
      theme:"",
      text:"",
    }
  },
  methods: {
    config() {
      let flag=true
      if (this.theme=='') {
        alert('主题不能为空')
        flag=false
      }
      if (this.text=='') {
        alert('正文不能为空')
        flag=false
      }
      if (this.text.length>300) {
        alert('正文长度不能超过')
        flag=false
      }
    },
    send() {
      if (this.config()==false) return
      let cookie = this.$cookies.get('now_user')
      let dict = {
        owner:cookie.id,
        owner_name:cookie.nickname,
        theme:this.theme,
        content:this.text,
      }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/postThread.php"
      this.$http.post(url,dict,headers).then((response)=>{
        if(response.data['status']==0) this.$router.push({name:'see'})
        alert(response.data['msg'])
      })
    }
  }
}
</script>

<style>
.main {
  color: white;
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 150px;
}
button {
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
.theme input {
  width: 80vw;
  border: 1px;
  border-radius: 4px;
  background: #b2eeda;
}
.text {
  padding-top: 20px;
}
textarea {
  width: 80vw;
  resize: none;
  border: 1px;
  border-radius: 4px;
  background: #b2eeda;
}
</style>
