<template>
  <div>
    <toolbar></toolbar>
    <div class="manage">
      <div class="book">
        <h2>書籍上架</h2>
        <div class="name side">
          <h4>書名</h4>
          <input type="text" v-model="name" />
        </div>
        <div class="picture">
          <h4>圖片</h4>
          <v-file-input accept="image/*" v-model="picture"></v-file-input>
        </div>
        <div class="ISBN">
          <h4>ISBN</h4>
          <input type="text" v-model="isbn[0]" />-<input
            type="text"
            v-model="isbn[1]"
          />-<input type="text" v-model="isbn[2]" />-<input
            type="text"
            v-model="isbn[3]"
          />-<input type="text" v-model="isbn[4]" />
        </div>
        <div class="date">
          <h4>出版日期</h4>
          <v-menu
            v-model="menu"
            :close-on-content-click="false"
            offset-y
            min-width="290px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="date"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker v-model="date" no-title scrollable color="#BDBDBD">
              <v-btn text color="#212121" v-on:click="menu = false">
                Close
              </v-btn>
            </v-date-picker>
          </v-menu>
        </div>
        <div class="publisher side">
          <h4>出版商</h4>
          <input type="text" v-model="publisher" />
        </div>
        <div class="author">
          <h4>作者</h4>
          <input type="text" placeholder="不同作者以 / 區隔" v-model="author" />
        </div>
        <div class="price side">
          <h4>價格</h4>
          <input type="text" v-model="price" />
        </div>
        <div class="storage">
          <h4>庫存</h4>
          <input type="text" v-model="storage" />
        </div>
        <div class="content">
          <h4>說明</h4>
          <textarea cols="30" rows="10" v-model="content"></textarea>
        </div>
        <center><v-btn v-on:click="uploadBook()">確定上架</v-btn></center>
      </div>
      <div class="delete_book">
        <h2>書籍下架</h2>
        <h4>ISBN</h4>
        <div class="ISBN delete">
          <input type="text" v-model="deleteIsbn[0]" />
          -
          <input type="text" v-model="deleteIsbn[1]" />
          -
          <input type="text" v-model="deleteIsbn[2]" />
          -
          <input type="text" v-model="deleteIsbn[3]" />
          -
          <input type="text" v-model="deleteIsbn[4]" />
        </div>
        <v-btn v-on:click="deleteBook()">下架</v-btn>
      </div>
      <div class="update_book">
        <h2>書籍更新</h2>
        <h4>ISBN</h4>
        <div class="ISBN">
          <input type="text" v-model="updateIsbn[0]" />
          -
          <input type="text" v-model="updateIsbn[1]" />
          -
          <input type="text" v-model="updateIsbn[2]" />
          -
          <input type="text" v-model="updateIsbn[3]" />
          -
          <input type="text" v-model="updateIsbn[4]" />
        </div>
        <h4>更新</h4>
        <v-radio-group v-model="updateAttribute" row>
          <v-radio label="價格" value="Price"></v-radio>
          <v-radio label="庫存" value="Storage"></v-radio>
        </v-radio-group>
        <div v-if="updateAttribute">
          <input type="text" v-model="updateValue" />
          <br />
          <v-btn v-on:click="updateBook()">更新</v-btn>
        </div>
      </div>
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
    menu: false,
    picture: null,
    name: null,
    isbn: [],
    date: null,
    publisher: null,
    author: null,
    price: null,
    storage: null,
    content: null,
    deleteIsbn: [],
    updateIsbn: [],
    updateSelect: [
      { text: "價格", value: "Price" },
      { text: "庫存", value: "Storage" },
      { text: "說明", value: "Content" },
    ],
    updateAttribute: null,
    updateValue: null,
  }),

  methods: {
    uploadBook: function () {
      var formData = new FormData();
      formData.append("picture", this.picture);
      formData.append("name", this.name);
      formData.append("isbn", this.isbn);
      formData.append("date", this.date);
      formData.append("publisher", this.publisher);
      formData.append("author", this.author);
      formData.append("price", this.price);
      formData.append("storage", this.storage);
      formData.append("content", this.content);
      this.$http
        .post("http://127.0.0.1:5000/uploadBook", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          if (response.data.status == "success") {
            alert("書籍上架完成");
            if (event) {
              location.reload();
            }
          } else {
            alert("書籍資料填寫不完整或有誤");
          }
        });
    },
    deleteBook: function () {
      if (this.deleteIsbn.length == 5) {
        this.$http
          .post(
            "http://127.0.0.1:5000/deleteBook",
            { isbn: this.deleteIsbn.toString() },
            { emulateJSON: true }
          )
          .then((response) => {
            if (response.data.status == "success") {
              alert("書籍已下架");
              if (event) {
                location.reload();
              }
            } else {
              alert("書籍不存在");
            }
          });
      }
    },
    updateBook: function () {
      if (this.updateIsbn.length == 5) {
        this.$http
          .post(
            "http://127.0.0.1:5000/updateBook",
            {
              isbn: this.updateIsbn.toString(),
              attritube: this.updateAttribute,
              value: this.updateValue,
            },
            { emulateJSON: true }
          )
          .then((response) => {
            if (response.data.status == "success") {
              alert("書籍已更新");
              if (event) {
                location.reload();
              }
            } else {
              alert("書籍不存在");
            }
          });
      }
    },
  },
};
</script>

<style scoped>
h2 {
  margin-top: 20px;
}
.manage {
  margin: 0px auto;
  width: 65%;
  /* min-width: 1200px; */
}
input {
  border-style: outset;
  margin: 5px 2px;
  padding: 4px;
}
.book {
  width: 60%;
  height: 100%;
  float: left;
  padding: 0px 50px;
}
.book .v-input {
  width: 200px;
  padding: 0px;
  margin: 0px;
}
.ISBN input {
  border-style: outset;
  margin: 5px 2px;
  padding: 4px;
  width: 40px;
}
.book textarea {
  border-style: outset;
  width: 100%;
}
.book .side {
  margin-right: 20px;
  float: left;
}
.delete_book {
  width: 40%;
  float: left;
  padding: 0px 50px;
}
.delete {
  float: left;
  margin-right: 20px;
}
.update_book {
  width: 40%;
  float: left;
  padding: 0px 50px;
}
.update_book .v-input {
  margin: 0px;
  height: 30px;
}
</style>