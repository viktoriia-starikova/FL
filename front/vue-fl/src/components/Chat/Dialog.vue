<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="form-section col-md-4">
          <h3 style="color: #6c757d">Диалоги</h3>
          <div class="mt-3 mb-3" style="overflow: auto !important;">
            <div
              @click="checkDialog(prof.user.id)"
              v-for="prof in profiles"
              class="media text-muted pt-3 form-section rounded mt-2 user"
            >
              <div class="mr-2" width="0" height="0">
                <img
                  class="mr-2"
                  style="width: 50px; height: 50px; border-radius: 5px;"
                  :src="$store.getters.get_url_media + prof.img"
                />
              </div>
              <p class="media-body pb-3 mb-0 lh-125">
                <strong class="d-block text-gray-dark">@{{prof.user.username}}</strong>
                <b v-if="email">Email:</b>
                {{ prof.user.email }}
              </p>
            </div>
          </div>
        </div>
        <div class="form-section col-md-8">
          <div class="media text-muted pt-3 form-section rounded">
            <div class="mr-2 rounded" width="0" height="0">
              <img
                class="mr-2 rounded"
                style="width: 164px; height: 164px;"
                :src="$store.getters.get_url_media + user.img"
              />
            </div>
            <p class="media-body pb-3 mb-0 lh-125 border-bottom border-gray">
              <strong class="d-block text-gray-dark">@{{user.user.username}}</strong>
              <b v-if="email">Email:</b>
              {{ user.user.email }}
            </p>
          </div>
          <div class="mt-3 mb-3 scroller50" id="d">
            <div v-for="mes in messages">
              <div v-if="isAuthor(mes)" class="media media-chat media-chat-reverse">
                <div class="media-body">
                  <p>{{mes.text}}</p>
                  <p
                    class="time"
                    style="background-color: transparent; color: gray;"
                  >{{mes.createdDate | filterDateTime}}</p>
                </div>
              </div>
              <div v-if="!isAuthor(mes)" class="media media-chat">
                <img class="avatar" :src="$store.getters.get_url_media + user.img" />
                <div class="media-body">
                  <p>{{mes.text}}</p>
                  <p class="time">{{mes.createdDate | filterDateTime}}</p>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-12">
              <textarea v-model="text" rows="3" cols="80" class="form-control"></textarea>
              <div style="padding-top: 10px">
                <a href="#" @click="sendMessage()" class="btn btn-info">Отправить</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script type="text/javascript">
Pusher.logToConsole = true;
import Datepicker from "vuejs-datetimepicker";
import { get, post } from "./../../Ajax/Http";

export default {
  name: "modal",
  props: {
    userId: ""
  },
  data() {
    return {
      maxPrice: "",
      roomId: "",
      channel: "",
      messages: [],
      isLoad: false,
      user: "",
      text: "",
      id: this.$route.params.id,
      profiles: []
    };
  },
  filters: {
    // Фильтр полной даты числами
    filterDateTime(item) {
      let old_date = new Date(item);
      return `${old_date.getDate()}.${old_date.getMonth() +
        1}.${old_date.getFullYear()} в ${old_date.getHours()}:${old_date.getMinutes()}`;
    }
  },
  created() {
    this.loadRoom();
    this.loadProf();
    this.loadRooms();
    this.loadUserProf();
  },
  components: {
    Datepicker
  },
  methods: {
    isAuthor(mes) {
      return this.$store.getters.get_user_info.user.id == mes.user.id;
    },
    close() {
      this.$emit("close");
    },
    sendMessage() {
      const url = this.$store.getters.get_url_server + "api/v1/messages/";
      post(url, response => {
        this.text = "";
        console.log("Sended message");
      }, {room: this.roomId, text: this.text});
    },
    checkDialog(id) {
      this.id = id;
      this.loadProf();
      this.loadRoom();
    },
    loadProf(context) {
      const url = this.$store.getters.get_url_server + "api/v2/prof/" + this.id + "/";
      get(url, response => {
        this.user = response;
      });
    },
    loadMessages() {
      const url = this.$store.getters.get_url_server + "api/v1/messages/";
      get(url, response => {
        this.messages = response;
        var block = document.getElementById("d");
        block.scrollTop = 99999;
      }, {room: this.roomId});
    },
    subscribe() {
      let pusher = new Pusher("2dd5ae948f21805d7639", {
        cluster: "eu",
        forceTLS: true
      });
      pusher.subscribe("my-channel" + this.roomId);
      pusher.bind("my-event", data => {
        this.loadMessages();
      });
    },
    loadRoom() {
      const url = this.$store.getters.get_url_server + "api/v1/room/";
      const data = {
          memberFirst: this.$store.getters.get_user_info.user.id,
          memberSecond: this.id
        }
      post(url, response => {
        this.roomId = response;
        this.subscribe();
        this.loadMessages();
      }, data)
    },
    loadRooms() {
      $.ajax({
        url: this.$store.getters.get_url_server + "api/v1/rooms/",
        type: "GET",
        success: response => {
          this.rooms = response;
          this.loadProfiles();
        }
      });
    },
    loadUserProf() {
      const url = this.$store.getters.get_url_server + "api/v2/";
      get(url, response => {
        this.prof = response;
      });
    },
    loadProfiles() {
      var userId = this.prof.user.id;
      this.rooms.forEach(room => {
        if (room.memberFirst.id == this.prof.user.id) {
          userId = room.memberSecond.id;
        } else {
          userId = room.memberFirst.id;
        }
        const url = this.$store.getters.get_url_server + "api/v2/prof/" + userId + "/";
        get(url, response => {
          this.profiles.push(response);
        })
      });
    }
  }
};
</script>

<style>
.scroller50 {
  overflow-y: auto !important;
  overflow-x: hidden;
  height: 50vh !important;
}
.user {
  cursor: pointer;
}
.time {
  background-color: transparent;
  color: gray;
}

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

.media-chat .media-body p.meta {
  background-color: transparent !important;
  padding: 0;
  opacity: 0.8;
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

.media-chat.media-chat-reverse {
  padding-right: 12px;
  padding-left: 64px;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: reverse;
  flex-direction: row-reverse;
}

.media-chat {
  padding-right: 64px;
  margin-bottom: 0;
  color: black;
}

.media {
  padding: 16px 12px;
  -webkit-transition: background-color 0.2s linear;
  transition: background-color 0.2s linear;
}

.media-chat.media-chat-reverse .media-body p {
  float: right;
  clear: right;
  background-color: #17a2b8;
  color: white;
}

.media-chat .media-body p {
  position: relative;
  padding: 6px 8px;
  margin: 4px 0;
  border-radius: 3px;
}
</style>