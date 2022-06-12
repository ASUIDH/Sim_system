<template>
  <div class="search">
    <div
      class="rolls"
      v-show="showRolls"
      :style="{ width: size === '600px' ? '100%' : '72%' }"
    >
      <div><Roll :infos="fileList1" class="roll1" :size="size"></Roll></div>
      <div><Roll :infos="fileList2" class="roll2" :size="size"></Roll></div>
      <div><Roll :infos="fileList3" class="roll3" :size="size"></Roll></div>
    </div>

   

    <div class="results" v-if="!showRolls && fileList.length > 0">
      <Card
        class="card"
        v-for="item in fileList"
        :key="item.md5"
        :info="item"
      ></Card>
    </div>
    
    <div v-else class="notfound">没有符合条件的文件！！！！！</div>
    <div class="pagination" v-if="!showRolls">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page.sync="searchForm.page"
        :page-size="10"
        layout="total, prev, pager, next"
        :total="total"
      >
      </el-pagination>
    </div>
  </div>
</template>

<script>
import Roll from "../components/Roll";
import Card from "../components/Card";

export default {
  components: {
    Roll,
    Card,
  },
  data() {
    return {
      showRolls: false,
      fileList1: [],
      fileList2: [],
      fileList3: [],
      total: 0,

      searchForm: {
        status: "",
        time: "timeDesc",
        count: "countDesc",
        date1: new Date().valueOf() - 365 * 55 * 24 * 3600 * 1000,
        date2: new Date().valueOf(),
        user: "",
        filename: "",
        md5: "",
        csrf_token: "",
        page: 1,
      },
      fileList: ["1"],
      drawer: false,
      size: "600px",
    };
  },
  async created() {
    document.title = "搜索中心";

    // const { data } = await this.$http.get("/sim_search_all");
    // this.fileList1 = data.result.slice(0, 12);
    // this.fileList2 = data.result.slice(12, 24);
    // this.fileList3 = data.result.slice(24);
      this.showRolls = false;
      this.drawer = false;
      await this.initCSRF();

      const { data } = await this.$http.post("sim_search", this.searchForm);
      this.fileList = data.fileList;
      this.total = data.total;
  },
  methods: {
    async handleCurrentChange(val) {
      this.searchForm.page = val;
      const { data } = await this.$http.post("sim_search", this.searchForm);
      // console.log(data);
      this.fileList = data.fileList;
      this.total = data.total;
    },
    async initCSRF() {
      await this.$http.get("/csrf");
      this.searchForm.csrf_token = this.getCookie("csrf_token");
    },
    getCookie(name) {
      let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    },
    async search() {
      this.showRolls = false;
      this.drawer = false;
      await this.initCSRF();

      const { data } = await this.$http.post("sim_search", this.searchForm);
      this.fileList = data.fileList;
      this.total = data.total;
    },
    focus() {
      this.size = "400px";
      this.drawer = true;
    },
  },
  watch: {
    drawer(a) {
      if (!a && this.showRolls) {
        this.size = "600px";
      }
    },
  },
};
</script>

<style scoped>
.sort {
  margin: 15px;
  background-color: #edf0f4;
  padding: 15px;
  margin-bottom: 60px;
  position: relative;
}

.sort::after {
  display: block;
  height: 2px;
  width: 100%;
  background-color: #edf0f4;
  content: "";
  position: absolute;
  /* border: 1px solid #edf0f4; */
  top: 125%;
  left: 0;
}

.dateSelector::after {
  display: block;
  height: 2px;
  width: 100%;
  background-color: #edf0f4;
  content: "";
  position: absolute;
  margin: 0 15px;
  /* border: 1px solid #edf0f4; */
  top: 118%;
  left: 0;
}

.sort > div {
  margin: 5px 0;
}
.input {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  /* border-radius: 20px; */
  margin: 15px 15px;
  background-color: #edf0f4;
  box-sizing: border-box;
}

.dateSelector {
  /* margin: 15px; */
  /* background-color: #edf0f4; */
  /* padding: 15px; */
  /* margin-bottom: 60px; */
  position: relative;
}

.input .timetxt {
  flex: 4;
  /* margin-right: 80px; */
}
.calendar {
  flex: 8;
}

.input div:nth-child(1) {
  flex: 2;
}

.input div:nth-child(2) {
  flex: 8;
}
.card {
  margin-right: 20px;
  margin-bottom: 20px;
}

.pagination {
  position: absolute;
  left: 50%;
  /* bottom: 140px; */
  transform: translateX(-50%);
}
.results {
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  align-items: center;
  margin-left: 150px;
  margin-top: 10px;
}
.drawer {
  position: relative;
}
.drawerbtn {
  position: absolute;
  right: 20px;
  bottom: 40px;
}

.el-drawer__wrapper {
  margin-top: 60px;
}

.search {
  width: 100%;
  height: 100%;
  /* background-color: #b5daec; */
  padding-top: 80px;
  position: relative;
}

.status {
  width: 100%;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.time {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.count {
  box-sizing: border-box;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.options {
  position: absolute;
  top: 15px;
  right: 10px;
  display: flex;
  /* width: 100%; */
  justify-content: space-between;
}

.roll1:hover,
.roll2:hover,
.roll3:hover {
  animation-play-state: paused;
}

.roll1 {
  animation: move 25s linear infinite backwards;
  margin-bottom: 120px;
}
.roll2 {
  animation: move 30s linear infinite backwards;
  margin-bottom: 120px;
}
.roll3 {
  animation: move 24s linear infinite backwards;
}

@keyframes move {
  0% {
    transform: rotateX(-3deg) rotateY(0);
  }
  100% {
    transform: rotateX(-3deg) rotateY(360deg);
  }
}

.notfound {
  margin: 0 auto;
  line-height: 500px;
  font-size: 60px;
  font-family: "Arial", "Microsoft YaHei", "黑体", "宋体", sans-serif;
}
</style>
