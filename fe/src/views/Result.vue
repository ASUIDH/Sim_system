<template>
  <div class="main">
    <div class ="head_1">Windows恶意软件相似性度量平台</div>
    <div class="resHeader">
      <img @click="goBack" src="../assets/imgs/fanhui.png" alt="" /><span
        @click="goBack"
        class="back"
        ></span
      ><span class="title">检测结果</span>
    </div>
    <!-- <el-page-header @back="goBack" content="检测结果页面"> </el-page-header> -->
    <div v-if="result" class="results">
      <div class="words">
        <img :src="require(`../assets/imgs/${result.status}.png`)" alt="" />

        <div class="necessary">
          <div>md5:{{ result.md5 }}</div>
          <div>文件名称:{{ result.filename }}</div>
          <div>文件大小:{{ result.filesize | byteFormat }}</div>
          <div>上传者:{{ result.user }}</div>
        </div>
        <div class="unnecessry">
          <div>上传时间:{{ result.time | dateFormat }}</div>
          <div>总热度:{{ result.count }}</div>
          <div v-if="result.currentcount">
            当前热度:{{ result.currentcount }}
          </div>

          <div v-if="result.exist">exist:{{ result.exist }}</div>
          <div v-if="result.pe_time">petime:{{ result.pe_time }}</div>
          <div v-if="result.check_time">checktime:{{ result.check_time }}</div>
        </div>
      </div>

      <div class="tabs">
        <el-tabs
          v-model="activeName"
          type="border-card"
          @tab-click="handleClick"
        >
          <el-tab-pane label="DOS头" name="DOS头"
            ><Coff :coff="coff"
          /></el-tab-pane>
          <el-tab-pane label="OPTIONAL头" name="OPTIONAL头"
            ><Optional :optional="optional"
          /></el-tab-pane>
          <el-tab-pane label="imports" name="imports"
            ><Imports :imports="imports"
          /></el-tab-pane>
          <el-tab-pane label="sections" name="sections"
            ><Sections :sections="sections"
          /></el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import Coff from "./details/Coff";
import Sections from "./details/Sections";
import Optional from "./details/Optional";
import Imports from "./details/Imports";
export default {
  async created() {
    document.title = "结果";
    const {key} = this.$route.params;
    const { data } = await this.$http.get(`/searchfilemd5/search/${key}`);
    this.result = data;
    this.coff = data.coff || {};
    this.optional = data.optional || {};
    this.imports = data.imports || [];
    this.sections = data.sections || [];
  },
  data() {
    return {
      result: null,
      activeName: "DOS头",
      coff: {},
      optional: {},
      imports: [],
      sections: [],
    };
  },
  methods: {
    goBack() {
      this.$router.back(-1);
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
  components: {
    Coff,
    Sections,
    Optional,
    Imports,
  },
};
</script>

<style scoped>
.main{
  background-image:url("../assets/imgs/beijing2.png");
  background-repeat:no-repeat;
  background-position:100%, -10%;
  background-size:40% 40%;
  height: 1200px;
}
.resHeader {
  position: relative;
  height: 50px;
  display: flex;
  align-items: center;
  box-shadow: rgb(17 17 17 / 16%) 0px 4px 8px -3px;
  margin-bottom: 15px;
    background-color: rgb(53,167,89);
}
.tabs{
    opacity: 0.9;
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
  color:rgb(255,255,255);
  position: relative;
}

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
.head_1{
  background:rgb(40,40,40);
  color:rgb(255,255,255);
  height:45px;
  font-size:36px;
  text-align: center;
  padding:0px 0px 0px 100px;
}
</style>