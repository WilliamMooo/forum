<template>
  <div class="main">
    <form class="login_form">
      <div class="login_form_r2">
        <span class="login_textfield">
          <label>ID</label>
          <input type="text" maxlength="30" v-model="id" />
        </span>
      </div>
      <div class="login_form_r4">
        <span class="login_textfield">
          <label>密保问题</label>
          <input disabled="disabled" type="text" maxlength="30" v-model="question" />
          <label @click="getQuestion">获取</label>
        </span>
      </div>
        <div class="login_form_r4">
        <span class="login_textfield">
          <label>密保问题答案</label>
          <input type="text" maxlength="30" v-model="answer" />
        </span>
      </div>
      <div class="login_form_r3">
        <span class="login_textfield">
          <label>重置后的新密码</label>
          <input type="password" maxlength="30" v-model="pass" />
        </span>
      </div>
      <div>
        <span class="login_button">
          <input type="button" value="" />
          <label @click="ok">提交</label>
        </span>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data () {
    return {
      id:"",
      pass:"",
      question:"",
      answer:""
    }
  },
  methods: {
    getQuestion() {
      let dict = {
        id:this.id
      }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getQuestion.php"
      this.$http.post(url,dict,headers).then((response)=>{
        if(response.data['status']==0) {
          this.question=response.data['msg']
        } else {
          alert(response.data['msg'])
        }
      })
    },
    ok() {
      if (this.question=='') {
        alert('请先获取密保问题')
        return
      }
      if (this.pass.length<6||this.pass.length>31) {
        alert("密码长度必须为6-30")
        return
      }
      let sha256 = require("js-sha256").sha256
      let dict = {
        id:this.id,
        password:sha256(this.pass),
        question:this.question,
        answer:sha256(this.answer)
      }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/recover.php"
      this.$http.post(url,dict,headers).then((response)=>{
        alert(response.data['msg'])
        if(response.data['status']==0) {
          this.$router.push({name:'login', path:'/'})
        }
      })
    }
  }
}
</script>
<style>
.main {
  width: 100%;
  color: white;
  font-size: 14px;
}
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
  /* transform: translateY(100%); */
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
  background: #14836b;
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
