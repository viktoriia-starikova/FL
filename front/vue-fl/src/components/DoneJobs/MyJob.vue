<template>
  <div>
    <main class="container">
      <div class="row">
        <div v-if="jobs.length<1" class="col-md-8">
          <h1>У вас нет готовых работ</h1>
        </div>
        <div v-if="jobs.length>0" class="col-md-8">
          <p>
            <input
              class="test form-control"
              v-model="search"
              type="text"
              maxlength="150"
              placeholder="Поиск"
            />
          </p>
          <div class="alert alert-light" v-for="job in filteredList">
            <p>{{job.message| truncate(320, '...')}}</p>
            <div class="row">
              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{job.createdDate| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(job.author.id)" href="#">{{job.author.username}}</a>
                </p>
              </div>
            </div>
            <a href @click="loadJob(job.task.id)" class="btn btn-outline-warning">Читать далее</a>
          </div>

          <div v-if="filteredList.length>0" id="pag" class="clearfix btn-group">
            <button
              type="button"
              class="btn btn-warning"
              v-if="page != 1"
              @click="page--"
            >Предыдущая</button>
            <button
              type="button"
              class="btn btn-outline-warning"
              v-for="pageNumber in pages.slice(page-1, page+5)"
              @click="page = pageNumber"
            >{{pageNumber}}</button>
            <button
              type="button"
              @click="page++"
              v-if="page < pages.length"
              class="btn btn-warning"
            >Следующая</button>
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

    <footer>
      <div class="container">
        <p class="float-right">
          <a href="#">Наверх</a>
        </p>
        <p>
          Впервые на нашем сайте?
          <a href="/">Посетите главную</a> или прочитайте
          <a @click="goPage('about')" href>о нас</a>.
        </p>
      </div>
    </footer>
  </div>
</template>

<script>
import Fuse from "fuse.js";
import { get, post } from "./../../Ajax/Http";

export default {
  name: "myJob",
  props: {
    jobs: "",
    mess: ""
  },
  created() {
    this.loadJobs();
    this.loadPosts();
  },
  data() {
    return {
      jobId: "",
      page: 1,
      perPage: 5,
      pages: [],
      search: "",
      posts: []
    };
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    },
    displayedJobs(rez) {
      return this.paginate(rez);
    },
    loadPosts() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/intrestingPosts/" +
        this.$store.getters.get_user_info.user.id +
        "/";
        get(url, response => {
          this.posts = response;
        });
    },
    filteredList() {
      var search = this.search;
      if (search.length < 1) return this.paginate(this.jobs);
      var options = {
        keys: ["message"]
      };
      var fuse = new Fuse(this.jobs, options);
      var res = fuse.search(search);
      return this.paginate(res);
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadJobs() {
      const url = this.$store.getters.get_url_server + "api/v1/my/doneJobs/";
      get(url, response => {
        this.jobs = response;
        console.log("Все посты успешно загружены");
      });
    },
    loadJob(id) {
      this.$router.push({ name: "task_detail", params: { taskId: id } });
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    setPages() {
      let numberOfPages = Math.ceil(this.jobs.length / this.perPage);
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    },
    paginate(jobs) {
      let page = this.page;
      let perPage = this.perPage;
      let from = page * perPage - perPage;
      let to = page * perPage;
      return jobs.slice(from, to);
    }
  },
  watch: {
    jobs() {
      this.setPages();
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
.test {
  padding: 5px 5px 5px 40px;
  background: url(https://cemsertoglu.files.wordpress.com/2015/11/system-search-svg.png)
    no-repeat 3px 1px;
  background-size: auto 90%;
}
#pag {
  margin-bottom: 50px;
}

.material-icons {
  color: orange;

  position: inherit;
  padding: 3px;
  top: 5px;
  cursor: pointer;
}
#loginModal {
  color: orange;
  position: inherit;
  padding: 3px;
  top: 5px;
  cursor: not-allowed;
}

.glyphicon-thumbs-up {
  color: orange;
  position: relative;
  cursor: pointer;
}
</style>
