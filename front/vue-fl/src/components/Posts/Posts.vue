 <template>
  <div>
    <main class="container">
      <div class="row">
        <div v-if="posts.length<1" class="col-md-8">
          <h1>Нет постов</h1>
        </div>
        <div v-if="posts.length>0" class="col-md-8">
          <p>
            <input
              class="test form-control shadow"
              v-model="search"
              type="text"
              maxlength="150"
              placeholder="Поиск"
            />
          </p>
          <div class="alert alert-light shadow" v-for="post in filteredList">
            <h1>{{post.title }}</h1>
            <p>{{post.text| truncate(320, '...')}}</p>
            <div class="row">
              <div class="col-12" id="lala">
                <b>{{ post.like }}</b>
                <i v-if="auth" @click="like(post.id)" class="material-icons">thumb_up</i>
                <i v-if="!auth" id="loginModal" class="material-icons">thumb_up</i>
              </div>

              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{post.date| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(post.avtor.id)" href="#">{{post.avtor.username}}</a>
                </p>
              </div>
            </div>
            <a href @click="loadPost(post.id)" class="btn btn-outline-warning">Читать далее</a>
          </div>
          <div v-if="filteredList.length<1" class="col-md-8">
            <h1>Нет постов</h1>
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

        <aside class="col-md-4">
          <div class="p-3 rounded nb-3">
            <p></p>
            <h3>
              <b>Знакомство с простейшей нейронной сетью и ее пошаговая реализация</b>
            </h3>
            <div class="p-3 mb-3">
              <img
                src="https://habrastorage.org/getpro/habr/post_images/747/592/94e/74759294e47907f3e8ba14438ab66001.jpg"
                class="img-thumbnail"
              />
            </div>
            <p>
              Эта статья для тех, кто хочет заниматься нейронными сетями и машинным обучением, но пока с трудом понимает эту удивительную область науки. Ниже будет описан самый простой скелет
              кода нейронной сети, чтобы многие поняли простейший принцип построения и взаимодействия всего того, из чего состоит эта нейронная сеть.
            </p>
            <a href="https://habr.com/ru/post/440190/" title="Посмотреть на habr" target="_blank">
              <button class="btn btn-warning">Посмотреть</button>
            </a>
            <p></p>
            <h3>
              <b>Разгоняем обработку событий до 1,6 миллионов в секунду</b>
            </h3>
            <div class="p-3 mb-3">
              <img
                src="https://habrastorage.org/webt/q8/s-/cq/q8s-cqlxfrv8abkdotnudzeq1u8.jpeg"
                class="img-thumbnail"
              />
            </div>
            <p>
              Когда участники HighLoad++ пришли на доклад Александра Крашенинникова, они надеялись услышать про обработку 1 600 000 событий в секунду. Ожидания не оправдались…
              Потому что во время подготовки к выступлению эта цифра улетела до 1 800 000 — так, на HighLoad++ реальность превосходит ожидания.
            </p>
            <a
              href="https://habr.com/ru/company/badoo/blog/442616/"
              title="Посмотреть на habr"
              target="_blank"
            >
              <button class="btn btn-warning">Посмотреть</button>
            </a>
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
import { get, post, put } from "./../../Ajax/Http";
import Fuse from "fuse.js";

export default {
  name: "Posts",
  props: {
    posts: "",
    mess: ""
  },
  create() {
    console.log(this.$store.getters.get_user_info.img);
  },
  data() {
    return {
      postid: "",
      page: 1,
      perPage: 5,
      pages: [],
      search: ""
    };
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    },
    displayedPosts(rez) {
      return this.paginate(rez);
    },
    filteredList() {
      var search = this.search;
      if (search.length < 1) return this.paginate(this.posts);
      var options = {
        keys: ["title", "text"]
      };
      var fuse = new Fuse(this.posts, options);
      var res = fuse.search(search);
      return this.paginate(res);
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    like(id) {
      const url = this.$store.getters.get_url_server + "api/v1/like/";
      post(url, response =>{ this.$emit("reload")}, {
        pk: id
      });
    },
    loadPosts() {
      const url = this.$store.getters.get_url_server + "api/v1/";
      get(url, response => {
        this.posts = response;
      });
    },
    loadPost(id) {
      this.$router.push({ name: "post_detail", params: { postId: id } });
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    setPages() {
      let numberOfPages = Math.ceil(this.posts.length / this.perPage);
      this.pages = [];
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    },
    setPages2(posts) {
      let numberOfPages = Math.ceil(posts.length / this.perPage);
      pages = [];
      for (let index = 1; index <= numberOfPages; index++) {
        pages.push(index);
      }
    },
    paginate(posts) {
      let page = this.page;
      let perPage = this.perPage;
      let from = page * perPage - perPage;
      let to = page * perPage;
      return posts.slice(from, to);
    }
  },
  watch: {
    posts() {
      this.setPages();
    },
    search() {
      this.setPages2(this.filteredList());
    }
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
