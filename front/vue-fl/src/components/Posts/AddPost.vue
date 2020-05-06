<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Добавить статью</h2>
            <form method="post">
              <div id="div_id_title" class="form-group">
                <label for="id_title" class="col-form-label requiredField">
                  Заголовок
                  <span class="asteriskField">*</span>
                </label>
                <div>
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

                <div>
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
                @click="addPost"
                type="button"
                class="btn btn-outline-warning btn-block btn-dark"
              >Сохранить</button>
            </form>
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
  </div>
</template>


<script>
import { get, post } from "./../../Ajax/Http";

export default {
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
    addPost() {
      const url = this.$store.getters.get_url_server + "api/v1/my/";
      post(
        url,
        response => {
          this.$router.push({ name: "my_posts" });
        },
        {
          title: this.title,
          text: this.text
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
.ic {
  position: inherit;
  margin-right: 5px;
}
</style>
