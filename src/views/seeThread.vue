<template>
  <div class="main">
    <div v-if="is_selected" class="threads">
      <div v-for="(item,i) in thread_list" :key="i"
          @click="selectThread(item)"
      >
        <thread :msg="item" />
      </div>
    </div>
    <div v-if="!is_selected" class="selected">
      <div v-for="(item,i) in floor_list" :key="i">
        <floor :msg="item" />
      </div>
      <div class="reply">
        <input v-model="reply_content" type="text">
        <span @click="reply">回复</span>
      </div>
      <button @click="back">返回</button>
    </div>
  </div>
</template>

<script>
import thread from '../components/Thread'
import floor from '../components/Floor'

export default {
  components: {
    thread,
    floor
  },
  data () {
    return {
      is_selected:true,
      selected_thread_id:"",
      thread_list:[],
      floor_list:[],
      reply_content:""
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getThreads.php"
      this.$http.get(url,headers).then((response)=>{
        if(response.data['status']==0) {
          const data = response.data['msg']
          this.thread_list=[]
          for(let i=0;i<data.length;i++) {
            this.thread_list[i]={
              id:data[i].id,
              owner:data[i].owner,
              owner_name:data[i].owner_name,
              theme:data[i].theme,
              content:data[i].content,
              pub_time:data[i].pub_time,
              click_tip:'点击查看详细内容'
            }
          }
        } else {
          alert(response.data['msg'])
        }
      })
    },
    selectThread (item) {
      this.selected_thread_id=item.id
      this.is_selected=false
      let dict = {
        params: { thread_id:item.id }
      }
      let headers = {
        header:{ "Content-Type":"application/json; charset=utf-8" }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getSelectedThreads.php"
      this.$http.get(url,dict, headers).then((response)=>{
        if(response.data['status']==0) {
          const data = response.data['msg']
          this.floor_list=[]
          for(let i=0;i<data.length;i++) {
            this.floor_list[i]={
              floor:data[i].floor,
              owner:data[i].owner,
              owner_name:data[i].owner_name,
              content:data[i].content,
              pub_time:data[i].pub_time,
            }
          }
        } else {
          alert(response.data['msg'])
        }
      })
    },
    reply () {
      let headers = {
        header:{ "Content-Type":"application/json; charset=utf-8" }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/reply.php"
      let dict = {
        owner: this.$cookies.get('now_user').id,
        owner_name: this.$cookies.get('now_user').nickname,
        content: this.reply_content,
        thread_id:this.selected_thread_id
      }
      this.$http.post(url,dict,headers).then((response)=>{
        alert(response.data['msg'])
        if (response.data['status']==0) {
          this.reply_content=''
          this.back()
        }
      })
    },
    back () {
      this.is_selected=true
    }
  }
}
</script>

<style>
.main {
  text-align: center;
  position: absolute;
  left: 0;
  right: 0;
  top: 100px;
  width: 80vw;
  height: 80vh;
  margin: 1px auto;
  overflow-y: auto;
  color: white;
  
}
.selected button {
  margin-top: 10px;
  border: 1px;
  border-radius: 4px;
  outline: none;
  outline: none;
  background: #14836b;
  width: 50%;
  height: 40px;
}
.reply {
  display: flex;
  justify-content: center;
  margin: 0 auto;
  margin-top: 50px;
  color: white;
  border: 1px;
  border-radius: 4px;
  outline: none;
  outline: none;
  background: #14836b;
  height: 40px;
}

.reply input {
  width: 80%;
}
.reply span {
  line-height: 40px;
  text-align:center;
  vertical-align: center;
  width: 20%;
  background: #14836b;
}
</style>
