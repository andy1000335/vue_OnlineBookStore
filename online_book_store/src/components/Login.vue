<template>
  <div>
    <toolbar></toolbar>
    <div class="login-card">
      <v-card>
        <v-card-title>Login</v-card-title>
        <v-card-text>
          <label>
            帳號：
            <input
              type="text"
              placeholder="account"
              v-model="account"
            /> </label
          ><br />
          <label>
            密碼：
            <input
              type="password"
              placeholder="password"
              v-model="password"
            /> </label
          ><br />
          <div class="button">
            <v-btn v-on:click="login">登入</v-btn>
            <v-btn router-link to="/register" exact>註冊</v-btn>
          </div>
        </v-card-text>
        <p class="tip" v-if="!status">＊帳號或密碼錯誤</p>
      </v-card>
      
    </div>
  </div>
</template>

<script>
import toolbar from "./Toolbar";

export default {
  components: {
    toolbar: toolbar,
  },
  data: () => ({
    account: "",
    password: "",
    status: true,
  }),
  methods: {
    login: function () {
      this.$http
        .post(
          "http://127.0.0.1:5000/login",
          { account: this.account, password: this.password },
          { emulateJSON: true }
        )
        .then((response) => {
          this.status = response.data.status;
          if (this.status == true) {
            this.$cookie.set("identity", response.data.identity, 1800);
            this.$cookie.set("account", this.account, 1800);
            this.$router.push({ path: "/" });
          }
        });
    },
  },
};
</script>

<style scoped>
.login-card {
  display: flex;
  justify-content: center;
}
.v-card {
  margin-top: 50px;
}
input {
  border-style: outset;
  margin-bottom: 10px;
  padding: 5px;
}
.button {
  display: flex;
  justify-content: center;
}
.v-btn {
  margin: 10px;
}
.tip {
  margin: 0px 20px 10px;
  color: red;
}
</style>