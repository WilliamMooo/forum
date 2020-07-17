<template>
  <form class="login_form">
    <div class="login_form_r1">
      <div class="login_text">
        <span class="login_textfield">
          <label>用户名</label>
          <input type="text" maxlength="30" v-model="nickname" />
        </span>
      </div>
    </div>
    <div class="login_form_r2">
      <span class="login_textfield">
        <label>ID</label>
        <input type="text" maxlength="30" v-model="id" />
      </span>
    </div>
    <div class="login_form_r3">
      <span class="login_textfield">
        <label>密码</label>
        <input type="password" maxlength="30" v-model="pass" />
      </span>
    </div>
    <div class="login_form_r4">
      <span class="login_textfield">
        <label>密保问题</label>
        <input type="text" maxlength="30" v-model="question" />
      </span>
    </div>
      <div class="login_form_r4">
      <span class="login_textfield">
        <label>密保问题答案</label>
        <input type="text" maxlength="30" v-model="answer" />
      </span>
    </div>
    <div class="login_form_r5">
      <label @click="forget">忘记密码</label>
    </div>
    <div>
      <span class="login_button">
        <input type="button" value="" />
        <label @click="logIn">登录</label>
        <label @click="signUp">注册</label>
      </span>
    </div>
  </form>
</template>
<script>

export default {
  data () {
    return {
      nickname: "",
      id:"",
      pass:"",
      question:"",
      answer:""
    }
  },
  methods: {
    config() {
      let flag = true
      if (this.id.length<6||this.id.length>31) {
        alert("id长度必须为6-30")
        flag=false
      }
      if (this.pass.length<6||this.pass.length>31) {
        alert("密码长度必须为6-30")
        flag=false
      }
      if (this.id==""||this.pass==""||this.nickname==""||this.question==""||this.answer=="") {
        alert("不允许填写空值")
        flag=false
      }
      return flag
    },
    logIn() {
      let sha256 = require("js-sha256").sha256
      let dict = {
        id:this.id,
        password:sha256(this.pass),
      }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://152.32.131.27:8080/stock_forum/backend/login.php"
      this.$http.post(url,dict,headers).then((response)=>{
        if(response.data['status']==0) {
          this.$cookies.set('now_user', {id:this.id, nickname:response.data['nickname']})
          this.$router.push({name:'Forum', path:'Forum', params:{id:this.id}})
        }
        alert(response.data['msg'])
      })
    },
    signUp() {
      let sha256 = require("js-sha256").sha256
      if(this.config()==false) return
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://152.32.131.27:8080/stock_forum/backend/signUp.php"
      let dict = {
        nickname:this.nickname,
        id:this.id,
        password:sha256(this.pass),
        question:this.question,
        answer:sha256(this.answer)
      }
      this.$http.post(url,dict,headers).then((response)=>{
        alert(response.data['msg'])
      })
    },
    forget() {
      this.$router.push({name:'Recover', path:'Recover'})
    }
  }
}
</script>
<style>
.login_form {
  padding: 20px;
}
.login_form > div {
  padding-bottom: 10px;
  display: flex;
  min-height: 40px;
  justify-content: space-between;
  transition: all 0.6s ease;
}
.login_text {
  display: flex;
  flex: 1;
}
.login_text .login_textfield {
  border-radius: 0;
}
.login_text .login_textfield:first-child {
  border-radius: 2px 0 0 2px;
}
.login_text .login_textfield:last-child {
  border-radius: 0 2px 2px 0;
}
.login__signup .login_form_r5 {
  opacity: 0;
  transform: translateY(100%);
  transition-duration: 0.4s;
}
.login__signup .login_button label:nth-child(2) {
  transform: translateY(-100%);
  opacity: 0;
}
.login__signin .login_form_r1,
.login__signin .login_form_r4 {
  opacity: 0;
  transform: translateY(30%) scale(0.8);
}
.login__signin .login_form_r2,
.login__signin .login_form_r3 {
  transform: translateY(-100%);
}
.login__signin .login_form_r5 {
  transform: translateY(-200%);
}
.login__signin .login_button label:nth-child(3) {
  transform: translateY(100%);
  opacity: 0;
}
.login_button {
  position: relative;
  display: flex;
  flex: 1;
  overflow: hidden;
}
.login_button input {
  display: block;
  flex: 1;
  width: 0;
  height: 40px;
  border: none;
  border-radius: 2px;
  outline: none;
  background: #0066d0;
}
.login_button label {
  position: absolute;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  display: flex;
  transition: all 0.6s ease;
}
.login_textfield {
  flex: 1;
  display: flex;
  padding: 10px;
  width: 100%;
  border-radius: 2px;
  background-color: white;
  box-shadow: 0 1px 1px #0066d0;
}
.login_textfield label {
  margin-right: 10px;
  color: #007dff;
}
.login_textfield label i {
  width: 20px;
}
.login_textfield input {
  flex: 1;
  width: 0;
  margin: 0;
  padding: 0;
  border: none;
  outline: none;
}
</style>