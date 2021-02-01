<template>
  <div>
    <toolbar></toolbar>
    <div class="checkout">
      <div class="address background">
        <h4>配送地址</h4>
        <hr />
        <input type="text" placeholder="請輸入配送地點" v-model="address" />
      </div>
      <div class="method background">
        <h4>付款方式</h4>
        <hr />
        <v-radio-group v-model="method">
          <v-radio label="信用卡" value="CreditCard"></v-radio>
          <v-radio label="線上支付" value="Online"></v-radio>
          <v-radio label="ATM轉帳" value="ATM"></v-radio>
        </v-radio-group>
      </div>
      <div class="orderer background">
        <h4>訂購人</h4>
        <hr />
        <table>
          <tr>
            <td>姓名：</td>
            <td>{{ name }}</td>
          </tr>
          <tr>
            <td>電話：</td>
            <td v-if="!phone">尚未設定</td>
            <td v-else>{{ phone }}</td>
          </tr>
          <tr>
            <td>Email：</td>
            <td>{{ mail }}</td>
          </tr>
        </table>
        <v-btn v-on:click="update = true">修改個人資料</v-btn>
      </div>
      <div class="coupon background">
        使用優惠券：
        <input type="text" placeholder="序號" v-model="coupon" />
        <v-btn id="coupon" v-on:click="useCoupon()">使用</v-btn>
        <v-btn id="cancel" v-on:click="cancel()">取消</v-btn>
      </div>
      <div class="check">
        <table>
          <tr>
            <td>
              <h4>總金額：{{ total }}</h4>
            </td>
            <td>
              <v-btn v-on:click="submit()">送出訂單</v-btn>
            </td>
          </tr>
        </table>
      </div>
    </div>
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
    total: 0,
    coupon: null,
    method: "CreditCard",
    name: "",
    phone: "",
    mail: "",
    address: "",
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
    totalPrice: function (datas) {
      this.total = 0;
      for (var idx in datas) {
        this.total += datas[idx].price * datas[idx].quantity;
      }
    },
    useCoupon: function () {
      this.$http.post(
        "http://127.0.0.1:5000/checkCoupon",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      );
      if (this.coupon) {
        this.$http
          .post(
            "http://127.0.0.1:5000/useCoupon",
            { account: this.$cookie.get("account"), coupon: this.coupon },
            { emulateJSON: true }
          )
          .then((response) => {
            var coupon = response.data;
            if (coupon.status == "CouponNotFound") {
              alert("未擁有此優惠券");
              this.coupon = null;
            } else {
              if (this.total >= coupon.over) {
                if (coupon.type == 1) {
                  if (coupon.discount < 10) {
                    this.total = Math.round(
                      (this.total * coupon.discount) / 10
                    );
                  } else {
                    this.total = Math.round(
                      (this.total * coupon.discount) / 100
                    );
                  }
                } else {
                  if (this.total < coupon.discount) {
                    this.total == 0;
                  } else {
                    this.total -= coupon.discount;
                  }
                }
                document.getElementById("coupon").style.display = "none";
                document.getElementById("cancel").style.display = "initial";
              } else {
                alert("無法使用該優惠券\n總金額未超過使用限制");
                this.coupon = null;
              }
            }
          });
      }
    },
    cancel: function () {
      this.coupon = null;
      this.totalPrice(this.books);
      document.getElementById("coupon").style.display = "initial";
      document.getElementById("cancel").style.display = "none";
    },
    submit: function () {
      if (this.address.length > 0) {
        this.$http
          .post(
            "http://127.0.0.1:5000/submitOrder",
            {
              account: this.$cookie.get("account"),
              address: this.address,
              coupon: this.coupon,
            },
            { emulateJSON: true }
          )
          .then((response) => {
            if (response.data.status == "success") {
              alert("訂單已送出");
              if (event) {
                this.$router.push({ path: "/" });
              }
            }
          });
      } else {
        alert("配送地址尚未填寫");
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
    this.$http
      .post(
        "http://127.0.0.1:5000/showShoppingcart",
        {
          account: this.$cookie.get("account"),
        },
        { emulateJSON: true }
      )
      .then((response) => {
        this.books = response.data;
        this.totalPrice(response.data);
      });
    this.$http
      .post(
        "http://127.0.0.1:5000/getUserInfo",
        { account: this.$cookie.get("account") },
        { emulateJSON: true }
      )
      .then((response) => {
        this.name = response.data.name;
        this.phone = response.data.phone;
        this.mail = response.data.mail;
      });
  },
};
</script>

<style scoped>
.checkout {
  margin: 20px auto;
  background-color: lightgray;
  width: 65%;
  font-size: 20px;
  padding: 10px 0;
}
.checkout .v-btn {
  margin-right: 20px;
}
input {
  border-style: outset;
}
.background {
  width: 85%;
  margin: 0px auto;
  background-color: #e0e0e0;
  margin-bottom: 10px;
  padding: 10px;
}
.address input {
  margin-top: 10px;
  width: 350px;
}
.orderer table {
  margin-top: 10px;
}
.orderer .v-btn {
  margin-top: 10px;
}
.coupon input {
  margin-right: 20px;
  padding: 5px;
  width: 150px;
}
.check {
  margin-top: 10px;
  width: 85%;
  margin: 0px auto;
  padding-left: 10px;
}
.check .v-btn {
  margin-left: 10px;
}
#cancel {
  display: none;
}
.v-card {
  padding: 10px;
  display: flex;
  justify-content: center;
}
.updateInfo input {
  padding: 5px;
  border-style: outset;
  width: 100%;
}
.updateInfo .update .v-btn {
  margin: 10px;
}
</style>