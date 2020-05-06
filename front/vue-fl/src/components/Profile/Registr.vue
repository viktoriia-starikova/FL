<template>
  <div>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Регистрация на сайте</h2>
            <form method="post">
              <div class="form-group">
                <label class="col-form-label requiredField">
                  Имя пользователя
                  <span class="asteriskField">*</span>
                </label>
                <div class>
                  <input
                    v-model="username"
                    type="text"
                    maxlength="150"
                    class="textinput textInput form-control"
                  />
                  <p id="p">{{mess1}}</p>
                  <small
                    class="form-text text-muted"
                  >Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.</small>
                </div>
              </div>
              <div class="form-group">
                <label class="col-form-label requiredField">
                  Пароль
                  <span class="asteriskField">*</span>
                </label>
                <div class>
                  <input v-model="password1" class="textinput textInput form-control" />
                  <p id="p">{{mess2}}</p>
                  <small class="form-text text-muted">
                    <ul>
                      <li>Ваш пароль не должен совпадать с вашим именем или другой персональной информацией или быть слишком похожим на неё.</li>
                      <li>Ваш пароль должен содержать как минимум 8 символов.</li>
                      <li>Ваш пароль не может быть одним из широко распространённых паролей.</li>
                      <li>Ваш пароль не может состоять только из цифр.</li>
                    </ul>
                  </small>
                </div>
              </div>
              <div class="form-group">
                <label class="col-form-label">Адрес электронной почты</label>
                <div class>
                  <input
                    v-model="email"
                    type="email"
                    maxlength="254"
                    class="emailinput form-control"
                  />
                </div>
              </div>

              <button
                @click="createProfile"
                type="button"
                class="btn btn-outline-warning btn-block btn-dark"
              >Зарегистрироваться</button>
            </form>
            <hr />Вы уже зарегистрированы?
            <a href @click="goPage('login')">Войти в личный кабинет.</a>
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
          <a href>о нас</a>.
        </p>
      </div>
    </footer>
  </div>
</template>


<script>
import { post } from "./../../Ajax/Http";

export default {
  data() {
    return {
      username: "",
      email: "",
      password1: "",
      mess1: "",
      mess2: ""
    };
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    createProfile() {
      const url = this.$store.getters.get_url_server + "api/v2/reg2/";
      post(
        url,
        response => {
          this.flashMessage.warning({
            title: "Информация",
            message: "Вы создали свой профиль!"
          });
          this.$router.push({ name: "login" });
        },
        {
          username: this.username,
          email: this.email,
          password: this.password1
        },
        response => {
          if (response.status === 400) {
            this.mess1 = response.responseJSON.username[0];
            this.mess2 = response.responseJSON.password[0];
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, заполните правильно все поля!"
            });
          }
        }
      );
    }
  }
};
</script>


<style lang="scss">
#p {
  color: #ff0000;
}
</style>
