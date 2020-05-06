<script>
import Datepicker from "vuejs-datetimepicker";
import { put } from "./../Ajax/Http";

export default {
  name: "modal",
  props: {
    price: 0,
    deadline: "",
    id: ""
  },
  data: {
    maxPrice: ""
  },
  created() {
    this.maxPrice = this.price;
  },
  components: {
    Datepicker
  },
  methods: {
    close() {
      this.$emit("close");
    },
    changedTask() {
      const url =
        this.$store.getters.get_url_server + "api/v1/task/" + this.id + "/";
      put(
        url,
        response => {
          this.$emit("approved");
          this.$emit("reload");
          this.close();
        },
        {
          price: this.price,
          deadline: this.deadline
        }
      );
    }
  }
};
</script>
<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body">
            <slot name="header">
              <button
                type="button"
                class="btn-close"
                style="right:0px; top: 0px;position:absolute;"
                @click="close"
                aria-label="Close modal"
              >&times;</button>
              <h3>
                <b>Увеличить сумму и сроки</b>
              </h3>
            </slot>
            <hr />
            <slot name="body">
              <div class="border-bottom pb-4">
                <p>
                  <b>Бюджет</b>
                  <b style="color: red;">*</b>
                  <b>, $</b>
                </p>
                <number-input size="small" v-model="price" :min="maxPrice" inline center controls></number-input>
                <p>
                  <b>Дата сдачи</b>
                  <b style="color: red;">*</b>
                </p>
                <Datepicker
                  style="text-align: center;"
                  v-model="deadline"
                  format="YYYY-MM-DD H:i"
                  width="130px"
                />
              </div>
            </slot>
          </div>
          <slot name="footer">
            <button class="btn btn-warning btn-block rounded" @click="changedTask()">Сохранить</button>
          </slot>
        </div>
      </div>
    </div>
  </transition>
</template>
<style>
.btn-close {
  border: none;
  font-size: 20px;
  padding-top: 5px;
  cursor: pointer;
  font-weight: bold;
  color: #818182;
  background: transparent;
}
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 500px;
  height: 350px;
  margin: 0px auto;
  padding: 5px 20px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>