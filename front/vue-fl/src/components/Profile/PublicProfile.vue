<template>
  <div>
    <div v-if="loading">Загрузка...</div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Профиль пользователя</h2>
            <div class="container">
              <div class="row alert alert-light" style="margin-bottom: 0px;">
                <div v-if="user.positiveAssessment>0" class="col text-center center-block rating">
                  <span>
                    <b>{{ user.positiveAssessment }}</b>
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
              <p class="media-body pb-3 mb-0 lh-125 border-bottom border-gray">
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
            <div class="mt-4 ml-3">
              <button
                @click="loadChat()"
                style="width: 164px; font-size: 9pt"
                class="btn btn-warning"
              >Отправить сообщение</button>
            </div>
            <hr v-if="portfolioWorks.length>0" />
            <div v-if="portfolioWorks.length>0">
              <div @click="checkPortfolio=!checkPortfolio" class="row portfolio">
                <div class="col-11">
                  <h2>Портфолио</h2>
                </div>
                <div class="col-1 icon-center">
                  <i v-if="!checkPortfolio" class="fa fa-chevron-right"></i>
                  <i v-if="checkPortfolio" class="fa fa-chevron-down"></i>
                </div>
              </div>
            </div>
            <hr v-if="portfolioWorks.length>0" />
            <div v-if="checkPortfolio" class="row">
              <div v-for="work in portfolioWorks" class="col-md-5 alert alert-light m-4">
                <h5>{{work.title | truncate(30, '...')}}</h5>
                <p>{{work.text | truncate(60, '...')}}</p>
                <div class="p-3 mb-3">
                  <p style="text-align: center;">
                    <img
                      class="img-thumbnail"
                      v-if="work.img"
                      style="width: 210px; height: 170px; "
                      :src="$store.getters.get_url_media + work.img"
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
          </div>
        </div>
        <aside v-if="posts.length" class="col-md-4">
          <div class="p-3 rounded nb-3">
            <h2 style="color: #b38a22;">Популярные посты</h2>
            <div v-for="post in posts" class="alert alert-light">
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
    <FlashMessage></FlashMessage>
  </div>
</template>


<script>
import { get, post, put } from "./../../Ajax/Http";

export default {
  data() {
    return {
      username: "",
      email: "",
      mess: "",
      mess1: "",
      loading: false,
      user: "",
      portfolioWorks: [],
      posts: [],
      checkPortfolio: false,
      post: "",
      reviews: [],
      showReview: false
    };
  },
  created() {
    this.loadProf();
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    }
  },
  methods: {
    loadPortfolioWork(id) {
      this.$router.push({ name: "portfolioWorkDetail", params: { id: id } });
    },
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadPost(id) {
      this.$router.push({ name: "post_detail", params: { postId: id } });
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
    loadChat() {
      this.$router.push({ name: "dialog", params: { id: this.user.user.id } });
    },
    loadPosts() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/intrestingPosts/" +
        this.$route.params.Id +
        "/";
      get(url, response => {
        this.posts = response;
      });
    },
    loadProf(context) {
      const url =
        this.$store.getters.get_url_server +
        "api/v2/prof/" +
        this.$route.params.Id +
        "/";
      get(url, response => {
        this.user = response;
        this.email = this.user.user.email;
        this.username = this.user.user.username;
        this.loadPortfolio();
        this.loadPosts();
        this.loadReview();
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
.portfolio {
  cursor: pointer;
  display: flex;
  color: #b38a22;
}
.rating {
  font-size: 14px;
}
.icon-center {
  margin: auto;
}
.icon-settings {
  cursor: pointer;
  position: absolute;
  right: 10px;
  color: black;
}
</style>