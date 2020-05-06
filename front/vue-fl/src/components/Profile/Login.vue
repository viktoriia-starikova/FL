<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Вход в аккаунт</h2>
            <form>
              <div class="form-group">
                <label for="disabledTextInput">Логин</label>
                <input
                  v-model="user.username"
                  type="text"
                  class="form-control"
                  placeholder="Введите логин"
                />
              </div>
              <div class="form-group">
                <label for="inputPassword5">Пароль</label>
                <input
                  v-model="user.password"
                  placeholder="Введите пароль"
                  type="password"
                  id="inputPassword5"
                  class="form-control"
                  aria-describedby="passwordHelpBlock"
                />
                <small
                  id="passwordHelpBlock"
                  class="form-text text-muted"
                >Ваш пароль должен быть длинной 8-11 символов.</small>
              </div>
              <div>
                <p class="b">{{mess}}</p>
              </div>
              <button
                type="button"
                class="btn btn-outline-warning btn-block btn-dark"
                @click="setLogin"
              >Войти</button>
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
              <b>Дефекты лайков</b>
            </h3>
            <div class="p-3 mb-3">
              <img
                src="https://habrastorage.org/getpro/habr/post_images/548/aa0/c55/548aa0c5510183d965d2b6417464fac6.jpg"
                class="img-thumbnail"
              />
            </div>
            <p>
              Вместо эпиграфа.
              Больше всего лайков собирают «котики». Можно ли это считать признаком эпидемии токсоплазмоза?
            </p>
            <a href="https://habr.com/ru/post/442714/" title="Посмотреть на habr" target="_blank">
              <button class="btn btn-warning">Посмотреть</button>
            </a>
          </div>
        </aside>
      </div>
    </main>
    <FlashMessage></FlashMessage>
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
import { post } from "./../../Ajax/Http";

export default {
  name: "Login",
  data() {
    return {
      user: {
        username: "",
        password: ""
      },
      mess: ""
    };
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    setLogin() {
      const url = this.$store.getters.get_url_server + "auth/token/login/";
      post(
        url,
        response => {
          sessionStorage.setItem("token", response.auth_token);
          this.$store.commit("set_auth", true);
          $.ajaxSetup({
            headers: {
              Authorization: "Token " + sessionStorage.getItem("token")
            }
          });
          window.location = "/";
        },
        {
          username: this.user.username,
          password: this.user.password
        },
        response => {
          if (response.status === 400) {
            this.mess = response.responseJSON.non_field_errors[0];
          }
        }
      );
    }
  }
};
</script>

<style>
.b {
  color: #ff0000;
}
</style>
