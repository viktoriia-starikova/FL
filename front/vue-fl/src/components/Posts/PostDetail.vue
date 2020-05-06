<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="alert alert-light">
            <h1>{{postid.title }}</h1>
            <p v-html="postid.text"></p>
            <div class="row">
              <div class="col-12" name="block">
                <b>{{ postid.like }}</b>
                <i v-if="auth" @click="like(postid.id)" class="material-icons">thumb_up</i>
                <i v-if="!auth" id="loginModal" class="material-icons">thumb_up</i>

                <b>{{ comments.length }}</b>
                <i @click="showComments()" class="material-icons">insert_comment</i>
              </div>
              <div class="mt-2">
                <span class="text-muted">
                  <b class="user_image">Дата:</b>
                  {{postid.date| filterDateTime}}
                </span>
                <p>
                  <b class="user_image">Автор:</b>
                  <a @click="loadProf(postid.avtor.id)" href>{{postid.avtor.username}}</a>
                </p>
              </div>
            </div>
            <hr />
            <a
              href="#"
              v-if="avtoriz"
              @click="updatePost(postid.id)"
              class="btn btn-info btn-block"
            >Редактировать</a>
            <a
              href="#"
              v-if="avtoriz"
              @click="DeletePost(postid.id)"
              class="btn btn-danger btn-block"
            >Удалить</a>
          </div>

          <div v-if="show && comments.length>0" class="col-12 tweet alert alert-light">
            <h3 class="title-comments">Комментарии</h3>
            <ul class="media-list" v-for="sub in comments">
              <li class="media">
                <div class="media-body">
                  <div class="media-heading">
                    <a @click="loadProf(sub.avtor.id)" href>{{sub.avtor.username}}</a>
                    <div class="metadata">
                      <span class="date">{{sub.date| filterDateTime}}</span>
                    </div>
                  </div>
                  <div class="media-text text-justify">{{ sub.text }}</div>
                </div>
              </li>
              <hr />
            </ul>
          </div>
          <div v-if="auth" class="alert alert-light col-12 tweet mt-3">
            <div class="row">
              <div class="col-12">
                <h3 class="title-comments">Ваш комментарий</h3>
                <textarea v-model="comment" rows="2" cols="80" class="form-control"></textarea>
                <div style="padding-top: 10px">
                  <button
                    @click="sendComment()"
                    type="submit"
                    class="btn btn-warning"
                  >Комментировать</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <aside class="col-md-4">
          <div class="p-3 rounded nb-3">
            <h3>
              <b>HTML, который мы потеряли</b>
            </h3>
            <p>
              В этом году исполняется 30 лет с тех пор, как Бернерс-Ли начал разрабатывать язык HTML. С тех пор мы прошли долгий путь, начиная с восхищения новой технологией,
              и заканчивая лечением интернет-зависимости и цензурой. Каких только бед не принес нам Интернет, взломанные пароли, кража личных данных,
              компьютерные вирусы, черви, а теперь даже вирусы-вымогатели. Вы когда-нибудь задумывались, почему Сеть до сих пор остается такой нестабильной и уязвимой?
              Где-то на этом длинном пути мы свернули не туда? Давайте разбираться.HTML 1.0, опубликованный в 1993 году, включал всего 13 элементов
              (считая только те, которые сохранились до наших дней):
              <br />
              <i>
                <b>a, address, base, dd, dir, dl, dt, h1..h6, li, p, plaintext, title, ul</b>
              </i>
            </p>
            <a href="https://habr.com/ru/post/440336/" title="Посмотреть на habr" target="_blank">
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
  </div>
</template>

<script>
import { get, post } from "./../../Ajax/Http";

export default {
  name: "PostDetail",

  data() {
    return {
      postid: "",
      comment: "",
      comments: "",
      show: false
    };
  },
  created() {
    this.loadPost();
    this.loadComment();
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
          this.postid.avtor.username ||
          this.$store.getters.get_user_info.user.username == "Administrator")
      )
        return true;
      else return false;
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    showComments() {
      if (this.show) this.show = false;
      else this.show = true;
    },
    loadProf(id) {
      if (this.$store.getters.get_user_info.user.id == id) {
        this.$router.push({ name: "profile", params: { Id: id } });
      } else {
        this.$router.push({ name: "publicProfile", params: { Id: id } });
      }
    },
    loadComment() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/comment/" +
        this.$route.params.postId +
        "/";
      get(url, response => {
        this.comments = response;
      });
    },
    sendComment() {
      const url = this.$store.getters.get_url_server + "api/v1/comment/";
      post(
        url,
        response => {
          this.comment = "";
          this.loadComment();
        },
        {
          text: this.comment,
          post: this.$route.params.postId
        }
      );
    },
    like(id) {
      const url = this.$store.getters.get_url_server + "api/v1/like/";
      post(
        url,
        response => {
          this.loadPost();
        },
        {
          pk: id
        }
      );
    },
    loadPost() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/posts/" +
        this.$route.params.postId +
        "/";
      get(url, response => {
        this.postid = response;
      });
    },
    DeletePost(id) {
      this.$router.push({ name: "delete_post", params: { Id: id } });
    },
    updatePost(id) {
      this.$router.push({ name: "edit_post", params: { Id: id } });
    }
  },
  filters: {
    // Фильтр полной даты числами
    filterDateTime(item) {
      let old_date = new Date(item);
      return `
                 ${old_date.getDate()}.${old_date.getMonth() +
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
