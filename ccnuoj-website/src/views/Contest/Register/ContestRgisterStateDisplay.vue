<template>
  <div>
    <template v-if="loading">
      <div v-loading="true"></div>
    </template>

    <template v-else-if="!loggedIn">
      <div>您还未登录，登录后即可报名。</div>
    </template>

    <template v-else-if="editing">
      <el-form
        :model="registerInfoForm"
        :rules="registerInfoRule"
        label-width="80px"
        ref="registerInfoForm"
        style="margin-top: 0;">


        <el-form-item label="真实姓名" prop="realName">
          <el-input v-model="registerInfoForm.realName"></el-input>
        </el-form-item>

        <div style="height:12px"></div>

        <el-form-item label="学校" prop="school">
          <el-input v-model="registerInfoForm.school"></el-input>
        </el-form-item>

        <el-form-item label="专业" prop="major">
          <el-input v-model="registerInfoForm.major"></el-input>
        </el-form-item>

        <div style="height:12px"></div>

        <el-form-item label="电话" prop="phone">
          <el-input v-model="registerInfoForm.phone"></el-input>
        </el-form-item>

        <el-form-item label="QQ" prop="qq">
          <el-input v-model="registerInfoForm.qq"></el-input>
        </el-form-item>

        <div style="height:12px"></div>

        <el-form-item label="备注" prop="remark">
          <el-input v-model="registerInfoForm.remark"></el-input>
        </el-form-item>

        <div style="height:18px"></div>

        <el-form-item size="large">
          <el-button
            :disabled="!formValid"
            @click="onClickSubmit()"
            style="width:200px ; height:40px"
            type="primary">
            提交
          </el-button>
          </el-form-item>

      </el-form>
    </template>

    <template v-else-if="registered">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>报名信息</span>
          <div style="float: right; padding: 3px 0">
            <template v-if="passed">
              <el-button disabled type="text">已通过审核</el-button>
            </template>
            <template v-else>
              <el-button @click="onClickDelete()" type="text">取消报名</el-button>
            </template>
          </div>
        </div>

        <div class="text item">
          <span>姓名：{{ registerInfo.realName }}</span>
        </div>
        <div class="text item">
          <span>学校：{{ registerInfo.studentInfo.school }}</span>
        </div>
        <div class="text item">
          <span>专业：{{ registerInfo.studentInfo.major }}</span>
        </div>
        <div class="text item">
          <span>电话：{{ registerInfo.phone }}</span>
        </div>
        <div class="text item">
          <span>QQ：{{ registerInfo.qq }}</span>
        </div>
        <div class="text item">
          <span>备注：{{ registerInfo.remark }}</span>
        </div>

        <template v-if="passed">
          <el-button disabled type="primary">已通过审核，不能再编辑</el-button>
        </template>
        <template v-else>
          <el-button @click="onClickEdit()" type="primary">编辑报名信息</el-button>
        </template>

      </el-card>
    </template>

    <template v-else>
      你还未报名。
      <el-button @click="onClickRegister()" type="primary">我要报名</el-button>
    </template>

  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import {
  getContestRegister,
  createContestRegister,
  updateContestRegister,
  deleteContestRegister,
} from '@/api/ContestRegister';

