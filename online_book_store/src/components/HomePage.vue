<template>
  <div>
    <toolbar></toolbar>

    <input
      type="text"
      placeholder="搜尋書名、出版商或作者"
      v-model="searchText"
      v-on:keyup.enter="onSearch()"
    />
    <div class="books">
      <v-card
        v-for="(book, key) in books"
        v-bind:key="key"
        router-link
        v-bind:to="'/book/' + book.isbn"
        ><center>
          <v-img
            height="100"
            width="100"
            v-bind:src="require('../../../BookImage/' + book.image)"
          ></v-img>
        </center>
        <v-card-title class="book_name">{{
          shortName(book.name, 19)
        }}</v-card-title>
        <v-card-text>
          <p v-if="book.star == null">書籍尚未評分</p>
          <v-row align="center" v-else>
            <v-rating
              :value="book.star"
              color="#FFC107"
              dense
              half-increments
              readonly
              size="15"
            ></v-rating>
            <p>{{ Math.round(book.star * 10) / 10 }} / 5</p>
          </v-row>

          <div class="price">
            $ •
            <p>{{ book.price }}</p>
          </div>

          <table>
            <tr>
              <td>出版：</td>
              <td>{{ shortName(book.publisher, 10) }}</td>
            </tr>
            <tr>
              <td>作者：</td>
              <td>{{ shortName(book.author, 10) }}</td>
            </tr>
          </table>
        </v-card-text>
      </v-card>
    </div>
    <div class="page">
      <table>
        <tr>
          <td><v-btn text v-on:click="lastPage()">&lt;&lt;</v-btn></td>
          <td>{{ this.$cookie.get("page") }}</td>
          <td><v-btn text v-on:click="nextPage()">&gt;&gt;</v-btn></td>
        </tr>
      </table>
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
    allBooks: [],
    books: [],
    searchText: "",
  }),

  methods: {
    search: function () {
      this.$http
        .post(
          "http://127.0.0.1:5000/getBookSearch",
          { search: this.searchText },
          { emulateJSON: true }
        )
        .then((response) => {
          this.allBooks = response.data;
          this.books = this.allBooks.slice(
            (Number(this.$cookie.get("page")) - 1) * 24,
            Number(this.$cookie.get("page")) * 24
          );
        });
    },
    onSearch: function() {
      if (this.searchText) {
        this.$cookie.set("search", this.searchText);
      } else {
        this.$cookie.delete("search");
      }
      this.$cookie.set("page", 1);
      this.search();
    },
    shortName: function (name, maxLength) {
      var length = 0;
      var idx = 0;
      var reg = /^[\d|a-zA-Z]+$/;
      var newName = "";
      while (length < maxLength && idx < name.length) {
        if (reg.test(name.charAt(idx))) {
          length += 0.5;
        } else {
          length++;
        }
        newName += name.charAt(idx);
        idx++;
      }
      if (idx < name.length) {
        return newName + " ...";
      } else {
        return newName;
      }
    },
    nextPage: function () {
      if (this.$cookie.get("page") < Math.ceil(this.allBooks.length / 24)) {
        this.$cookie.set("page", Number(this.$cookie.get("page")) + 1);
        location.reload();
      }
    },
    lastPage: function () {
      if (this.$cookie.get("page") > 1) {
        this.$cookie.set("page", Number(this.$cookie.get("page")) - 1);
        location.reload();
      }
    },
  },
  created() {
    if (!this.$cookie.get("page")) {
      this.$cookie.set("page", 1);
    }
    if (this.$cookie.get("search")) {
      this.searchText = this.$cookie.get("search");
      this.search();
    } else {
      this.$http.get("http://127.0.0.1:5000/getAllBook").then(
        (response) => {
          this.allBooks = response.data;
          this.books = this.allBooks.slice(
            (Number(this.$cookie.get("page")) - 1) * 24,
            Number(this.$cookie.get("page")) * 24
          );
        },
        (response) => {
          // error action
          console.log(response);
        }
      );
    }
  },
};
</script>

<style scoped>
input[type="text"] {
  margin: 20px 10%;
  padding: 10px;
  border-style: outset;
}
.books {
  margin: 30px 10%;
}
.v-card {
  width: 20%;
  height: 300px;
  margin: 0px 20px 50px;
  float: left;
  min-width: 256px;
}
.book_name {
  padding-top: 5px;
  padding-bottom: 0px;
}
.v-rating {
  margin: 0px 10px;
}
table {
  margin-top: 10px;
  font-size: 15px;
}
.price {
  margin-top: 5px;
  display: flex;
  justify-content: left;
  font-size: 20px;
}
.price p {
  margin-left: 10px;
  color: red;
}
.page {
  clear: both;
}
.page table {
  margin: 10px auto;
  /* margin-bottom: 10px; */
}
</style>