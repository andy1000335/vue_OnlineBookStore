<template>
  <div>
    <toolbar></toolbar>
    <div class="account">
      <div class="have">
        <div class="myCoupon">
          <h2>我的優惠券</h2>
          <table>
            <tr bgcolor="#BDBDBD">
              <td>序號</td>
              <td>期限</td>
              <td>折扣</td>
              <td>數量</td>
            </tr>
            <tr v-for="(coupon, key) in coupons" v-bind:key="key">
              <td>{{ coupon.number }}</td>
              <td v-if="coupon.end == 'None'">{{ coupon.start }} 以後</td>
              <td v-else>{{ coupon.start }}～{{ coupon.end }}</td>
              <td v-if="coupon.type == 1">{{ coupon.discount }} 折</td>
              <td v-else>折扣 {{ coupon.discount }} 元</td>
              <td>{{ coupon.quantity }}</td>
            </tr>
          </table>
        </div>
        <hr />
        <div class="myOrder">
          <h2>我的訂單</h2>
          <table>
            <tr bgcolor="#BDBDBD">
              <td>訂單編號</td>
              <td>訂購日期</td>
              <td>優惠券</td>
              <td>狀態</td>
              <td>明細</td>
              <td>取消訂單</td>
            </tr>
            <tr v-for="(order, key) in orders" v-bind:key="key">
              <td>{{ order.number }}</td>
              <td>{{ order.date }}</td>
              <td>{{ order.coupon }}</td>
              <td v-if="order.status == 1">未處理</td>
              <td v-else-if="order.status == 2">處理中</td>
              <td v-else>已完成</td>
              <td>
                <v-btn
                  v-on:click="
                    product = true;
                    getOrderBook(order.number);
                    getDiscount(order.coupon);
                    address = order.address;
                  "
                  >詳細資料</v-btn
                >
              </td>
              <td>
                <v-btn
                  v-if="order.status != 3"
                  v-on:click="deleteOrder(order.number, order.coupon)"
                  >取消訂單</v-btn
                >
              </td>
            </tr>
          </table>
        </div>
      </div>
      <div class="information">
        <table>
          <th>個人資料</th>
          <tr>
            <td>姓名：</td>
            <td>{{ name }}</td>
          </tr>
          <tr>
            <td>性別：</td>
            <td v-if="!sex">尚未設定</td>
            <td v-else-if="sex == 'M'">男</td>
            <td v-else-if="sex == 'F'">女</td>
          </tr>
          <tr>
            <td>手機：</td>
            <td v-if="!phone">尚未設定</td>
            <td v-else>{{ phone }}</td>
          </tr>
          <tr>
            <td>生日：</td>
            <td v-if="!birthday">尚未設定</td>
            <td v-else>{{ birthday }}</td>
          </tr>
          <tr>
            <td>Email：</td>
            <td>{{ mail }}</td>
          </tr>
        </table>
        <center>
          <v-btn v-on:click="update = true">修改個人資料</v-btn>
        </center>
      </div>
    </div>

    <v-dialog max-width="800" v-model="product" persistent>
      <v-btn v-on:click="product = false" fab small
        ><v-icon>mdi-close</v-icon></v-btn
      >
      <v-card>
        <table class="book">
          <tr>
            <td>書名</td>
            <td>單價</td>
            <td>數量</td>
            <td>小計</td>
          </tr>
          <tr v-for="(book, key) in books" v-bind:key="key">
            <td style="text-align: left">
              <router-link router-link v-bind:to="'/book/' + book.isbn">{{
                book.name
              }}</router-link>
            </td>
            <td>{{ book.price }}</td>
            <td>{{ book.quantity }}</td>
            <td>{{ book.price * book.quantity }}</td>
          </tr>
          <tr>
            <td colspan="4" style="text-align: left">
              配送地址：{{ this.address }}
            </td>
          </tr>
          <tr>
            <td colspan="4">
              <table class="totalPrice">
                <tr>
                  <td><h5>原價</h5></td>
                  <td></td>
                  <td>{{ totalPrice(books) }}</td>
                </tr>
                <tr>
                  <td><h5>折扣</h5></td>
                  <td>{{ discount.type }}</td>
                  <td>{{ discount.discount }}</td>
                </tr>
                <tr>
                  <td></td>
                  <td colspan="2"><hr /></td>
                </tr>
                <tr>
                  <td><h5>總價</h5></td>
                  <td></td>
                  <td v-if="discount.type == '-'">
                    {{ totalPrice(books) - discount.discount }}
                  </td>
                  <td v-else>
                    {{ Math.round(totalPrice(books) * discount.discount) }}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </v-card>
    </v-dialog>
    <v-dialog max-width="450" v-model="update" persistent>
      <v-card>
        <table class="updateInfo">
          <tr>
            <td>性別：</td>
            <td>
              <v-select
                v-model="newSex"
                v-bind:items="sexSelect"
                dense
              ></v-select>
            </td>
          </tr>
          <tr>
            <td>手機：</td>
            <td>
              <input type="text" v-model="newPhone" />
            </td>
          </tr>
          <tr>
            <td>生日：</td>
            <td>
              <v-menu
                v-model="menu"
                :close-on-content-click="false"
                offset-y
                min-width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="newDate"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="newDate"
                  no-title
                  scrollable
                  color="#BDBDBD"
                >
                  <v-btn text color="#212121" v-on:click="menu = false">
                    Close
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </td>
          </tr>
          <tr>
            <td>信箱：</td>
            <td>
              <input type="text" v-model="newMail" />
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <center style="color: red">
                ＊未輸入的資料視為不提供（信箱除外）
              </center>
              <center style="color: red" v-if="inputError">
                ＊資料格式有誤
              </center>
            </td>
          </tr>
          <tr>
            <td colspan="2">
              <center class="update">
                <v-btn v-on:click="updateInfo()">修改</v-btn>
                <v-btn v-on:click="update = false">取消</v-btn>
              </center>
            </td>
          </tr>
        </table>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import toolbar from "./Toolbar";
