<template>
  <div>
    <el-card>
      <!-- 搜索与添加区域 -->
      <!-- <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            placeholder="请输入内容"
            v-model="queryInfo.query"
            clearable
            @clear="getUserList"
          >
            <el-button
              slot="append"
              icon="el-icon-search"
              @click="getUserList"
            ></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="addDialogVisible = true"
            >添加用户</el-button
          >
        </el-col>

        <el-col :span="2">
          <el-button type="danger" @click="clear">清空</el-button>
        </el-col>
      </el-row> -->

      <!-- 用户列表区域 -->
      <el-table :data="userlist" border stripe>
        <el-table-column width="30" type="index"></el-table-column>
        <el-table-column
          width="100"
          label="用户名"
          prop="username"
        ></el-table-column>
        <el-table-column
          width="400"
          label="密码"
          prop="password"
        ></el-table-column>
        <el-table-column label="邮箱" prop="email"></el-table-column>
        <el-table-column label="创建时间" prop="create_time"></el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 修改按钮 -->
            <el-tooltip
              effect="dark"
              content="修改资料"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="primary"
                icon="el-icon-edit"
                size="mini"
                @click="showEditDialog(scope.row.email)"
              ></el-button>
            </el-tooltip>
            <!-- 删除按钮 -->
            <el-tooltip
              effect="dark"
              content="删除"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="danger"
                icon="el-icon-delete"
                size="mini"
                @click="removeUserById(scope.row.email)"
              ></el-button>
            </el-tooltip>
            <el-tooltip
              effect="dark"
              content="课程修改"
              placement="top"
              :enterable="false"
            >
              <el-button
                type="warning"
                icon="el-icon-setting"
                size="mini"
                @click="editClass(scope.row.email)"
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <el-pagination
        :style="{ marginTop: '30px' }"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryInfo.pagenum"
        :page-sizes="[1, 2, 5, 10]"
        :page-size="queryInfo.pagesize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      >
      </el-pagination>
    </el-card>

    <!-- 添加用户的对话框 -->
    <el-dialog
      title="添加用户"
      :visible.sync="addDialogVisible"
      width="50%"
      @close="addDialogClosed"
    >
      <!-- 内容主体区域 -->
      <el-form
        :model="addForm"
        :rules="addFormRules"
        ref="addFormRef"
        label-width="70px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="addForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="addForm.password"></el-input>
        </el-form-item>
        <el-form-item label="id" prop="id">
          <el-input v-model="addForm.id"></el-input>
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="addForm.position"></el-input>
        </el-form-item>
        <el-form-item label="学院" prop="dep">
          <el-input v-model="addForm.dep"></el-input>
        </el-form-item>
      </el-form>
      <!-- 底部区域 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 修改用户的对话框 -->
    <el-dialog
      title="修改用户"
      :visible.sync="editDialogVisible"
      width="50%"
      @close="editDialogClosed"
    >
      <el-form
        :model="editForm"
        :rules="editFormRules"
        ref="editFormRef"
        label-width="70px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="editForm.password"></el-input>
        </el-form-item>
        <el-form-item label="id" prop="id">
          <el-input v-model="editForm.id"></el-input>
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="editForm.position"></el-input>
        </el-form-item>
        <el-form-item label="学院" prop="dep">
          <el-input v-model="editForm.dep"></el-input>
        </el-form-item>
        <el-form-item label="等级" prop="grade">
          <el-input v-model="editForm.grade"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUserInfo">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改课程的对话框 -->
    <el-dialog
      title="修改课程"
      :visible.sync="editClassDialogVisible"
      width="50%"
      @close="editClassDialogClosed"
    >
      <el-table :data="editClassForm" style="width: 100%">
        <el-table-column type="index"></el-table-column>
        <el-table-column label="已有课程" prop="cname"></el-table-column>
        <el-table-column label="课程id" prop="cid"></el-table-column>
        <el-table-column align="right">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.row.cid)"
              >Delete</el-button
            >
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-row>
          <el-col :span="3"
            ><el-button type="primary" @click="addClasses"
              >添加课程</el-button
            ></el-col
          >
          <el-col :span="2" :offset="15"
            ><el-button @click="editClassDialogVisible = false"
              >取 消</el-button
            ></el-col
          >
          <el-col :span="2" :offset="1"
            ><el-button type="primary" @click="editClassDialogVisible = false"
              >确 定</el-button
            ></el-col
          >
        </el-row>
      </span>
    </el-dialog>
    <!-- 添加课程的对话框 -->
    <el-dialog
      title="添加课程"
      :visible.sync="addClassDialogVisible"
      width="50%"
      @close="addClassDialogClosed"
    >
      <el-input
        placeholder="请输入内容逗号分隔"
        v-model="addClassList"
        clearable
      ></el-input>
      <span slot="footer" class="dialog-footer">
        <el-row>
          <el-button @click="addClassDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="commitAdd">确 定</el-button></el-row
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // 获取用户列表的参数对象
      queryInfo: {
        query: "",
        // 当前的页数
        pagenum: 1,
        // 当前每页显示多少条数据
        pagesize: 10,
        csrf_token: "",
      },
      userlist: [],
      total: 0,
      // 控制添加用户对话框的显示与隐藏
      addDialogVisible: false,
      editDialogVisible: false,
      editClassDialogVisible: false,
      addClassDialogVisible: false,
      // 添加用户的表单数据
      addForm: {
        username: "",
        password: "",
        id: "",
        dep: "",
        position: "",
      },
      // 添加课 以逗号分隔输入
      addClassList: "",
      // 添加表单的验证规则对象
      addFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        id: [],
        dep: [],
        position: [],
      },
      current_id: "", // 编辑和改课时存储当前人id
      // 查询到的用户信息对象
      editForm: {},
      editClassForm: {},
      editFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        id: [{ required: true, message: "请输入id", trigger: "blur" }],
        dep: [{ required: true, message: "请输入学院", trigger: "blur" }],
        position: [{ required: true, message: "请输入职位", trigger: "blur" }],
        grade: [{ required: true, message: "请输入等级", trigger: "blur" }],
      },
      editClassFormRules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        id: [{ required: true, message: "请输入id", trigger: "blur" }],
        dep: [{ required: true, message: "请输入学院", trigger: "blur" }],
        position: [{ required: true, message: "请输入职位", trigger: "blur" }],
      },
    };
  },
  created() {
    this.getUserList();
  },
  methods: {
    async initCSRF() {
      await this.$http.get("/csrf");
      this.queryInfo.csrf_token = this.getCookie("csrf_token");
    },
    getCookie(name) {
      let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
      return r ? r[1] : undefined;
    },
    async getUserList() {
      await this.initCSRF();
      const { data } = await this.$http.post("alluser", this.queryInfo);
      const { userlist, total } = data;

      for (let item of userlist) {
        let ct = item.create_time;
        let index = ct.indexOf("GMT");
        item.create_time = ct.slice(0, index);
      }
      this.userlist = userlist;
      this.total = total;
      this.queryInfo.query = "";
    },

    // 监听 pagesize 改变的事件
    handleSizeChange(newSize) {
      this.queryInfo.pagesize = newSize;
      this.getUserList();
    },
    // 监听 页码值 改变的事件
    handleCurrentChange(newPage) {
      //   console.log(newPage);
      this.queryInfo.pagenum = newPage;
      this.getUserList();
    },

    // 监听添加用户对话框的关闭事件
    addDialogClosed() {
      this.$refs.addFormRef.resetFields();
    },
    // 监听修改用户对话框的关闭事件
    editDialogClosed() {
      this.$refs.editFormRef.resetFields();
    },
    editClassDialogClosed() {},
    addClassDialogClosed() {
      this.addClassList = "";
    },
    async clear() {
      // 弹框询问用户是否删除数据
      const confirmResult = await this.$confirm(
        "此操作将删除所有信息, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).catch((err) => err);

      if (confirmResult !== "confirm") {
        return this.$message.info("已取消删除");
      }
      //   const { data: res } = await this.$http.delete("clearPeoples/");

      //   if (res.meta.status !== 200) {
      //     return this.$message.error("清空失败！");
      //   }
      this.$message.success("清除成功！");
      this.getUserList();
    },

    addUser() {
      this.$refs.addFormRef.validate(async (valid) => {
        if (!valid) return;
        // 可以发起添加用户的网络请求
        const { data: res } = await this.$http.post("manage", this.addForm);

        if (res.meta.status !== 201) {
          this.$message.error("添加用户失败！");
        }

        this.$message.success("添加用户成功！");
        // 隐藏添加用户的对话框
        this.addDialogVisible = false;
        // 重新获取用户列表数据
        this.getUserList();
      });
    },
    // 展示编辑用户的对话框
    async showEditDialog(email) {
      //   const { data: res } = await this.$http.get("manage/" + id);
      //   if (res.meta.status !== 200) {
      //     return this.$message.error("查询用户信息失败！");
      //   }
      //   this.current_id = id;
      //   this.editForm = res.data;
      //   this.editDialogVisible = true;
    },
    addClasses() {
      this.addClassDialogVisible = true;
    },
    async commitAdd() {
      let arr = this.addClassList.split(",");
      const { data: res } = await this.$http.post("addClass/", {
        arr,
        id: this.current_id,
      });
      if (res.meta.status !== 200) {
        return this.$message.error("提交加课信息失败！");
      }
      this.addClassDialogVisible = false;
      this.editClass(this.current_id);
    },
    async editClass(email) {
      //   const { data: res } = await this.$http.get("manage/" + id);
      //   if (res.meta.status !== 200) {
      //     return this.$message.error("查询用户信息失败！");
      //   }
      //   this.current_id = id; // 要有这一句 ，否则没进行编辑就改课 this.current_id是''
      //   this.editClassForm = res.data.cls;
      //   this.editClassDialogVisible = true;
    },
    async handleDelete(cid) {
      // 弹框询问用户是否删除数据
      const confirmResult = await this.$confirm(
        "此操作将永久删除, 是否继续?",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      ).catch((err) => err);

      if (confirmResult !== "confirm") {
        return this.$message.info("已取消删除");
      }
      const { data: res } = await this.$http.get(
        "manage/" + cid + "/haha/" + this.current_id
      );

      if (res.meta.status !== 200) {
        return this.$message.error("删除课程失败！");
      }
      // 关闭对话框
      // this.editClassDialogVisible = false
      // 刷新数据列表
      this.editClass(this.current_id);
      // 提示修改成功
      this.$message.success("更新用户信息成功！");
    },
    // 修改用户信息并提交
    editUserInfo() {
      this.$refs.editFormRef.validate(async (valid) => {
        if (!valid) return;
        // 发起修改用户信息的数据请求
        const { data: res } = await this.$http.put(
          "manage/" + this.current_id,
          {
            username: this.editForm.username,
            password: this.editForm.password,
            id: this.editForm.id,
            position: this.editForm.position,
            dep: this.editForm.dep,
            grade: this.editForm.grade,
          }
        );

        if (res.meta.status !== 200) {
          return this.$message.error("更新用户信息失败！");
        }
        this.current_id = this.editForm.id;
        // 关闭对话框
        this.editDialogVisible = false;
        // 刷新数据列表
        this.getUserList();
        // 提示修改成功
        this.$message.success("更新用户信息成功！");
      });
    },
    // 根据Id删除对应的用户信息
    async removeUserById(email) {
      // 弹框询问用户是否删除数据
      //   const confirmResult = await this.$confirm(
      //     "此操作将永久删除该用户, 是否继续?",
      //     "提示",
      //     {
      //       confirmButtonText: "确定",
      //       cancelButtonText: "取消",
      //       type: "warning",
      //     }
      //   ).catch((err) => err);
      //   // 如果用户确认删除，则返回值为字符串 confirm
      //   // 如果用户取消了删除，则返回值为字符串 cancel
      //   if (confirmResult !== "confirm") {
      //     return this.$message.info("已取消删除");
      //   }
      //   const { data: res } = await this.$http.delete("manage/" + id);
      //   if (res.meta.status !== 200) {
      //     return this.$message.error("删除用户失败！");
      //   }
      //   this.$message.success("删除用户成功！");
      //   this.getUserList();
    },
  },
};
</script>
