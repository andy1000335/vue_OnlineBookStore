<template>
  <div>
    <toolbar></toolbar>

    <table>
      <tr bgcolor="#BDBDBD">
        <td colspan="2">書籍</td>
        <td>單價</td>
        <td>數量／庫存</td>
        <td>小計</td>
        <td>刪除</td>
      </tr>
      <tr v-for="(book, key) in books" v-bind:key="key">
        <td class="book_img">
          <router-link router-link v-bind:to="'/book/' + book.isbn">
            <v-img
              height="100"
              width="100"
              v-bind:src="require('../../../BookImage/' + book.image)"
            ></v-img>
          </router-link>
        </td>
        <td class="book_name">
          <router-link router-link v-bind:to="'/book/' + book.isbn">
            <h4>{{ book.name }}</h4>
          </router-link>
        </td>
        <td>{{ book.price }}</td>
        <td>{{ book.quantity }}／{{ book.storage }}</td>
        <td>{{ book.price * book.quantity }}</td>
        <td>
          <v-btn v-on:click="deleteBook(book.isbn)">刪除</v-btn>
        </td>
      </tr>
    </table>
    
    <center>
      <v-btn v-on:click="checkout()">結帳</v-btn>
    </center>
  </div>
</template>

<script>
import toolbar from "./Toolbar";
export default {
  components: {
    toolbar: toolbar,
  },
  data: () => ({
    books: [],
    coupon: null,
    noStorage: false,
  }),
  methods: {
    deleteBook: function (isbn) {
      this.$http
        .post(
          "http://127.0.0.1:5000/deleteShoppingcartBook",
          { account: this.$cookie.get("account"), isbn: isbn },
          { emulateJSON: true }
        )
        .then((response) => {
          if (response.data.status == "success") {
            location.reload();
          }
        });
    },
    checkout: function(){
      if (this.books.length > 0) {
        if (this.noStorage) {
          alert("商品庫存不足")
        } else {
          this.$router.push({ path: "/checkout" });
        }
      } else {
        alert("購物車無商品")
      }
    },
  },
  created() {
    this.$http
      .post(
        "http://127.0.0.1:5000/showShoppingcart",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      )
      .then((response) => {
        this.books = response.data;
        for (var idx in this.books) {
          if (this.books[idx].quantity > this.books[idx].storage) {
            this.noStorage = true;
          }
        }
      });
  },
};
</script>

<style scoped>
table {
  border-style: outset;
  text-align: center;
  margin: 50px auto 20px auto;
  width: 60%;
  min-width: 1200px;
}
td {
  border: outset;
  padding: 0px 20px;
  font-size: 20px;
  min-width: 150px;
}
.shoppingcart {
  margin: 20px;
}
.book_img {
  width: 150px;
}
.book_name {
  text-align: left;
  min-width: 200px;
}
a {
  text-decoration: none;
  color: #333;
}
</style>