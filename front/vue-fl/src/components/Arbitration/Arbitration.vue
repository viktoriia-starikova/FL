<template>
  <div>
    <main class="container">
      <div class="shadow rounded alert alert-light">
        <div class="row">
          <div  class="col-md-8">
            <div class="col-10" style="padding: 0px">
                <h3 class="h3"><b>Арбитраж</b></h3>
                <span >
                <a @click="goPage('fl')" href="#">Биржа фриланса </a>
                <a @click="loadProf($store.getters.get_user_info.user.id)" href="#">/ Аккаунт </a>
                <span class="text-muted">/ Арбитраж</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <aside class="col-md-4">
          <div class="shadow alert alert-light vh">
            <h2 class="pointer">Претензии</h2>
            <div class="mt-3 scroll">
              <div
                v-for="task in tasks"
                @click="id = task.id; loadTask();"
                class="shadow media text-muted pt-3 form-section rounded mt-2 user"
              >
                <p class="media-body pb-3 mb-0 lh-125">
                  {{task.title}}
                  <strong class="d-block text-gray-dark">@{{task.author.username}}</strong>
                </p>
              </div>
            </div>
            <b v-show="!tasks">Нет споров</b>
          </div>
        </aside>
        <div class="col-md-8">
          <div class="alert alert-light text-muted shadow vh scroll">
          <h2 class="pointer">Заказ</h2>
          <h3>{{task.title }}</h3>
          <p v-html="task.description"></p>
          <Files :files="files"></Files>
          <div class="row">
            <div class="col-md-2 divHidden" style="padding-top: 30px;text-center;">
              <img
                :src="$store.getters.get_url_media + author.img"
                @click="loadProf(task.author.id)"
                class="divHidden profile_image"
              />
            </div>
            <div style="padding: 0px" class="col-8 mt-2">
              <p>
                <a class="category">{{task.category.name}}</a>
              </p>
              <p style="margin-bottom: 0px">
                <b class="user_image">Дедлайн:</b>
                {{task.deadline| filterDateTime}}
              </p>
              <span>
                <b class="user_image">Дата:</b>
                {{task.createdDate| filterDateTime}}
              </span>
              <p>
                <b class="user_image">Автор:</b>
                <a @click="loadProf(task.author.id)">{{task.author.username}}</a>
              </p>
            </div>
            <div v-if="task.price!=0" class="col-2" style="padding: 0px">
              <p class="price">
                <b>${{task.price}}</b>
              </p>
            </div>
          </div>
            <hr v-if="doneJob"/>
              <div v-if="doneJob" @click="checkWork=!checkWork" class="row pointer">
                <div class="col-11">
                  <h2>Работа</h2>
                </div>
                <div class="col-1 icon-center">
                  <i v-if="!checkWork" class="fa fa-chevron-right"></i>
                  <i v-if="checkWork" class="fa fa-chevron-down"></i>
                </div>
              </div>
            <hr v-if="doneJob"/>
          <div v-if="checkWork && doneJob">
            <p v-html="doneJob.message"></p>
            <Files :files="jobFiles"></Files>
            <div class="row">
              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{doneJob.createdDate| filterDateTime}}
                </span>
                <p class="text-muted">
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(doneJob.author.id)" href="#">{{doneJob.author.username}}</a>
                </p>
              </div>
            </div>
          </div>
            <hr/>
              <div @click="checkDispute=!checkDispute" class="row pointer">
                <div class="col-11">
                  <h2>Претензия</h2>
                </div>
                <div class="col-1 icon-center">
                  <i v-if="!checkDispute" class="fa fa-chevron-right"></i>
                  <i v-if="checkDispute" class="fa fa-chevron-down"></i>
                </div>
              </div>
            <hr/>
          <div v-if="checkDispute && dispute">
            <p>
              {{dispute.message}}
            </p>
          </div>
            <hr />
              <div @click="showDecision=!showDecision" class="row pointer">
                <div class="col-11">
                  <h2>Решение</h2>
                </div>
                <div class="col-1 icon-center">
                  <i v-if="!showDecision" class="fa fa-chevron-right"></i>
                  <i v-if="showDecision" class="fa fa-chevron-down"></i>
                </div>
              </div>
            <hr/>
          <div v-if="showDecision && !decision">
            <div class="row mb-3">
              <div class="col-6 text-center">
                <label class="form-check-label">
                  <input type="radio" class="form-check-input" name="optionsRadios" :value="task.author.id" v-model="rightContractor" checked>
                  Прав заказчик
                </label>
              </div>
              <div class="col-6 text-center">
                <label class="form-check-label">
                  <input type="radio" class="form-check-input" name="optionsRadios" :value="task.contractor.id" v-model="rightContractor">
                  Прав исполнитель
                </label>
              </div>
            </div>
            <textarea
              v-model="message"
              name="text"
              cols="10"
              rows="5"
              class="textarea form-control mb-3"
            ></textarea>
            <button
              @click="sendDecision"
              type="button"
              class="btn btn-outline-warning btn-block btn-dark"
            >Отправить</button>
          </div>
          <div v-if="showDecision && decision">
            <p>Спор решен в пользу <a @click="loadProf(decision.rightContractor.id)" href="#">{{decision.rightContractor.username}}</a></p>
            {{decision.message}}
          </div>
          <p v-show="messages.length>0">
            <hr />
              <div @click="checkDialog=!checkDialog" class="row pointer">
                <div class="col-11">
                  <h2>Диалог</h2>
                </div>
                <div class="col-1 icon-center">
                  <i v-if="!checkDialog" class="fa fa-chevron-right"></i>
                  <i v-if="checkDialog" class="fa fa-chevron-down"></i>
                </div>
              </div>
            <hr />
          </p>
          <div v-show="checkDialog" class="mt-3 mb-3 scroller30" id="d">
            <div v-for="mes in messages">
              <div v-if="isAuthor(mes)" class="media media-chat media-chat-reverse">
                <img class="avatar authorImg" :src="$store.getters.get_url_media + author.img" />
                <div class="media-body">
                  <p>{{mes.text}}</p>
                  <p
                    class="time"
                    style="background-color: transparent; color: gray;"
                  >{{mes.createdDate | filterDateTime}}</p>
                </div>
              </div>
              <div v-if="!isAuthor(mes)" class="media media-chat">
                <img class="avatar" :src="$store.getters.get_url_media + contractor.img" />
                <div class="media-body">
                  <p>{{mes.text}}</p>
                  <p class="time">{{mes.createdDate | filterDateTime}}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import Datepicker from "vuejs-datetimepicker";
