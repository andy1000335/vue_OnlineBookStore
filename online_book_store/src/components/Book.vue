<template>
  <div>
    <toolbar></toolbar>
    <div class="book">
      <div class="image">
        <v-img
          height="150"
          width="150"
          v-if="book.image != undefined"
          v-bind:src="require('../../../BookImage/' + book.image)"
        ></v-img>
      </div>
      <table class="infor">
        <tr>
          <td>書名：</td>
          <td>{{ book.name }}</td>
        </tr>
        <tr>
          <td>ISBN：</td>
          <td>{{ book.isbn }}</td>
        </tr>
        <tr>
          <td>價格：</td>
          <td>{{ book.price }}</td>
        </tr>
        <tr>
          <td>作者：</td>
          <td>{{ book.author }}</td>
        </tr>
        <tr>
          <td>出版商：</td>
          <td>{{ book.publisher }}</td>
        </tr>
        <tr v-if="book.star != null">
          <td>評分：</td>
          <td>
            <v-row align="center">
              <v-rating
                :value="book.star"
                color="#FFC107"
                dense
                half-increments
                readonly
                size="20"
              ></v-rating>
              <p>{{ Math.round(book.star * 10) / 10 }} / 5</p>
            </v-row>
          </td>
        </tr>
        <tr v-else>
          <td>評分：</td>
          <td>書籍尚未評分</td>
        </tr>
        <tr>
          <td>庫存：</td>
          <td>{{ book.storage }}</td>
        </tr>
        <tr>
          <td>出版日期：</td>
          <td>{{ book.date }}</td>
        </tr>
      </table>
    </div>
    <div class="center shoppingcart" v-if="book.storage > 0">
      <p>數量：</p>
      <v-btn v-on:click="decrease()">-</v-btn>
      <p class="quantity">{{ quantity }}</p>
      <v-btn v-on:click="increase()">+</v-btn>
      <v-btn class="add" v-on:click="shoppingcart()">加入購物車</v-btn>
    </div>
    <div class="center shoppingcart" v-else>暫無庫存</div>
    <div class="center score">
      <p>評分：</p>
      <v-rating
        color="#333"
        dense
        half-increments
        size="30"
        v-model="star"
      ></v-rating>
      <v-btn v-on:click="score()">送出</v-btn>
    </div>
    <center class="content">
      <hr />
      <span v-html="book.content"></span>
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
    book: {},
    quantity: 1,
    star: 0,
  }),

  methods: {
    decrease: function () {
      if (this.$cookie.get("identity") == "customer" && this.quantity > 1) {
        this.quantity--;
      }
    },
    increase: function () {
      if (
        this.$cookie.get("identity") == "customer" &&
        this.quantity < this.book.storage
      ) {
        this.quantity++;
      }
    },
    shoppingcart: function () {
      if (this.$cookie.get("identity") == "customer") {
        this.$http
          .post(
            "http://127.0.0.1:5000/shoppingcart",
            {
              account: this.$cookie.get("account"),
              isbn: this.$route.params.isbn,
              quantity: this.quantity,
            },
            { emulateJSON: true }
          )
          .then((response) => {
            if (response.data.status == "error") {
              alert("該書籍已存在購物車");
            } else {
              alert("加入完成");
            }
          });
      } else if (
        !this.$cookie.get("identity") ||
        this.$cookie.get("identity") == "vistor"
      ) {
        this.$router.push({ path: "/login" });
      }
    },
    score: function () {
      if (this.$cookie.get("identity") == "customer") {
        this.$http
          .post(
            "http://127.0.0.1:5000/score",
            {
              star: this.star,
              isbn: this.$route.params.isbn,
              account: this.$cookie.get("account"),
            },
            { emulateJSON: true }
          )
          .then((response) => {
            response;
            location.reload();
          });
      }
    },
  },

  created() {
    this.$http
      .post(
        "http://127.0.0.1:5000/getBookInfo",
        { isbn: this.$route.params.isbn },
        { emulateJSON: true }
      )
      .then((response) => {
        this.book = response.data;
      });
  },
};
</script>

<style scoped>
.book {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 50px;
}
.image {
  float: left;
  margin-right: 20px;
}
table {
  font-size: 25px;
  max-width: 800px;
}
td {
  min-width: 130px;
}
.v-rating {
  margin: 0px 10px;
}
.center {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  font-weight: bold;
}
.shoppingcart p {
  font-size: 25px;
}
.shoppingcart .quantity {
  margin: 20px;
  min-width: 25px;
  text-align: center;
}
.shoppingcart .add {
  margin-left: 20px;
}
.shoppingcart .v-btn {
  font-weight: bold;
}
input {
  margin: 0px 15px;
  max-width: 50px;
  border-style: outset;
  font-size: 20px;
}
.content hr {
  margin: 20px 0px;
  max-width: 1000px;
}
span {
  display: inline-block;
  max-width: 800px;
  font-size: 20px;
  text-align: left;
  margin-bottom: 20px;
}
</style>