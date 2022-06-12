<template>

  <div class="main">
    <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">  
    <div class ="head_1"> Windows恶意软件相似性度量平台</div>
    <div class="resHeader">
      <img @click="goBack" src="../assets/imgs/fanhui.png" alt="" /><span
        @click="goBack"
        class="back"    
        ></span
      ><span class="title">检测结果</span>
     
    </div>
     <!-- <div v-if="result">
          {{result}}
    </div> -->
    
  
    <div class="div1" vif="graph" ref="avgtime"></div>
    <div class="div2" v-if="sim_res">
      <table class="table table-bordered">
        <caption style="font-size:20px">{{table[5]}}</caption>
        <thead >
          <th style="text-align:left; font-size:16px">{{table[0]}}</th>
          <th style="text-align:left; font-size:16px">{{table[1]}}</th>
          <th style="text-align:left; font-size:16px">{{table[2]}}</th>
          <th style="text-align:left; font-size:16px">{{table[3]}}</th>
          <th style="text-align:left; font-size:16px">{{table[4]}}</th>
      
        </thead>
        <tbody>
          <tr v-for="res in sim_res" :key='res'>
            <td>{{res.FileType}}</td>
            <td>{{res.MachineType}}</td>
            <td>{{res.filesize}}</td>
            <td>{{res.md5}}</td>
            <td>{{res.time}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
<script>
import Coff from "./details/Coff";
import Sections from "./details/Sections";
import Optional from "./details/Optional";
import Imports from "./details/Imports";

export default {
  //  async drawLine() {
  //   document.title = "结果";
  //   const { key } = this.$route.params;
  //   const { data } =  await this.$http.get(`/searchfilemd5/sim/${key}`);
  //   this.result = data;
  //   this.coff = data.coff || {};
  //   this.optional = data.optional || {};
  //   this.imports = data.imports || [];
  //   this.sections = data.sections || [];
  //   this.sim_res = data.sim_res || [];
  // },
  data() {
    return {
      result: {},
      activeName: "DOS头",
      coff: {},
      optional: {},
      imports: [],
      sections: [],
      sim_res:[],
      graph:{},
      table:[],
    };
  },
  async created(){
    document.title = "结果";
    const { key } = this.$route.params;
    const { data } =  await this.$http.get(`/searchfilemd5/sim/${key}`);
    this.result = data;
    this.table=["FileType","MachineType","FileSize","Md5","Time","相似性度排行结果"];
    this.graph = data.graph || {};
    this.coff = data.coff || {};
    this.optional = data.optional || {};
    this.imports = data.imports || [];
    this.sections = data.sections || [];
    this.sim_res = data.sim_res || [];
    // this.drawLine([1,2,3,4,5,6,7]);
    this.drawGraph(this.graph);

  },
  methods: {
    goBack() {
      this.$router.back(-1);
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    async drawLine(test){
    
    let mychart = this.$echarts.init(this.$refs.avgtime1);
    let option = {
      xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      },
      yAxis: {
        type: 'value'
      },
      series: [
        {
          data: test,
          type: 'line'
        }
      ]
      };
    mychart.setOption(option);
    },
    async drawGraph(graph){
        let myChart = this.$echarts.init(this.$refs.avgtime);
        let option = {
          tooltip: {},
          legend: [
            {
              data: graph.categories.map(function (a) {
                return a.name;
              })
            }
          ],
          series: [
            {
              name: 'Les Miserables',
              type: 'graph',
              layout: 'none',
              data: graph.nodes,
              links: graph.links,
              categories: graph.categories,
              roam: true,
              label: {
                show: true,
                position: 'right',
                formatter: '{b}'
              },
              labelLayout: {
                hideOverlap: true
              },
              scaleLimit: {
                min: 0.4,
                max: 2
              },
              lineStyle: {
                color: 'source',
                curveness: 0.3
              }
            }
          ]
        };
        myChart.setOption(option);
          },
  },
  components: {
    Coff,
    Sections,
    Optional,
    Imports,
  },
  mounted(){

    //this.drawGraph(this.graph)
    // this.$nextTick(()=>{
    //   this.drawLine()
    // })
  },
};





</script>

<style scoped>

.resHeader {
  position: relative;
  height: 50px;
  display: flex;
  align-items: center;
  box-shadow: rgb(17 17 17 / 16%) 0px 4px 8px -3px;
  margin-bottom: 15px;
  background-color: rgb(53,167,89);
}
.words {
  display: flex;
  justify-content: space-between;
}

.resHeader img {
  display: inline-block;
  width: 30px;
  height: 30px;
}

.resHeader img:hover,
.resHeader .back:hover {
  cursor: pointer;
}

.resHeader .back {
  /* margin: 20px 0; */
  /* padding: 5px; */
  position: relative;
  color:rgb(255,255,255);
}
/* .resHeader .back::after {
  content: "";
  position: absolute;
  width: 3px;
  height: 90%;
  background-color: #000;
  left: 45px;
  top: 50%;
  transform: translateY(-50%);
} */

.title {
  position: absolute;
  font-size: 24px;
  left: 50%;
  transform: translateX(-50%);
  color:rgb(255,255,255);
}

.results {
  width: 86vw;
  margin: 0 auto;
  /* height: calc(100vh - 50px); */
  /* background-color: rgb(237, 240, 244); */
}
.div1 {
  float:left;
  width:45%;
  height:1000px;
}
.div2{
  float:left;
  width:50%;
}
.head_1{
  background:rgb(40,40,40);
  color:rgb(255,255,255);
  height:45px;
  font-size:36px;
  text-align: center;
  padding:0px 0px 0px 100px;
}
</style>
