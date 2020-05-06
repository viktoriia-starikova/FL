<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Вы точно хотите удалить статью "{{postid.title}}"</h2>
            <form method="POST">
              <button
                type="button"
                @click="deletePost()"
                class="btn btn-outline-danger"
                name="button"
              >Удалить</button>
              <a href="#" @click="goPage('my_posts')">Нет, отмена</a>
            </form>
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
import { get, post, del } from "./../../Ajax/Http";

export default {
  name: "PostDetail",
  data() {
    return {
      postid: ""
    };
  },
  created() {
    this.loadPost();
  },
  beforeCreate() {
    const url =
      this.$store.getters.get_url_server +
      "api/v1/posts/" +
      this.$route.params.Id +
      "/";
    get(
      url,
      response => {
        this.postid = response;
      },
      {
        pk: this.$route.params.Id
      }
    );
  },
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
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
        this.$route.params.Id +
        "/";
      get(url, response => {
        this.postid = response;
      });
    },
    deletePost(id) {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/posts/" +
        this.$route.params.Id +
        "/";
      del(
        url,
        response => {
          window.location = "/my";
        },
        {
          pk: id
        }
      );
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
</style>
