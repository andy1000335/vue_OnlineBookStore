<template>
  <div>
    <toolbar></toolbar>
    <v-card>
      <v-card-title> 註冊帳號 </v-card-title>
      <v-card-text>
        <table>
          <tr>
            <td>姓名：</td>
            <td colspan="6">
              <input type="text" placeholder="" v-model="name" />
            </td>
            <td style="color: red">＊必填</td>
          </tr>
          <tr>
            <td>性別：</td>
            <td>
              <v-select v-model="sex" v-bind:items="sexSelect" dense></v-select>
            </td>
          </tr>
          <tr>
            <td>手機：</td>
            <td colspan="6">
              <input type="text" placeholder="0912345678" v-model="phone" />
            </td>
          </tr>
          <tr>
            <td>生日：</td>
            <td>
              <v-combobox
                v-bind:items="Array.from({ length: 50 }, (_, i) => i + 1970)"
                label="Year"
                v-model="year"
              ></v-combobox>
            </td>
            <td>年</td>
            <td>
              <v-combobox
                v-bind:items="Array.from({ length: 12 }, (_, i) => i + 1)"
                label="Month"
                v-model="month"
              ></v-combobox>
            </td>
            <td>月</td>
            <td>
              <v-combobox
                v-bind:items="Array.from({ length: 31 }, (_, i) => i + 1)"
                label="Day"
                v-model="day"
              ></v-combobox>
            </td>
            <td>日</td>
          </tr>
          <tr>
            <td>信箱：</td>
            <td colspan="6">
              <input type="text" placeholder="" v-model="mail" />
            </td>
            <td style="color: red">＊必填</td>
          </tr>
          <tr>
            <td>帳號：</td>
            <td colspan="6">
              <input type="text" placeholder="5~20字" v-model="account" />
            </td>
            <td style="color: red">＊必填</td>
          </tr>
          <tr v-if="(account.length > 0) & (account.length < 5)">
            <td colspan="7"><p class="error">＊帳號長度不足</p></td>
          </tr>
          <tr v-if="account.length > 20">
            <td colspan="7"><p class="error">＊帳號長度過長</p></td>
          </tr>
          <tr>
            <td>密碼：</td>
            <td colspan="6">
              <input type="password" placeholder="5~20字" v-model="password" />
            </td>
            <td style="color: red">＊必填</td>
          </tr>
          <tr v-if="(password.length > 0) & (password.length < 5)">
            <td colspan="7"><p class="error">＊密碼長度不足</p></td>
          </tr>
          <tr v-if="password.length > 20">
            <td colspan="7"><p class="error">＊密碼長度過長</p></td>
          </tr>
        </table>
        <div class="button">
          <v-btn v-on:click="register()">註冊</v-btn>
        </div>
      </v-card-text>
      <div class="error" v-if="status == 'error'">＊資料填寫不完整</div>
      <div class="error" v-else-if="status == 'AccError'">＊帳號已被註冊</div>
      <div class="error" v-else-if="status == 'LengthError'">＊帳號或密碼長度錯誤</div>
      <div class="error" v-else-if="status == 'DateError'">＊日期錯誤</div>
    </v-card>
  </div>
</template>

<script>
import toolbar from "./Toolbar";
export default {
  components: {
    toolbar: toolbar,
  },
  data: () => ({
    name: "",
    sex: null,
    phone: null,
    birthday: null,
    mail: "",
    account: "",
    password: "",
    status: "",
    sexSelect: [
      { text: "不提供", value: null },
      { text: "男性", value: "M" },
      { text: "女性", value: "F" },
    ],
    year: null,
    month: null,
    day: null,
  }),
  methods: {
    register: function () {
      if (!this.name | !this.mail | !this.account | !this.password) {
        this.status = "error";
      } else {
      this.$http
        .post(
          "http://127.0.0.1:5000/register",
          {
            name: this.name,
            sex: this.sex,
            phone: this.phone,
            birthday: this.year + "-" + this.month + "-" + this.day,
            mail: this.mail,
            account: this.account,
            password: this.password,
          },
          { emulateJSON: true }
        )
        .then((response) => {
          if (response.data.status == "success") {
            this.status = "success";
            alert("帳號註冊成功");
            if (event) {
                this.$router.push({ path: "/login" });
            }
          } else if (response.data.status == "AccError") {
            this.status = "AccError";
          } else if (response.data.status == "LengthError") {
            this.status = "LengthError";
          } else {
            this.status = "DateError";
          }
          // location.reload();
        });
      }
    },
  },
};
</script>

<style scoped>
input {
  border-style: outset;
  margin: 5px 10px;
  padding: 5px;
  width: 95%;
}
.v-card {
  max-width: 500px;
  margin: 40px auto;
}
.v-card-text {
  padding-bottom: 0px;
}
.button {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 10px auto;
}
.error {
  display: flex;
  justify-content: center;
  margin: 0px;
  color: red;
}
.v-input {
  width: 90px;
  margin-left: 10px;
}
</style>