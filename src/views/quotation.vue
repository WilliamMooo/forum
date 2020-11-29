<template>
  <div class="main">
      <div class="search">
        <span class="search-input">
          <input v-model="searchValue" maxlength="10" placeholder="请输入股票代码搜索" />
        </span>
        <span class="confirm-btn" @click="getData">确定</span>
      </div>
      <div v-if="isShow">
          <div class="no-data">吼吼~暂未查询到数据</div>
      </div>
      <div v-if="!isShow">{{stock_name}}</div>
      <div v-if="!isShow" id="echartContainer" ref="echartContainer"></div>
  </div>
</template>

<script>
import echarts from "echarts"
export default {
  data() {
    return {
      isShow:true,
      searchValue: '',
      stock_name:'',
      //数据模型 time0 open1 close2 min3 max4 vol5 tag6 macd7 dif8 dea9
      //['2019-10-18',18.56,18.25,18.19,18.56,55.00,0,-0.00,0.08,0.09]
      data: []
    };
  },
  methods: {
    getData() {
      this.isShow = false
      this.data = []
      let dict = { params:{"code": this.searchValue} }
      let headers = {
        header:{
          "Content-Type":"application/json; charset=utf-8"
        }
      }
      let url="http://107.150.125.214:8080/stock_forum/backend/getQuotation.php"
      this.$http.get(url,dict,headers).then((response)=>{
        if(response.data['status']==0) {
          this.isShow = false
          this.stock_name = response.data['msg']['name']
          let arr = response.data['msg']['data']
          for (let i in arr) {
            this.data.push([arr[i].time, arr[i].open, arr[i].close, arr[i].low, arr[i].high, arr[i].volume, 0])
          }
          // 计算涨跌
          let close = []
          for (let i in this.data) {
            close.push(this.data[i][2])
            if (this.data[i][2] > this.data[i][1]) { // 收盘价大于开盘价
              this.data[i][this.data[i].length-1] = 1
            }
          }
          // macd计算
          function calcEMA(n,data,field){
            let i,l,ema,a;
            a=2/(n+1);
            if(field){
                //二维数组
                ema=[data[0]["close"]];
                for(i=1,l=data.length;i<l;i++){
                    ema.push(a*data[i]["close"]+(1-a)*ema[i-1]);
                }
            }else{
                //普通一维数组
                ema=[data[0]];
                for(i=1,l=data.length;i<l;i++){
                    ema.push(a*data[i]+(1-a)*ema[i-1]);
                }
            }
            return ema;
          }
          function calcDIF(short,long,data) {
              let i,l,dif,emaShort,emaLong
              dif=[]
              emaShort=calcEMA(short,data, 1)
              emaLong=calcEMA(long,data, 1)
              for(i=0,l=data.length;i<l;i++){
                  dif.push(emaShort[i]-emaLong[i])
              }
              return dif
          }
          function calcMACD(short,long,mid,data){
            var i,l,dif,dea,macd,result
            result={}
            macd=[]
            dif=calcDIF(short,long,data)
            dea=calcDEA(mid,dif)
            for(i=0,l=data.length;i<l;i++){
                macd.push((dif[i]-dea[i])*2)
            }
            result.dif=dif
            result.dea=dea
            result.macd=macd
            return result
          }
          function calcDEA(mid,dif){
              return calcEMA(mid,dif, 0)
          }
          let macd=calcMACD(12,26,9,arr)
          for (let i in arr) {
            this.data[i].push(macd.macd[i], macd.dif[i], macd.dea[i])
          }
          let categoryData = []
          let values = []
          let macds = []
          let difs = []
          let deas = []
          for (let i in this.data) {
            categoryData.push(this.data[i].splice(0, 1)[0]);
            values.push(this.data[i]);
            macds.push(this.data[i][6]);
            difs.push(this.data[i][7]);
            deas.push(this.data[i][8]);
          }
          let data0 =  {
            categoryData: categoryData,
            values: values,
            macds: macds,
            difs: difs,
            deas: deas
          }
          // ma均线函数
          function calculateMA(dayCount) {
            var result = [];
            for (var i = 0, len = data0.values.length; i < len; i++) {
              if (i < dayCount) {
                result.push("-");
                continue;
              }
              var sum = 0;
              for (var j = 0; j < dayCount; j++) {
                sum += parseFloat(data0.values[i - j][1]);
              }
              result.push(sum / dayCount);
            }
            return result;
          }
          // k线配置项
          let option = {
            backgroundColor: '#ffffff',
            tooltip: {
              trigger: "axis",
              axisPointer: {
                type: "cross"
              }
            },
            grid: [
              {
                left: "3%",
                top: "0",
                height: "75%"
              },
              {
                left: "3%",
                right: "10%",
                top: "80%",
                height: "10%"
              }
            ],
            xAxis: [
              {
                type: "category",
                data: data0.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {
                  onZero: false,
                  lineStyle: {
                    color: "black"
                  }
                },
                splitLine: {
                  show: false
                },
                splitNumber: 20
              },
              {
                type: "category",
                gridIndex: 1,
                data: data0.categoryData,
                axisLabel: { show: true }
              }
            ],
            yAxis: [
              {
                scale: true,
                splitArea: {
                  show: true
                },
                axisLine: {
                  lineStyle: {
                    color: "black"
                  }
                },
                position: "right"
              },
              {
                gridIndex: 1,
                splitNumber: 3,
                axisLine: { onZero: false },
                axisTick: { show: false },
                splitLine: { show: false },
                axisLabel: { show: true },
                axisLine: {
                  lineStyle: {
                    color: "black"
                  }
                },
                position: "right"
              }
            ],
            dataZoom: [
              {
                type: "inside",
                start: 100,
                end: 80
              },
              {
                show: true,
                type: "slider",
                y: "90%",
                start: 50,
                end: 100
              },
              {
                show: false,
                xAxisIndex: [0, 1],
                type: "slider",
                start: 20,
                end: 100
              }
            ],
            series: [
              {
                name: "当日行情",
                type: "candlestick",
                data: data0.values,
              },
              {
                name: "MA5",
                type: "line",
                data: calculateMA(5),
                smooth: true,
                lineStyle: {
                  normal: {
                    opacity: 0.5
                  }
                }
              },
              {
                name: "MA10",
                type: "line",
                data: calculateMA(10),
                smooth: true,
                lineStyle: {
                  normal: {
                    opacity: 0.5
                  }
                }
              },
              {
                name: "MA20",
                type: "line",
                data: calculateMA(20),
                smooth: true,
                lineStyle: {
                  normal: {
                    opacity: 0.5
                  }
                }
              },
              {
                name: "MA30",
                type: "line",
                data: calculateMA(30),
                smooth: true,
                lineStyle: {
                  normal: {
                    opacity: 0.5
                  }
                }
              },
              {
                name: "MACD",
                type: "bar",
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data0.macds,
                itemStyle: {
                  normal: {
                    color: function(params) {
                      var colorList;
                      if (params.data >= 0) {
                        colorList = "#ef232a";
                      } else {
                        colorList = "#14b143";
                      }
                      return colorList;
                    }
                  }
                }
              },
              {
                name: "DIF",
                type: "line",
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data0.difs
              },
              {
                name: "DEA",
                type: "line",
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: data0.deas
              }
            ]
          }
          // 进行初始化
          let charts = echarts.init(document.getElementById("echartContainer"));
          charts.setOption(option);
        } else {
          this.isShow = true
          alert(response.data['msg'])
        }
      })
    }
  }
};
</script>

<style>
.search {
  display: flex;
  padding-bottom: 2vh;
  width: 80%;
  left: 0;
  right: 0;
  margin: auto;
}
.search input {
  width: 100%;
  background: #b2eeda;
  border: 1px;
}
.confirm-btn {
  width: 20%;
  display: inline-block;
  text-align: center;
  color: #fff;
  background: #14836b;
}
.search-input {
  width: 80%;
}
.no-data {
  text-align: center;
}
#echartContainer {
  width:100%; 
  height:70vh;
}
</style>
