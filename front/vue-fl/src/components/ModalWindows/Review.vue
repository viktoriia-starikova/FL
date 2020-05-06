
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
                <b>Оставить отзыв</b>
              </h3>
            </slot>
            <hr />
            <slot name="body">
              <div class="border-bottom pb-3">
                <b>Рейтинг</b>
                <b style="color: red;">*</b>
                <star-rating
                  active-color="#ffc107"
                  v-model="estimation"
                  :star-size="20"
                  :border-width="3"
                  :show-rating="false"
                  v-bind:increment="0.1"
                  style="margin-bottom: 10px"
                ></star-rating>
                <b>Описание</b>
                <textarea
                  v-model="message"
                  name="text"
                  cols="20"
                  rows="3"
                  class="textarea form-control"
                ></textarea>
              </div>
            </slot>
          </div>
          <slot name="footer">
            <button class="btn btn-warning btn-block rounded" @click="SendReview()">Отправить</button>
          </slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { post } from "./../../Ajax/Http";

export default {
  name: "modal",
  props: {
    id: "",
    message: "",
    estimation: 0
  },
  methods: {
    close() {
      this.$emit("close");
    },
    SendReview() {
      const url = this.$store.getters.get_url_server + "api/v1/review/";
      post(url, response => {
        this.close();
      }, {
        message: this.message,
        estimation: this.estimation,
        addressee: this.id
      });
    }
  }
};
</script>

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
  height: 200px;
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