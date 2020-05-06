<template>
  <div>
    <main class="container">
      <FlashMessage></FlashMessage>
      <div class="row">
        <div class="col-md-8">
          <div class="alert alert-light">
            <h1>{{task.title }}</h1>
            <p v-html="task.description"></p>
            <Files :files="files"></Files>
            <div class="row">
              <div class="col-md-2 divHidden" style="padding-top: 30px;text-center;">
                <img
                  :src="$store.getters.get_url_media + profile.img"
                  @click="loadProf(task.author.id)"
                  class="divHidden profile_image"
                />
              </div>
              <div style="padding: 0px" class="col-8 mt-2">
                <p>
                  <a class="category">{{task.category.name}}</a>
                </p>
                <p style="margin-bottom: 0px" class="text-muted">
                  <b class="user_image">Дедлайн:</b>
                  {{task.deadline| filterDateTime}}
                </p>
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{task.createdDate| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(task.author.id)" href>{{task.author.username}}</a>
                </p>
              </div>
              <div v-if="task.price!=0" class="col-2" style="padding: 0px">
                <p class="price">
                  <b>${{task.price}}</b>
                </p>
              </div>
            </div>
            <hr v-if="avtoriz && task.state == 'posted'" />
            <a
              href="#"
              v-if="avtoriz && task.state == 'posted'"
              @click="goEdit()"
              class="btn btn-info btn-block"
            >Редактировать</a>
            <a
              href="#"
              v-if="avtoriz && task.state == 'posted'"
              @click="showDelete = true"
              class="btn btn-danger btn-block"
            >Удалить</a>
          </div>
          <div v-if="doneJob" class="alert alert-light">
            <p v-html="doneJob.message"></p>
            <Files :files="jobFiles"></Files>
            <div class="row">
              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{doneJob.createdDate| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(doneJob.author.id)" href="#">{{doneJob.author.username}}</a>
                </p>
              </div>
            </div>
            <div
              v-if="task.state != 'completed' && task.state != 'arbitration'"
              style="margin: 0px"
            >
              <button
                v-if="task.author.id == $store.getters.get_user_info.user.id"
                class="btn btn-info approved"
                @click="acceptJob()"
              >Принять работу</button>
              <button
                v-if="task.author.id == $store.getters.get_user_info.user.id"
                style="margin-left: 15px"
                type="button"
                class="btn btn-outline-info approved"
                @click="showArbitration = true;"
              >Арбитраж</button>
            </div>
            <div v-if="task.state == 'completed'">
              <b style="color: #17a2b8;">Работа принята</b>
            </div>
            <div v-if="task.state == 'arbitration'">
              <b style="color: #17a2b8;">В арбитраже</b>
            </div>
          </div>
          <Review :id="task.contractor.id" v-if="showReview" @close="showReview = false"></Review>
          <Arbitration
            :id="task.id"
            v-if="showArbitration"
            @close="showArbitration = false"
            @reloadTask="loadTask()"
          ></Arbitration>
          <div v-if="auth && requests && requests.length>0 && !doneJob" class="alert alert-light">
            <h3 class="title-comments">Заявки фрилансеров</h3>
            <ul class="pl-0 ml-0 media-list" v-for="request in requests">
              <li class="media">
                <div class="media-body">
                  <div class="media-heading">
                    <a @click="loadProf(request.author.id)" href>{{request.author.username}}</a>
                    <div class="metadata">
                      <span class="date">{{request.createdDate| filterDateTime}}</span>
                    </div>
                  </div>
                  <div class="media-text text-justify">{{ request.message }}</div>
                </div>
              </li>
              <button
                v-if="!task.approved && task.author.id == $store.getters.get_user_info.user.id && task.state == 'posted'"
                class="btn btn-info approved"
                @click="approvedUser(request.author.id)"
              >Указать исполнителем</button>
              <button
                v-if="task.approved && task.contractor.id !== request.author.id  && task.author.id == $store.getters.get_user_info.user.id && task.state == 'posted'"
                class="btn btn-info approved"
                @click="approvedUser(request.author.id)"
                disabled
              >Указать исполнителем</button>

              <button
                class="btn btn-outline-info"
                v-if="task.approved && isContractor && task.state  == 'in progress'"
                @click="addJob(task.id)"
              >Добавить работу</button>
              <button
                v-if="task.approved && 
                task.author.id == $store.getters.get_user_info.user.id && 
                task.contractor.id == request.author.id && 
                task.state == 'in progress'"
                style="margin-left: 15px"
                type="button"
                class="btn btn-outline-info"
                @click="showArbitration = true;"
              >Арбитраж</button>
              <b
                class="approved"
                v-if="task.approved && task.contractor.id == request.author.id && task.state == 'in progress'"
                style="color: #17a2b8; margin-left: 15px"
              >Выбран исполнителем</b>
              <button
                v-if="!task.approved && task.author.id == $store.getters.get_user_info.user.id && task.state == 'posted'"
                style="margin-left: 15px"
                type="button"
                class="btn btn-outline-info approved"
                @click="showModal = true;"
              >Увеличить сумму и сроки</button>
              <div v-if="task.state == 'arbitration' && task.contractor.id == request.author.id">
                <b style="color: #17a2b8;">В арбитраже</b>
              </div>
              <modal
                :id="task.id"
                :price="task.price"
                :deadline="task.deadline"
                v-if="showModal"
                @close="showModal = false"
                @approved="approvedUser(request.author.id)"
                @reload="loadTask"
              ></modal>
            </ul>
          </div>
          <div v-if="task.state == 'resolved' && decision" class="alert alert-light">
            <h3 class="title-comments">Решение арбитража</h3>
            <p>
              Спор решен в пользу
              <a
                @click="loadProf(decision.rightContractor.id)"
                href="#"
              >{{decision.rightContractor.username}}</a>
            </p>
            <b style="color: #17a2b8;">{{decision.message}}</b>
          </div>
          <div
            v-if="auth && !isAuthor && requests.length<1"
            class="col-12 tweet alert alert-light"
            style="margin-top: 10px"
          >
            <div class="row">
              <div class="col-12">
                <h3 class="title-comments">Новая заявка</h3>
                <textarea v-model="message" rows="3" cols="80" class="form-control"></textarea>
                <div style="padding-top: 10px">
                  <a href="#" @click="sendRequest()" class="btn btn-info">Оставить заявку</a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <aside class="col-md-4">
          <div class="alert alert-light">
            <h3>
              <b>Рекомендованные фрилансеры</b>
            </h3>
            <div v-for="recommendation in recommendations" class="row">
              <div class="col-3">
                <img
                  :src="$store.getters.get_url_media + recommendation.img"
                  class="shadow-lg center-block recommendation_image"
                />
              </div>
              <div style="padding: 0px" class="col-7">
                <a
                  href="#"
                  @click="loadProf(recommendation.user.id)"
                >{{recommendation.user.username}}</a>
                <p v-if="recommendation.user.email">{{recommendation.user.email}}</p>
              </div>
            </div>
          </div>
          <div v-if="isAuthor" class="alert alert-light">
            <h3>
              <b>Статистика заказа</b>
            </h3>
            <p>{{task.visits + " " + getNoun(task.visits, "просмотр", "просмотра", "просмотров")}}</p>
            <p>{{requests.length + " " + getNoun(requests.length, "заявка", "заявки", "заявок")}}</p>
          </div>
        </aside>
      </div>
      <DeleteTask v-if="showDelete" @close="showDelete = false" @removeTask="RemoveTask()"></DeleteTask>
    </main>
  </div>
</template>

<script>
import modal from "./../modal.vue";
import Review from "./../ModalWindows/Review.vue";
import Arbitration from "./../ModalWindows/Arbitration.vue";
import DeleteTask from "./../ModalWindows/DeleteTask.vue";
import Files from "../Files";
import Datepicker from "vuejs-datetimepicker";
import { get, post, del } from "./../../Ajax/Http";

export default {
  name: "TaskDetail",
  components: {
    Datepicker,
    modal,
    Review,
    Arbitration,
    DeleteTask,
    Files
  },
  data() {
    return {
      task: "",
      show: false,
      files: [],
      message: "",
      requests: [],
      profile: "",
      recommendations: [],
      showModal: false,
      doneJob: "",
      jobFiles: [],
      classJob: "alert alert-light",
      showReview: false,
      showArbitration: false,
      showDecision: false,
      showDelete: false,
      decision: ""
    };
  },
  created() {
    this.loadTask();
    this.loadFiles();
    this.loadRequests();
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    },
    avtoriz() {
      if (
        this.$store.getters.get_auth &&
        (this.$store.getters.get_user_info.user.username ==
          this.task.author.username ||
          this.$store.getters.get_user_info.user.username == "Administrator")
      )
        return true;
      else return false;
    },
    isAuthor() {
      return this.$store.getters.get_user_info.user.id == this.task.author.id;
    },
    isContractor() {
      return (
        this.$store.getters.get_user_info.user.id == this.task.contractor.id
      );
    }
  },
  methods: {
    addJob(id) {
      this.$router.push({ name: "addJob", params: { tastId: id } });
    },
    loadDecision() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/dispute/decision/" +
        this.task.id +
        "/";
      get(
        url,
        response => {
          this.decision = response;
        },
        null,
        error => {
          this.decision = "";
        }
      );
    },
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    getNoun(number, one, two, five) {
      let n = Math.abs(number);
      n %= 100;
      if (n >= 5 && n <= 20) {
        return five;
      }
      n %= 10;
      if (n === 1) {
        return one;
      }
      if (n >= 2 && n <= 4) {
        return two;
      }
      return five;
    },
    getExtencion(filename) {
      return filename.split(".").pop();
    },
    goPage(item) {
      this.$router.push({ name: item });
    },
    goEdit() {
      this.$router.push({ name: "editTask", params: { Id: this.task.id } });
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    RemoveTask() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/task/" +
        this.task.id +
        "/";
      del(
        url,
        response => {
          this.showDelete = false;
          this.flashMessage.warning({
            title: "Информация",
            message: "Вы успешно удалили заказ!"
          });
          this.goPage("my_tasks");
        },
        { pk: this.task.id }
      );
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
    loadRecommendations() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/recommendations/" +
        this.task.id +
        "/";
      get(url, response => {
        this.recommendations = response;
      });
    },
    loadProfile() {
      const url =
        this.$store.getters.get_url_server +
        "api/v2/prof/" +
        this.task.author.id +
        "/";
      get(url, response => {
        this.profile = response;
      });
    },
    loadRequests() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/requestsForTask/" +
        this.$route.params.taskId +
        "/";
      get(url, response => {
        this.requests = response;
      });
    },
    loadTask() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/task/" +
        this.$route.params.taskId +
        "/";
      get(url, response => {
        this.task = response;
        this.loadProfile();
        this.loadRecommendations();
        this.loadDoneJob();
        if (this.task.state == "resolved") {
          this.loadDecision();
        }
      });
    },
    loadFiles() {
      const doneJobUrl =
        this.$store.getters.get_url_server +
        "api/v1/doneJobFiles/" +
        this.$route.params.taskId +
        "/";
      get(doneJobUrl, response => {
        this.jobFiles = response;
      });

      const tasksFileUrl =
        this.$store.getters.get_url_server +
        "api/v1/allFilesByTask/" +
        this.$route.params.taskId +
        "/";
      get(tasksFileUrl, response => {
        this.files = response;
      });
    },
    sendRequest() {
      const url = this.$store.getters.get_url_server + "api/v1/my/requests/";
      post(
        url,
        response => {
          this.message = "";
          this.loadRequests();
        },
        {
          message: this.message,
          task: this.task.id
        }
      );
    },
    approvedUser(id) {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/approved/" +
        this.task.id +
        "/";
      put(
        url,
        response => {
          this.loadTask();
        },
        {
          approved: true,
          contractor: id
        }
      );
    },
    acceptJob() {
      const url =
        this.$store.getters.get_url_server + "api/v1/acceptJob/" + this.task.id;
      get(url, response => {
        this.loadTask();
        this.showReview = true;
      });
    },
    getFileName(filename) {
      const fullName = filename.split("/").pop();
      if (fullName.length > 15) return ".." + fullName.substr(9);
      return fullName;
    },
    anotherFile(filename) {
      const extencion = this.getExtencion(filename);
      return (
        extencion != "rar" &&
        extencion != "7zip" &&
        extencion != "png" &&
        extencion != "jpg" &&
        extencion != "svg" &&
        extencion != "gif" &&
        extencion != "txt" &&
        extencion != "doc" &&
        extencion != "docx"
      );
    },
    rarFile(filename) {
      const extencion = this.getExtencion(filename);
      return extencion == "rar" || extencion == "7zip";
    },
    docFile(filename) {
      const extencion = this.getExtencion(filename);
      return extencion == "txt" || extencion == "doc" || extencion == "docx";
    }
  },
  filters: {
    // Фильтр полной даты числами
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

.job {
  background-color: rgb(232, 243, 232);
}

.recommendation_image {
  width: 50px;
  height: 50px;
}

.profile_image {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 10px;
  display: inline-block;
  cursor: pointer;
}

.approved {
  margin-top: 20px;
}

.filesDiv {
  border-top: 2px solid #f0f0f0;
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  text-align: center;
  color: gray;
}

.file {
  width: 55px;
  height: 55px;
  background-color: rgba(255, 255, 255, 0.5);
  font-weight: bold;
}

html {
  font-size: 16px;
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

.title-comments {
  font-size: 1.4rem;
  font-weight: bold;
  line-height: 1.5rem;
  color: #6c757d;
  margin-bottom: 1rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid rgba(34, 36, 38, 0.15);
}

.tweet {
  padding: 10px;
  border: 1px solid #bfbfbf;
  background: #fafafa;
  box-sizing: border-box;
  margin-right: 0;
  margin-left: 0;
}
</style>