export default {
  name: 'ContestRegisterStateDisplay',
  data() {
    return {
      loading: true,

      loggedIn: undefined,
      registered: undefined,
      editing: false,

      passed: undefined,
      registerInfo: {},
      registerTime: '',

      formValid: false,
      registerInfoForm: {
        realName: '',
        school: '',
        major: '',
        phone: '',
        qq: '',
        remark: '',
      },
      registerInfoRule: {
        realName: [
          { required: true, message: '真实姓名为必填项', trigger: 'blur' },
          {
            min: 3, max: 15, message: '真实姓名长度限制在 3 到 15 个字符之间', trigger: 'blur',
          },
        ],

        school: [
          { required: true, message: '学校为必填项', trigger: 'blur' },
        ],
        major: [
          { required: true, message: '专业为必填项', trigger: 'blur' },
        ],

        phone: [
          { required: true, message: '电话号码为必填项', trigger: 'blur' },
          {
            min: 11, max: 11, message: '电话号码格式不正确', trigger: 'blur',
          },
        ],
        qq: [
          { required: true, message: 'QQ号码为必填项', trigger: 'blur' },
          {
            min: 5, max: 13, message: 'QQ号码格式不正确', trigger: 'blur',
          },
        ],

        remark: [
          { max: 100, message: '备注信息过长', trigger: 'blur' },
        ],
      },
    };
  },
  computed: {
    contestID() {
      return this.$route.params.contest_id;
    },
    ...mapGetters({
      userID: 'user/id',
    }),
  },

  methods: {
    onClickRegister() {
      this.loading = true;
      this.$store.dispatch('user/getDetailInfo')
        .then((detailInfo) => {
          const { realPersonInfo } = detailInfo;
          this.registerInfoForm = {
            realName: realPersonInfo.realName,
            school: realPersonInfo.studentInfo.school,
            major: realPersonInfo.studentInfo.major,
            phone: realPersonInfo.phone,
            qq: '',
            remark: '',
          };
          this.editing = true;
          this.loading = false;
        })
        .catch((error) => {
          this.$message.error('获取默认信息失败，请手动填写。');
          this.registerInfoForm = {
            realName: '',
            school: '',
            major: '',
            phone: '',
            qq: '',
            remark: '',
          };
          this.editing = true;
          this.loading = false;
        });
    },
    onClickEdit() {
      const { registerInfo } = this;
      this.registerInfoForm = {
        realName: registerInfo.realName,
        school: registerInfo.studentInfo.school,
        major: registerInfo.studentInfo.major,
        phone: registerInfo.phone,
        qq: registerInfo.qq,
        remark: registerInfo.remark,
      };
      this.editing = true;
    },
    onClickSubmit() {
      const formData = this.registerInfoForm;
      const registerInfo = {
        realName: formData.realName,
        studentInfo: {
          school: formData.school,
          major: formData.major,
        },
        phone: formData.phone,
        qq: formData.qq,
        remark: formData.remark,
      };
      if (this.registered) {
        this.updateRegisterInfo(registerInfo)
          .then((result) => {
            this.$message.success('更新报名信息成功');
            this.loadRegisterInfo();
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('更新报名信息失败：网络错误');
                break;
              default:
                this.$message.error('更新报名信息失败：未知错误');
                break;
            }
          });
      } else {
        this.createRegisterInfo(registerInfo)
          .then((result) => {
            this.$message.success('报名成功');
            this.loadRegisterInfo();
          })
          .catch((error) => {
            switch (error) {
              case 'NetworkError':
                this.$message.error('报名失败：网络错误');
                break;
              default:
                this.$message.error('报名失败：未知错误');
                break;
            }
          });
      }
    },
    onClickDelete() {
      this.deleteRegisterInfo()
        .then((result) => {
          this.$message.success('取消报名成功');
          this.loadRegisterInfo();
        })
        .catch((error) => {
          switch (error) {
            case 'NetworkError':
              this.$message.error('取消报名失败：网络错误');
              break;
            default:
              this.$message.error('取消报名失败：未知错误');
              break;
          }
        });
    },

    loadRegisterInfo() {
      if (this.userID === undefined) {
        this.loading = true;
      } else if (this.userID === null) {
        this.loggedIn = false;
        this.loading = false;
      } else {
        this.loggedIn = true;
        this.editing = false;
        this.loading = true;

        getContestRegister(this.contestID, this.userID)
          .then((result) => {
            this.registered = true;
            this.registerInfo = result.registerInfo;
            this.registerTime = result.registerTime;
            this.passed = result.passed;

            this.loading = false;
          })
          .catch((error) => {
            switch (error) {
              case 'RegisterNotFound':
                this.registered = false;
                this.loading = false;
                break;
              case 'NetworkError':
                this.$message.error('获取报名信息失败：网络错误');
                break;
              default:
                this.$message.error('获取报名信息失败：未知错误');
                break;
            }
          });
      }
    },
    createRegisterInfo(registerInfo) {
      return new Promise((resolve, reject) => {
        createContestRegister(this.contestID, this.userID, registerInfo)
          .then((result) => {
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    updateRegisterInfo(registerInfo) {
      return new Promise((resolve, reject) => {
        updateContestRegister(this.contestID, this.userID, registerInfo)
          .then((result) => {
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
    deleteRegisterInfo() {
      return new Promise((resolve, reject) => {
        deleteContestRegister(this.contestID, this.userID)
          .then(() => {
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      });
    },
  },

  watch: {
    userID() {
      this.loadRegisterInfo();
    },
    registerInfoForm: {
      deep: true,
      handler() {
        if ('registerInfoForm' in this.$refs) {
          this.$refs.registerInfoForm.validate((valid) => {
            this.formValid = valid;
          });
        } else {
          this.formValid = false;
        }
      },
    },
  },
  mounted() {
    this.loadRegisterInfo();
  },
};

</script>

<style scoped>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    font-size: 20px;
  }
</style>
