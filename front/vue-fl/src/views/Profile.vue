<template>
  <div>
    <transition name="modal" v-if="showModal">
      <div class="modal-mask">
        <div class="modal-wrapper">
          <div class="portfolio-modal">
            <div class="modal-body">
              <slot name="header">
                <button
                  type="button"
                  class="btn-close"
                  style="right:0px; top: 0px;position:absolute;"
                  @click="showModal=false"
                  aria-label="Close modal"
                >&times;</button>
                <h3>
                  <b>Работа из портфолио</b>
                </h3>
              </slot>
              <hr />
              <slot name="body">
                <div class="border-bottom pb-4">Вы действительно хотите удалить работу?</div>
              </slot>
            </div>
            <slot name="footer">
              <button class="btn btn-warning rounded ml-2" @click="DeleteProfile()">Удалить</button>
              <button class="btn btn-outline-warning rounded ml-2" @click="showModal=false">Нет</button>
            </slot>
          </div>
        </div>
      </div>
    </transition>

    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="shadow form-section">
            <h2>Личный кабинет</h2>
            <div class="container">
              <div class="row alert alert-light" style="margin-bottom: 0px;">
                <div v-if="user.positiveAssessment>0" class="col text-center center-block rating">
                  <span>
                    <b>{{ user.positiveAssessment}}</b>
                  </span>
                  <p>положительных оценок</p>
                </div>
                <div v-if="user.positiveAssessment==0" class="col text-center center-block rating">
                  <span>
                    <b>&mdash;</b>
                  </span>
                  <p>недостаточно оценок</p>
                </div>

                <div v-if="user.rating>0" class="col text-center center-block rating">
                  <span>
                    <b>{{ user.rating.toFixed(1) }} из 5</b>
                  </span>
                  <p>по оценкам заказчика</p>
                </div>
                <div v-if="user.rating==0" class="col text-center center-block rating">
                  <span>
                    <b>&mdash;</b>
                  </span>
                  <p>недостаточно оценок</p>
                </div>

                <div v-if="user.negativeAssessment>0" class="col text-center center-block rating">
                  <span>
                    <b>{{user.negativeAssessment}}</b>
                  </span>
                  <p>отрицательных оценок</p>
                </div>
                <div v-if="user.negativeAssessment==0" class="col text-center center-block rating">
                  <span>
                    <b>&mdash;</b>
                  </span>
                  <p>недостаточно оценок</p>
                </div>
              </div>
            </div>
            <div class="media text-muted pt-3">
              <div class="mr-2 rounded" width="0" height="0">
                <img
                  class="mr-2 rounded"
                  style="width: 164px; height: 164px;"
                  :src="$store.getters.get_url_media + user.img"
                />
              </div>
              <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
                <strong class="d-block text-gray-dark">@{{user.user.username}}</strong>
                <b v-if="email">Email:</b>
                {{ user.user.email }}
              </p>
            </div>
            <div class="ml-4">
              <star-rating
                active-color="#ffc107"
                v-model="user.rating"
                :star-size="20"
                :read-only="true"
                :border-width="3"
                :show-rating="false"
                v-bind:increment="0.1"
              ></star-rating>
            </div>
            <hr v-if="portfolioWorks.length > 0" />
            <div
              v-if="portfolioWorks.length > 0"
              @click="checkPortfolio=!checkPortfolio"
              class="row portfolio"
            >
              <div class="col-md-11">
                <h2>Портфолио</h2>
              </div>
              <div class="col-md-1 icon-center">
                <i v-if="!checkPortfolio" class="fa fa-chevron-right"></i>
                <i v-if="checkPortfolio" class="fa fa-chevron-down"></i>
              </div>
            </div>
            <hr v-if="portfolioWorks.length > 0" />
            <div class="row" v-show="checkPortfolio">
              <div v-for="work in portfolioWorks" class="col-md-5 alert alert-light m-4">
                <div>
                  <i
                    @click="showModal = true; portfolioId = work.id"
                    class="fa fa-trash portfolioIcon"
                  ></i>
                  <i @click="editPortfolioWork(work.id)" class="icon-settings fa fa-cog fa-fw"></i>
                </div>
                <h5>{{work.title | truncate(30, '...')}}</h5>
                <p>{{work.text | truncate(60, '...')}}</p>
                <div class="p-3 mb-3">
                  <p style="text-align: center;">
                    <img
                      v-if="work.img"
                      style="width: 210px; height: 170px; "
                      :src="$store.getters.get_url_media + work.img"
                      class="img-thumbnail"
                    />
                  </p>
                </div>
                <button
                  @click="loadPortfolioWork(work.id)"
                  class="btn btn-outline-warning"
                  style="bottom: 15px; position: absolute; "
                >Посмотреть</button>
              </div>
            </div>
            <hr v-if="reviews.length > 0" />
            <div v-if="reviews.length > 0" @click="showReview=!showReview" class="row portfolio">
              <div class="col-md-11">
                <h2>Отзывы</h2>
              </div>
              <div class="col-md-1 icon-center">
                <i v-if="!showReview" class="fa fa-chevron-right"></i>
                <i v-if="showReview" class="fa fa-chevron-down"></i>
              </div>
            </div>
            <hr v-if="reviews.length > 0" />
            <div v-if="showReview" class="scroller50">
              <div v-for="review in reviews" class="row">
                <div class="col-1"></div>
                <div class="col-10 alert alert-light">
                  <div class="row">
                    <div class="col-12">
                      <h5>{{review.message}}</h5>
                    </div>
                    <div class="col-12">
                      <b>@{{review.addressee.username}}</b>
                      <br />
                      <b>Дата:</b>
                      {{review.createdDate | filterDateTime}}
                    </div>
                  </div>
                </div>
                <div class="col-1"></div>
              </div>
            </div>
            <hr />
            <div @click="checkRedact=!checkRedact" class="row portfolio">
              <div class="col-md-11">
                <h2>Редактировать данные пользователя</h2>
              </div>
              <div class="col-md-1 icon-center">
                <i v-if="!checkRedact" class="fa fa-chevron-right"></i>
                <i v-if="checkRedact" class="fa fa-chevron-down"></i>
              </div>
            </div>
            <hr />
            <form method="POST" v-show="checkRedact">
              <div class="form-group">
                <label class="col-form-label requiredField">
                  <b>Имя пользователя</b>
                  <b class="asteriskField">*</b>
                </label>
                <div class>
                  <input
                    v-model="username"
                    type="text"
                    maxlength="150"
                    class="textinput textInput form-control"
                  />
                  <p id="p">{{ mess }}</p>
                  <small
                    class="form-text text-muted"
                  >Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.</small>
                </div>
              </div>
              <div class="form-group">
                <label for="id_email" class="col-form-label">
                  <b>Адрес электронной почты</b>
                </label>
                <div class>
                  <input
                    v-model="email"
                    type="email"
                    maxlength="254"
                    class="emailinput form-control"
                  />
                  <p id="p">{{ mess1 }}</p>
                </div>
              </div>
              <div class="form-group">
                <label class="col-form-label requiredField">
                  <b>Изображение профиля</b>
                  <b class="asteriskField">*</b>
                </label>
                <div class>
                  <div class="not-selected-input">
                    <div class="form-group">
                      <input
                        @change="inputChange()"
                        type="file"
                        name="file"
                        id="file"
                        class="input-file"
                        multiple="true"
                      />
                      <label for="file" class="btn btn-tertiary js-labelFile">
                        <i class="icon fa fa-check"></i>
                        <span class="js-fileName">Загрузить файл</span>
                      </label>
                    </div>
                  </div>На данный момент:
                  <a
                    :href="$store.getters.get_url_server + $store.getters.get_user_info.img"
                  >{{$store.getters.get_user_info.img}}</a>
                </div>
              </div>
              <button
                type="button"
                @click="updateProfile($store.getters.get_user_info.user.id)"
                class="shadow-lg btn btn-outline-warning btn-block btn-dark"
                name="button"
              >Обновить данные</button>
            </form>
          </div>
        </div>
        <aside v-if="posts.length" class="col-md-4">
          <div class="p-3 rounded nb-3">
            <h2 style="color: #b38a22;">Популярные посты</h2>
            <div v-for="post in posts" class="shadow alert alert-light">
              <h3>
                <b>{{post.title}}</b>
              </h3>
              <p>{{post.text| truncate(300, '...')}}</p>
              <div class="col-12 mb-3">
                <b>{{ post.like }}</b>
                <i id="loginModal" class="material-icons">thumb_up</i>
              </div>
              <button @click="loadPost(post.id)" class="btn btn-warning">Посмотреть</button>
            </div>
          </div>
        </aside>
      </div>
    </main>
    <FlashMessage :position="'right bottom'" />
  </div>
