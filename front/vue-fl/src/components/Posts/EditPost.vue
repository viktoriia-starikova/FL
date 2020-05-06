<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Редактировать статью</h2>
            <form method="post">
              <div id="div_id_title" class="form-group">
                <label for="id_title" class="col-form-label requiredField">
                  Заголовок
                  <span class="asteriskField">*</span>
                </label>
                <div class>
                  <input
                    v-model="title"
                    type="text"
                    name="title"
                    maxlength="50"
                    class="textinput textInput form-control"
                  />
                </div>
              </div>
              <div class="form-group">
                <label for="id_text" class="col-form-label requiredField">
                  Текст
                  <span class="asteriskField">*</span>
                </label>
                <ul class="ul">
                  <button
                    @click="addTagB"
                    title="Жирный"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>B</b>
                  </button>
                  <button
                    @click="addTagH"
                    title="Заголовок"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>H</b>
                  </button>
                  <button
                    @click="addTagI"
                    title="Курсив"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>
                      <i>I</i>
                    </b>
                  </button>
                  <button
                    @click="addTagU"
                    title="Подчеркнутый"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>
                      <u>U</u>
                    </b>
                  </button>
                  <button
                    @click="addTagS"
                    title="Зачеркнутый"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>
                      <s>S</s>
                    </b>
                  </button>
                  <button
                    @click="addTagA"
                    title="Ссылка"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>A</b>
                  </button>
                  <button
                    @click="addTagO"
                    title="Список"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>Ol</b>
                  </button>
                  <button
                    @click="addTagImg"
                    title="Изображение"
                    type="button"
                    class="btnOtst btn btn-sm btn-secondary"
                  >
                    <b>Im</b>
                  </button>
                </ul>
                <div class>
                  <textarea
                    v-model="text"
                    name="text"
                    cols="40"
                    rows="10"
                    class="textarea form-control"
                  ></textarea>
                </div>
              </div>
              <div>
                <p class="b">{{mess}}</p>
              </div>
              <button
                @click="updatePost"
                type="button"
                class="btn btn-outline-warning btn-block btn-dark"
              >Сохранить</button>
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
import { get, post, put } from "./../../Ajax/Http";

export default {
  name: "EditPost",
  created() {
    this.loadPost();
  },
  data() {
    return {
      title: "",
      text: "",
      mess: ""
    };
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    loadPost() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/posts/" +
        this.$route.params.Id +
        "/";
      get(url, response => {
        (this.title = response.title), (this.text = response.text);
      });
    },
    updatePost() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/posts/" +
        this.$route.params.Id +
        "/";
      put(
        url,
        response => {
          this.$router.push({ name: "my_posts" });
        },
        {
          pk: this.$route.params.Id,
          title: this.title,
          text: this.text,
          avtor: this.$store.getters.get_user_info.user
        },
        response => {
          if (response.status === 400) {
            this.mess = "Пожалуйста, заполните все поля!";
          }
        }
      );
    },
    addTagB() {
      this.text += "<b> </b>";
    },
    addTagH() {
      this.text += "<h3> </h3>";
    },
    addTagI() {
      this.text += "<i> </i>";
    },
    addTagU() {
      this.text += "<u> </u>";
    },
    addTagS() {
      this.text += "<s> </s>";
    },
    addTagImg() {
      this.text += '<img src= " http:// " class="img-thumbnail"/>';
    },
    addTagA() {
      this.text += '<a href="http:// "></a>';
    },
    addTagO() {
      this.text += "<ol>\n    <li> </li> \n</ol>";
    }
  }
};
</script>


<style>
.b {
  color: #ff0000;
}
.ul {
  padding: 1px;
}
.btnOtst {
  width: 30px;
  margin-left: 5px;
}
</style>
