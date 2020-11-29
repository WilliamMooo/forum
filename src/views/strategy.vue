<template>
  <div class="main">
    <div v-if="is_selected" class="strategys">
      <div v-for="(item,i) in strategy_list" :key="i" @click="selectStrategy(item)">
        <strategy :msg="item" />
      </div>
    </div>
    <div v-if="!is_selected" class="selected">
      <div class="box">
        <h4>策略说明:</h4>
        <p class="content">{{description}}</p>
      </div>
      <div class="box">
        <h4>历史表现:</h4>
        <p class="content">初始资产净值为1,当策略发出信号时买入或卖出相应股指期权,横坐标为时间,纵坐标为资产倍数。</p>
      </div>
      <div class="equity_graph" id="equity_graph"></div>
      <div class="box" style="height: 30vh">
        <h4>风险分析:</h4>
        <table>
          <tbody>
            <tr>
              <th>参数</th>
              <th>数值</th>
            </tr>
            <tr>
              <td>年化收益</td>
              <td>{{annualised_return}}</td>
            </tr>
            <tr class="alt">
              <td>累计净值</td>
              <td>{{equity_sum}}</td>
            </tr>
            <tr>
              <td>平均持仓时间</td>
              <td>{{average_hold}}</td>
            </tr>
            <tr class="alt">
              <td>单笔最大盈利</td>
              <td>{{max_win}}</td>
            </tr>
            <tr>
              <td>单笔最大亏损</td>
              <td>{{max_lose}}</td>
            </tr>
            <tr class="alt">
              <td>盈利笔数</td>
              <td>{{win_count}}</td>
            </tr>
            <tr>
              <td>亏损笔数</td>
              <td>{{lose_count}}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="box" style="height: 50vh">
        <h4>历史交易记录:</h4>
        <table>
          <tbody>
            <tr>
              <th>起始时间</th>
              <th>策略信号</th>
              <th>单笔盈亏</th>
            </tr>
            <tr v-for="(item, i) in equity_curve" :key="i">
              <td>{{item.start}}
                <br>
                {{item.end}}
              </td>
              <td>{{item.signal}}</td>
              <td>{{item.change}}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <button @click="back">返回</button>
    </div>
  </div>
</template>

<script>
import strategy from '../components/StrategyBox'

export default {
  components: {
    strategy
  },
  data () {
    return {
      is_selected: true,
      description: '',
      strategy_list: [],
      schart_data: {
        id: 'equity_curve',
        options: {
          type: 'bar',
          title: { text: '资产曲线'},
          showValue: false,
          bgColor: '#fbfbfb',
          labels: [],
          datasets: []
        }
      },
      equity_curve:[],
      annualised_return: '',
      average_hold: '',
      equity_sum: '',
      lose_count: '',
      max_lose: '',
      max_win: '',
      win_count: ''
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    init() {
      let dict = { params:{"user_id": this.$cookies.get('now_user').id} }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getStrategy.php"
      this.$http.get(url,dict,headers).then((response)=>{
        if(response.data['status']==0) {
          let arr = response.data['msg']
          for(let data in arr) {
            this.strategy_list.push({
              annualised_return: arr[data].annualised_return,
              average_hold: arr[data].average_hold,
              description: arr[data].description,
              equity_sum: arr[data].equity_sum,
              id: arr[data].id,
              lose_count: arr[data].lose_count,
              max_lose: arr[data].max_lose,
              max_win: arr[data].max_win,
              name: arr[data].name,
              win_count: arr[data].win_count
            })
          }
        }
      })
    },
    selectStrategy(item) {
      this.is_selected=false
      this.schart_data.options.datasets = []
      this.description = item.description
      // 获取策略数据
      let cookie = this.$cookies.get('now_user')
      let dict = {params:{
        user_id:cookie.id ,
        strategy_id:item.id
      }}
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getEquityData.php"
      this.$http.get(url,dict,headers).then((response)=>{
        if(response.data['status']==0) {
          let arr = response.data['msg']['data']
          let x = []
          let y = []
          for (let i in arr) {
            this.equity_curve.push(arr[i])
            x.push(arr[i]['end'])
            y.push(parseFloat(arr[i]['equity']))
          }
          console.log(x)
          console.log(y)
          this.drawEquityGraph(x, y)
          
          // 风险分析
          this.annualised_return = (item.annualised_return*100).toFixed(2) + '%'
          this.equity_sum = item.equity_sum
          this.average_hold = item.average_hold
          this.max_win = (item.max_win*100).toFixed(2) + '%'
          this.max_lose = (item.max_lose*100).toFixed(2) + '%'
          this.win_count = item.win_count
          this.lose_count = item.lose_count
          // 历史交易记录
          for (let i=0; i<this.equity_curve.length; i++) {
            if (this.equity_curve[i].signal == '1') this.equity_curve[i].signal='做多'
            if (this.equity_curve[i].signal == '-1') this.equity_curve[i].signal='做空'
            this.equity_curve[i].change = (this.equity_curve[i].change*100).toFixed(2) + '%'
          }
        } else {
          alert('获取数据失败')
          this.back()
        }
      })
    },
    back () {
      this.is_selected=true
    },
    drawEquityGraph(x, y) {
      let graph_data = []
      for (let i = 0; i < x.length; i++) {
        graph_data.push([x[i], y[i]])
      }
      console.log(graph_data)
      let chart = this.$echarts.init(document.getElementById('equity_graph'))
      let option = {
        backgroundColor: '#eee',
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                lineStyle: {
                    color: '#57617B'
                }
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
          name: '时间',
          type: 'time'
        },
        yAxis: {
          name:'净值曲线',
          scale: true,
          type: 'value'
        },
        dataZoom: [
          {
            type: 'slider',
            xAxisIndex: 0,
            filterMode: 'empty',
            start: 100,
            end: 0
          },
          {
            type: 'inside',
            xAxisIndex: 0,
            filterMode: 'empty'
          },
        ],
        tooltip: {
          trigger: 'axis'
        },
        series: [
          {
              type:'line',
              data: graph_data
          }
        ]
      }
      chart.setOption(option)
    }
  },
}
</script>

<style scoped>
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
.selected button {
  margin-top: 10px;
  color: white;
  border: 1px;
  border-radius: 4px;
  outline: none;
  outline: none;
  background: #14836b;
  width: 50%;
  height: 40px;
}
.equity_graph{
  width: 80vw;
  height: 50vh;
  margin: 0 auto;
}
.box table {
  width:100%;
  border-collapse:collapse;
  text-align: center;
}
td, th {
  font-size:0.8em;
  border:1px solid #98bf21;
  padding:3px 7px 2px 7px;
}
th {
  font-size:1em;
  padding-top:5px;
  padding-bottom:4px;
  background-color:#A7C942;
  color:#ffffff;
}
.alt {
  color:#000000;
  background-color:#EAF2D3;
}
</style>