</template>

<script>
import { get, put, post, postFiles } from "./../Ajax/Http";

export default {
  data() {
    return {
      username: "",
      email: "",
      mess: "",
      mess1: "",
      loading: false,
      user: "",
      rating: 0,
      portfolioWorks: [],
      showModal: false,
      portfolioId: 0,
      checkPortfolio: false,
      checkRedact: true,
      posts: [],
      reviews: [],
      showReview: false
    };
  },
  created() {
    this.loadProf();
    this.loadReview();
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    }
  },
  methods: {
    loadPosts() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/intrestingPosts/" +
        this.user.user.id +
        "/";
      get(url, response => {
        this.posts = response;
      });
    },
    editPortfolioWork(id) {
      this.$router.push({ name: "editPortfolio", params: { Id: id } });
    },
    loadPost(id) {
      this.$router.push({ name: "post_detail", params: { postId: id } });
    },
    loadPortfolioWork(id) {
      this.$router.push({ name: "portfolioWorkDetail", params: { id: id } });
    },
    setRating(rating) {
      this.rating = rating;
    },
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadProf() {
      const url = this.$store.getters.get_url_server + "api/v2/";
      get(url, response => {
        this.user = response;
        this.email = this.user.user.email;
        this.username = this.user.user.username;
        this.rating = response.rating;
        this.loadPortfolio();
        this.loadPosts();
      });
    },
    loadPortfolio() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/portfolio/" +
        this.user.user.id +
        "/";
      get(url, response => {
        this.portfolioWorks = response;
        console.log("Все работы успешно загружены!");
      });
    },
    loadReview() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/my/reviews/" +
        this.user.user.id +
        "/";
      get(url, response => {
        this.reviews = response;
      });
    },
    DeleteProfile() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/portfolioDetail/" +
        this.portfolioId;
      del(url, response => {
        this.showModal = false;
        this.flashMessage.warning({
          title: "Информация",
          message: "Работа удалена из профиля!"
        });
        this.loadPortfolio();
      });
    },
    updateIMG(id) {
      const file = $("#file");
      const result = $("#result");
      if (file.prop("files").length) {
        const formData = new FormData();
        formData.append("img", file.prop("files")[0]);
        formData.append("pk", id);
        const url =
          this.$store.getters.get_url_server +
          "api/v2/update-ava/" +
          this.user.id +
          "/";
        postFiles(
          url,
          response => {
            window.location.reload();
          },
          formData,
          response => {
            console.log("Аватар не загружен");
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, выберите другую фотографию!"
            });
          }
        );
      }
    },
    updateProfile(id) {
      this.updateIMG(this.$store.getters.get_user_info.id);
      const url =
        this.$store.getters.get_url_server +
        "api/v2/red/" +
        this.user.user.id +
        "/";
      put(
        url,
        response => {
          this.mess = "";
          this.mess1 = "";
          this.flashMessage.warning({
            title: "Информация",
            message: "Вы успешно обновили свой профиль!"
          });
          this.loadProf();
        },
        {
          pk: id,
          username: this.username,
          email: this.email
        },
        response => {
          console.log("Профиль не обновлен");
          this.flashMessage.error({
            title: "Ошибка",
            message: "Пожалуйста, заполните правильно все поля!"
          });
          if (response.status === 400) {
            this.mess = response.responseJSON.username[0];
            this.mess1 = response.responseJSON.email[0];
          }
        }
      );
    },
    onFileChange(e) {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      this.createImage(files[0]);
      this.formData.append("file", files[0]);
      this.file = files[0];
    },
    createImage(file) {
      var image = new Image();
      var reader = new FileReader();
      var vm = this;
      reader.onload = function(e) {
        vm.image = e.target.result;
      };
      reader.readAsDataURL(file);
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
.portfolioIcon {
  position: absolute;
  right: 40px;
  color: black;
  cursor: pointer;
}

.portfolio-modal {
  width: 450px;
  height: 205px;
  margin: 0px auto;
  padding: 5px 20px;
  background-color: #fff;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;
}
</style>