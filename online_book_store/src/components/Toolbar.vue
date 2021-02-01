<template>
  <div>
    <v-toolbar dark v-if="status == 'customer'">
      <v-toolbar-title>Online Book Store</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn router-link to="/" exact v-on:click="resetPage()">首頁</v-btn>
      <v-btn router-link to="/shoppingcart" exact>購物車</v-btn>
      <v-btn router-link to="/account" exact>帳號</v-btn>
      <v-btn v-on:click="logout()">登出</v-btn>
    </v-toolbar>
    <v-toolbar dark v-else-if="status == 'manager'">
      <v-toolbar-title>Online Book Store</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn router-link to="/" exact v-on:click="resetPage()">首頁</v-btn>
      <v-btn router-link to="/order_manage" exact>訂單管理</v-btn>
      <v-btn router-link to="/book_manage" exact>書籍管理</v-btn>
      <v-btn v-on:click="logout()">登出</v-btn>
    </v-toolbar>
    <v-toolbar dark v-else>
      <v-toolbar-title>Online Book Store</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn router-link to="/" exact v-on:click="resetPage()">首頁</v-btn>
      <v-btn router-link to="/login" exact>登入</v-btn>
    </v-toolbar>
  </div>
</template>

<script>
export default {
  data: () => ({
    status: "",
  }),
  methods: {
    logout: function () {
      this.status = "visitor";
      this.$cookie.delete("identity");
      this.$cookie.delete("account");
      this.$router.push({ path: "/" }).catch(err => {err});
    },
    resetPage: function () {
      this.$cookie.set("page", 1);
    }
  },
  created() {
    this.status = this.$cookie.get("identity");
  },
};
</script>

<style scoped>
</style>