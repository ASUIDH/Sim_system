<template>
  <div
    class="handle-center"
    v-loading="isLoading"
    element-loading-text="检测中"
  >
    <div class="upload-container">
      <div class="selector">
        <div>选择检测引擎:</div>
        <div>
          <el-select v-model="suanfa" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
      </div>

      <el-upload
        v-show="showUpload"
        class="upload-demo"
        drag
        action="/api/upload"
        multiple
        :data="{ csrf_token }"
        :before-upload="beforeUpload"
        :on-success="uploadSuccess"
        :on-progress="loading"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          <div>将文件拖到此处，或<em>点击上传</em></div>
          <div class="tip">上传PE文件</div>
        </div>
      </el-upload>
    </div>
    <el-progress
      :stroke-width="10"
      :width="200"
      v-show="showPercent"
      type="dashboard"
      :percentage="percent"
      :color="colors"
    ></el-progress>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLoading: false,
      csrf_token: "",
      percent: 0,
      showUpload: true,
      showPercent: false,
      colors: [
        { color: "#f56c6c", percentage: 20 },
        { color: "#e6a23c", percentage: 40 },
        { color: "#5cb87a", percentage: 60 },
        { color: "#1989fa", percentage: 80 },
        { color: "#6f7ad3", percentage: 100 },
      ],
      suanfa: "tree",
      options: [
        {
          value: "tree",
          label: "DT",
        },
        {
          value: "svm",
          label: "SVM",
        },
        {
          value: "hin",
          label: "HIN",
        },
        {
          value: "LightGBM",
          label: "LightGBM",
        },
        {
          value: "CNN",
          label: "CNN",
        },
      ],
    };
  },
  created() {
    this.initCSRF();
    document.title = "首页";
  },
  methods: {
    beforeUpload(file) {
      const extensionName = file.name.split(".");
      if (
        extensionName[extensionName.length - 1] !== "exe" &&
        extensionName[extensionName.length - 1] !== "EXE"
      ) {
        this.$message.error("请上传PE文件!");
        return false;
      }
      this.showUpload = false;
      return true;
    },
    loading(event) {
      this.showPercent = true;
      this.percent = Math.floor(event.percent);
      if (this.percent === 100) {
        this.showPercent = false;
        this.isLoading = true;

        this.$message.success("上传成功!");
      }
    },

    uploadSuccess(res) {
      this.isLoading = false;
      this.$router.push(`/result/${res.id}/id`);
      this.showUpload = true;
    },
    getCookie(name) {
      let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    },
    async initCSRF() {
      await this.$http.get("/csrf");
      this.csrf_token = this.getCookie("csrf_token");
    },
  },
};
</script>

<style>
.selector {
  width: 25%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: absolute;
  top: 16%;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px;
  background-color: #f6fbfe;
  opacity: 0.9;
  border-radius: 6px;
  font-size: 18px;
  box-shadow: 10px 5px 5px #888888;
}
.handle-center {
  width: 100vw;
  height: 94vh;
  /* background: url(../assets/imgs/op.jpg); */
  position: relative;
}
.upload-demo {
  opacity: 0.8;
}

div.el-upload-dragger {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50vw;
  height: 45vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-shadow: 5px 10px 5px #888888;
}
.el-progress {
  position: absolute !important;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.el-upload__text {
  font-size: 20px !important;

  
}
.tip {
  font-size: 14px !important;
  margin-top: 30px;
}
</style>
