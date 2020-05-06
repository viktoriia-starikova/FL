<template>
  <div>
    <main class="container">
      <div class="rounded alert alert-light">
        <div class="row">
          <div class="col-md-8">
            <div class="col-10" style="padding: 0px">
              <h3 class="h3">
                <b>Работа из портфолио</b>
              </h3>
              <span>
                <a @click="goPage('fl')" href="#">Биржа фриланса</a>
                <a @click="loadProf(work.avtor.id)" href="#">/ {{work.avtor.username}}</a>
                <span class="text-muted">/ Работа из портфолио</span>
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-8">
          <div class="alert alert-light">
            <h1>{{work.title }}</h1>
            <p v-html="work.text"></p>
            <img :src="$store.getters.get_url_media + work.img" class="img-thumbnail" />
            <Files :files="files"></Files>
            <div class="row">
              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{work.date| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(work.avtor.id)" href>{{work.avtor.username}}</a>
                </p>
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
  </div>
</template>

<script>
import { get } from "./../../Ajax/Http";
import Files from "../Files";

export default {
  name: "PostDetail",
  components: {
    Files
  },
  data() {
    return {
      work: {},
      posts: [],
      files: []
    };
  },
  created() {
    this.loadPortfolioWork();
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    }
  },
  methods: {
    loadPost(id) {
      this.$router.push({ name: "post_detail", params: { postId: id } });
    },
    loadPosts() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/intrestingPosts/" +
        this.work.avtor.id +
        "/";
      get(url, response => {
        this.posts = response;
      });
    },
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    loadPortfolioWork() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/portfolioDetail/" +
        this.$route.params.id;
      get(url, response => {
        this.work = response.portfolio;
        this.files = response.files;
        this.loadPosts();
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

#loginModal {
  color: orange;
  position: inherit;
  padding: 3px;
  top: 5px;
  /* left: 620px; */
  cursor: not-allowed;
}
#com {
  left: 20px;
}
</style>
