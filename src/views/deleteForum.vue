<template>
  <div class="main">
    <h1>我的发帖：</h1>
    <div v-for="(item,i) in thread_list" :key="i" 
      @click="deleteThread(item)"
    >
      <thread :msg="item" />
    </div>
  </div>
</template>

<script>
import thread from '../components/Thread'

export default {
  components: {
    thread
  },
  data () {
    return {
      isSelected:true,
      thread_list:[]
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
      let dict = {
        params:{id: this.$cookies.get('now_user').id}
      }
      this.$http.get(url, dict, headers).then((response)=>{
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
              click_tip:'点击删除'
            }
          }
        } else {
          alert(response.data['msg'])
        }
      })
    },
    deleteThread(item) {
      if (confirm('是否删除该帖子?')) {
        let headers = {
          header:{
            "Content-Type":"application/json; charset=utf-8"
          }
        }
        let url="http://107.150.125.214:8080/stock_forum/backend/deleteThread.php"
        let dict = {
          id:item.id
        }
        this.$http.post(url,dict,headers).then((response)=>{
          if (response.data['status']==0) this.thread_list.splice(this.thread_list.indexOf(item),1)
          alert(response.data['msg'])
        })
      }
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
  top: 100px;
  width: 80vw;
  height: 80vh;
  margin: 1px auto;
  overflow-y: auto;
}
</style>