export default {
  components: {
    toolbar: toolbar,
  },
  data: () => ({
    coupons: [],
    orders: [],
    books: [],
    total: 0,
    discount: {},
    name: "",
    sex: "",
    phone: "",
    birthday: "",
    mail: "",
    address: "",
    product: false,
    update: false,
    sexSelect: [
      { text: "不提供", value: null },
      { text: "男性", value: "M" },
      { text: "女性", value: "F" },
    ],
    menu: false,
    newSex: null,
    newPhone: null,
    newDate: null,
    newMail: null,
    inputError: false,
  }),
  methods: {
    getOrderBook: function (number) {
      this.$http
        .post(
          "http://127.0.0.1:5000/getOrderBook",
          { ONumber: number },
          { emulateJSON: true }
        )
        .then((response) => {
          this.books = response.data;
        });
    },
    totalPrice: function (books) {
      var price = 0;
      for (var idx in books) {
        price += books[idx].price * books[idx].quantity;
      }
      return price;
    },
    getDiscount: function (CNumber) {
      if (CNumber) {
        this.$http
          .post(
            "http://127.0.0.1:5000/getDiscount",
            { number: CNumber },
            { emulateJSON: true }
          )
          .then((response) => {
            this.discount = {
              type: response.data.type,
              discount: response.data.discount,
            };
          });
      } else {
        this.discount = { type: "-", discount: 0 };
      }
    },
    deleteOrder: function (ONumber, CNumber) {
      var r = confirm("確定要刪除訂單嗎？");
      if (r) {
        this.$http
          .post(
            "http://127.0.0.1:5000/deleteOrder",
            {
              number: ONumber,
              coupon: CNumber,
              account: this.$cookie.get("account"),
            },
            { emulateJSON: true }
          )
          .then(() => {
            location.reload();
          });
      }
    },
    updateInfo: function () {
      this.$http
        .post(
          "http://127.0.0.1:5000/updateInfo",
          {
            sex: this.newSex,
            phone: this.newPhone,
            birthday: this.newDate,
            mail: this.newMail,
            account: this.$cookie.get("account"),
          },
          { emulateJSON: true }
        )
        .then((response) => {
          if (response.data.status == "InputError") {
            this.inputError = true;
          } else {
            this.inputError = false;
            location.reload();
          }
        });
    },
  },
  created() {
    this.$http.post(
      "http://127.0.0.1:5000/checkCoupon",
      { account: this.$cookie.get("account") },
      { emulateJSON: true }
    );
    this.$http
      .post(
        "http://127.0.0.1:5000/getUserInfo",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      )
      .then((response) => {
        this.name = response.data.name;
        this.sex = response.data.sex;
        this.phone = response.data.phone;
        this.birthday = response.data.birthday;
        this.mail = response.data.mail;
      });
    this.$http
      .post(
        "http://127.0.0.1:5000/getCoupon",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      )
      .then((response) => {
        this.coupons = response.data;
      });
    this.$http
      .post(
        "http://127.0.0.1:5000/getOrder",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      )
      .then((response) => {
        this.orders = response.data;
      });
  },
};
</script>

<style scoped>
.account {
  margin: 20px auto;
  width: 90%;
  min-width: 1200px;
}
.have {
  width: 70%;
  height: 100%;
  float: left;
}
.information {
  width: 30%;
  height: 100%;
  padding-top: 60px;
  float: left;
}
.information table {
  margin: 0 auto 20px auto;
  font-size: 20px;
}
.have table {
  border-style: outset;
  text-align: center;
}
.have td {
  border: outset;
  padding: 0px 20px;
  font-size: 15px;
}
.have .myCoupon {
  margin: 20px 50px;
}
.have .myOrder {
  margin: 20px 50px;
}
.have .v-btn {
  max-width: 65px;
}
.v-card {
  padding: 10px;
  display: flex;
  justify-content: center;
}
.v-dialog .book {
  border-style: outset;
  text-align: center;
}
.v-dialog .book td {
  border: outset;
  padding: 0px 20px;
  font-size: 20px;
  min-width: 100px;
}
.v-dialog .totalPrice {
  float: right;
  border-style: none;
  text-align: right;
}
.v-dialog .totalPrice td {
  border: none;
}

.updateInfo input {
  padding: 5px;
  border-style: outset;
  width: 100%;
}
.updateInfo .update .v-btn {
  margin: 10px;
}
a {
  text-decoration: none;
  color: #333;
}
</style>