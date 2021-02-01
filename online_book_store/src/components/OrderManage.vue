<template>
  <div>
    <toolbar></toolbar>
    <div class="order">
      <h2 style="float: left; margin-right: 20px">所有訂單</h2>
      <v-btn
        v-on:click="show = true"
        style="height: 25px; min-width: 100px; padding: 0px"
        >查看銷售狀況</v-btn
      >
      <table>
        <tr bgcolor="#BDBDBD">
          <td>訂單編號</td>
          <td>訂購者</td>
          <td>訂購日期</td>
          <td>總金額</td>
          <td>狀態</td>
          <td>更新狀態</td>
        </tr>
        <tr v-for="(order, key) in orders" v-bind:key="key">
          <td>{{ order.number }}</td>
          <td>{{ order.orderer }}</td>
          <td>{{ order.date }}</td>
          <td>$ {{ order.total }}</td>
          <td v-if="order.status == 1">未處理</td>
          <td v-else-if="order.status == 2">處理中</td>
          <td v-else>已完成</td>
          <td v-if="order.status != 3">
            <v-select
              v-bind:items="orderStatus"
              v-model="status[key]"
              dense
            ></v-select>
            <v-btn v-on:click="updateOrderStatus(order.number, status[key])"
              >更新</v-btn
            >
          </td>
          <td v-else></td>
        </tr>
      </table>
    </div>
    <v-dialog max-width="800" v-model="show" persistent>
      <v-btn v-on:click="show = false" fab small
        ><v-icon>mdi-close</v-icon></v-btn
      >
      <v-card style="padding: 10px 0px">
        <h3 style="padding-left: 10px">2020年</h3>
        <v-sparkline
          :labels="Array.from({ length: 12 }, (_, i) => i + 1 + '月')"
          :value="salesData"
          type="bar"
          auto-line-width
          line-width="2"
          padding="12"
        ></v-sparkline>
        <table
          style="
            width: 100%;
            padding: 0px 0px;
            table-layout: fixed;
            text-align: center;
          "
        >
          <tr>
            <td v-for="(data, key) in salesData" v-bind:key="key">
              {{ Math.round(data / 100) / 10
              }}<span v-if="Math.round(data / 100) / 10 != 0">k</span>
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
    show: false,
    orders: [],
    orderStatus: [
      { text: "未處理", value: 1 },
      { text: "處理中", value: 2 },
      { text: "已完成", value: 3 },
    ],
    status: [],
    salesData: [],
  }),

  methods: {
    updateOrderStatus: function (number, status) {
      if (status) {
        this.$http
          .post(
            "http://127.0.0.1:5000/updateOrderStatus",
            {
              account: this.$cookie.get("account"),
              number: number,
              status: status,
            },
            { emulateJSON: true }
          )
          .then(() => {
            location.reload();
          });
      }
    },
  },
  created() {
    this.$http.get("http://127.0.0.1:5000/getAllOrder").then((response) => {
      this.orders = response.data;
    });
    this.$http.get("http://127.0.0.1:5000/getSalesData").then((response) => {
      this.salesData = response.data;
    });
  },
};
</script>

<style scoped>
.order {
  max-width: 1000px;
  margin: 20px auto;
}
.order table {
  border-style: outset;
  text-align: center;
  width: 100%;
}
.order td {
  border: outset;
  padding: 0px 15px;
  font-size: 20px;
}
.order .v-btn {
  max-width: 80px;
}
.order .v-input {
  width: 90px;
  float: left;
}
</style>