<template>
  <main class="container">
    <div class="shadow rounded alert alert-light">
      <div class="row">
        <div class="col-md-8">
          <div class="col-10" style="padding: 0px">
            <h3 class="h3">
              <b>Баланс</b>
            </h3>
            <span>
              <a @click="goPage('fl')" href="#">Биржа фриланса</a>
              <a @click="loadProf($store.getters.get_user_info.user.id)" href="#">/ Аккаунт</a>
              <span class="text-muted">/ Баланс</span>
            </span>
          </div>
        </div>
        <div class="col-md-4 mt-1 pr-1">
          <button
            @click="goPage('payPal')"
            data-turbolinks="false"
            type="button"
            class="shadow btn btn-warning btn-lg btn-block"
          >Пополнить</button>
        </div>
      </div>
    </div>

    <div class="row">
      <div class="col-md-8">
        <div class="shadow-lg alert alert-light">
          <h3 class="h3">
            <b>История платежей</b>
          </h3>
          <br />
          <div class="scroller70">
            <div v-for="(payment, index) in paymentHistory" class="mb-3">
              <h5
                v-if="index!=0 && payment.createdDate.substring(0,10) != paymentHistory[index-1].createdDate.substring(0,10)"
              >{{payment.createdDate| filterDateTime}}</h5>
              <h5 v-if="index == 0">{{payment.createdDate| filterDateTime}}</h5>
              <div
                class="row shadow ml-1 form-section border border-gray red"
                v-if="payment.isSent && payment.sender.id == $store.getters.get_user_info.user.id"
              >
                <div class="col-10">
                  <h3>{{payment.recipient.username}}</h3>
                </div>
                <div class="col-2" style="text-align: right;">
                  <h3>${{payment.total}}</h3>
                </div>
              </div>
              <div
                class="row shadow ml-1 form-section border border-gray green"
                v-if="payment.isSent && payment.recipient.id == $store.getters.get_user_info.user.id"
              >
                <div class="col-10">
                  <h3>{{payment.sender.username}}</h3>
                </div>
                <div class="col-2" style="text-align: right;">
                  <h3>${{payment.total}}</h3>
                </div>
              </div>
              <div
                class="row shadow ml-1 form-section border border-gray yellow"
                v-if="!payment.isSent && payment.recipient.id == $store.getters.get_user_info.user.id"
              >
                <div class="col-10">
                  <h3>{{payment.sender.username}}</h3>
                </div>
                <div class="col-2" style="text-align: right;">
                  <h3>${{payment.total}}</h3>
                </div>
              </div>
              <div
                class="row shadow ml-1 form-section border border-gray yellow"
                v-if="!payment.isSent && payment.sender.id == $store.getters.get_user_info.user.id"
              >
                <div class="col-10">
                  <h3>{{payment.recipient.username}}</h3>
                </div>
                <div class="col-2" style="text-align: right;">
                  <h3>${{payment.total}}</h3>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <aside class="col-md-4">
        <div id="multi-derevo" class="p-3 rounded nb-3 alert alert-light shadow">
          <h3 style="cursor: pointer">
            <b @click="loadTasks()">Баланс - ${{user.balance}}</b>
          </h3>
          <p>
            <a class="a" href="#" @click="goPage('myActiveTasks')">Я фрилансер</a>
          </p>
          <p>
            <a class="a" href="#" @click="goPage('customer')">Я заказчик</a>
          </p>
          <p>
            <a class="a" href="#" @click="loadProf($store.getters.get_user_info.user.id)">Аккаунт</a>
          </p>
          <p>
            <a class="a" href="#" @click="goPage('addPortfolio')">Портфолио</a>
          </p>
        </div>
      </aside>
    </div>
  </main>
</template>

<script>
import { get } from "../../Ajax/Http";

export default {
  data() {
    return {
      paymentHistory: [],
      user: ""
    };
  },
  created() {
    this.loadPaymentHistory();
    this.loadProfile();
  },
  filters: {
    filterDateTime(item) {
      let old_date = new Date(item);
      return `${old_date.getDate()}.${old_date.getMonth() +
        1}.${old_date.getFullYear()}`;
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadPaymentHistory() {
      const url = this.$store.getters.get_url_server + "api/v1/paymentHistory/";
      get(url, response => {
        this.paymentHistory = response;
      });
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    loadProfile() {
      const url = this.$store.getters.get_url_server + "api/v2/";
      get(url, response => {
        this.user = response;
      });
    }
  }
};
</script>

<style>
.scroller70 {
  overflow-y: auto;
  overflow-x: hidden;
  height: 70vh !important;
}

.red {
  background: #fdcdcd;
}

.green {
  background: #cdfdd1;
}

.yellow {
  background: #faf9b8;
}
</style>