import { get, post } from "./../../Ajax/Http";
import Files from "../Files";

export default {
  name: "Arbitration",
  components: {
    Datepicker,
    Files
  },
  data() {
    return {
      task: "",
      show: false,
      files: [],
      jobFiles: [],
      message: "",
      author: "",
      contractor: "",
      recommendations: [],
      doneJob: "",
      tasks: [],
      messages: [],
      roomId: "",
      checkDialog: false,
      checkWork: true,
      dispute: "",
      checkDispute: true,
      showDecision: false,
      rightContractor: "",
      decision: ""
    };
  },
  created() {
    this.loadTasks();
  },
  methods: {
    isAuthor(mes) {
      return this.task.author.id == mes.user.id;
    },
    loadMessages() {
      const url = this.$store.getters.get_url_server + "api/v1/messages/";
      get(
        url,
        response => {
          this.messages = response;
          var block = document.getElementById("d");
          block.scrollTop = 99999;
        },
        { room: this.roomId }
      );
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadRoom() {
      const url = this.$store.getters.get_url_server + "api/v1/room/";
      const data = {
        memberFirst: this.task.author.id,
        memberSecond: this.task.contractor.id
      };
      post(
        url,
        response => {
          this.roomId = response;
          this.loadMessages();
        },
        data
      );
    },
    loadProfiles() {
      const urlAuthor =
        this.$store.getters.get_url_server +
        "api/v2/prof/" +
        this.task.author.id +
        "/";
      get(urlAuthor, response => {
        this.author = response;
      });
      const urlContractor =
        this.$store.getters.get_url_server +
        "api/v2/prof/" +
        this.task.contractor.id +
        "/";
      get(urlContractor, response => {
        this.contractor = response;
      });
    },
    loadDecision() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/dispute/decision/" +
        this.task.id +
        "/";
      get(url, response => {
        this.decision = response;
      }, null, error => {
        this.decision = "";
      });
    },
    sendDecision() {
      const url = this.$store.getters.get_url_server + "api/v1/decision/";
      const decision = {dispute: this.dispute.task, rightContractor: this.rightContractor, message: this.message};
      post(url, response => {
        this.message = "";
        this.loadDecision();
      }, decision);
    },
    loadDoneJob() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/doneJob/" +
        this.task.id +
        "/";
      get(url, response => {
        this.doneJob = response;
      });
    },
    loadFiles() {
      const urlDoneJobFiles =
        this.$store.getters.get_url_server +
        "api/v1/doneJobFiles/" +
        this.task.id +
        "/";
      get(urlDoneJobFiles, response => {
        this.jobFiles = response;
      });

      const urlTaskFiles =
        this.$store.getters.get_url_server +
        "api/v1/allFilesByTask/" +
        this.task.id +
        "/";
      get(urlTaskFiles, response => {
        this.files = response;
      });
    },
    loadDispute(id){
      const url = this.$store.getters.get_url_server + "api/v1/dispute/" + id + "/";
      get(url,response => {
        this.dispute = response;
      });
    },
    loadTask() {
      const url = this.$store.getters.get_url_server + "api/v1/task/" + this.id + "/";
      get(url, response => {
        this.task = response;
        this.loadProfiles();
        this.loadFiles();
        this.loadRoom();
        this.loadDoneJob();
        this.loadDispute(this.task.id)
        this.loadDecision();
      });
    },
    loadTasks() {
       
      var url = this.$store.getters.get_url_server + "api/v1/arbitrationTasks/";
      get(url, resp => {
        this.tasks = resp;
        this.task = this.tasks[0];
        this.id = this.task.id;
        this.loadTask();
         
      });
    }
  },
  checkTask(id) {
    this.id = id;
    this.loadTask();
  },
  filters: {
    filterDateTime(item) {
      let old_date = new Date(item);
      return `${old_date.getDate()}.${old_date.getMonth() +
        1}.${old_date.getFullYear()} в ${old_date.getHours()}:${old_date.getMinutes()}`;
    }
  }
};
</script>
<style>
@media screen and (max-width: 991px) {
  .divHidden {
    display: none;
  }
}

.vh {
  height: 100vh;
}

.authorImg {
  margin-left: 5px;
}

.scroll {
  overflow-y: auto;
  overflow-x: hidden;
  height: 100vh !important;
}

.time {
  background-color: transparent;
  color: gray;
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

.job {
  background-color: #b3ffb3;
}

.profile_image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 10px;
  display: inline-block;
  cursor: pointer;
}

.file {
  width: 55px;
  height: 55px;
  background-color: rgba(255, 255, 255, 0.5);
  font-weight: bold;
}

.media-body .author {
  display: inline-block;
  font-size: 1rem;
  /* color: #6c757d; */
  cursor: pointer;
  font-weight: 700;
}
.media-body .metadata {
  display: inline-block;
  margin-left: 0.5rem;
  color: #6c757d;
  font-size: 0.8125rem;
}

.scroller30{
  overflow-y: auto;
  overflow-x: hidden;
  height: 30vh !important;
}

.pointer{
  cursor: pointer;
}
</style>
