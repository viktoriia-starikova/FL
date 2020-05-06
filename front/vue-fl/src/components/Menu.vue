<template>
  <div>
    <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark mb-2" style="color: gray">
      <a @click="goPage('fl')" class="navbar-brand" href="#">
          <img :src="$store.getters.get_url_media + '/Media/favicon.png'" width="40" height="40" class="d-inline-block align-top" alt="">
          <b>
            <big> FL</big>
          </b>
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#navbarsExample09"
        aria-controls="navbarsExample09"
        aria-expanded="false"
        aria-label="Переключение навигации"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarsExample09">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#" @click="goPage('home')">
              <big>Блог</big>
            </a>
          </li>
          <li class="nav-item active">
            <a v-if="auth" class="nav-link" href="#" @click="goPage('my_posts')">
              <big>Мои посты</big>
            </a>
          </li>
          <li class="nav-item active">
            <div v-if="auth" class="dropdown">
              <a
                v-if="auth"
                class="dropdown-toggle nav-link text-white"
                id="menu"
                data-toggle="dropdown"
              >
                <big>Заказчик</big>
              </a>
              <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                <a @click="goPage('addTask')" href class="dropdown-item">Создать заказ</a>
                <a @click="goPage('my_tasks')" href class="dropdown-item">Мои заказы</a>
              </div>
            </div>
          </li>
          <li class="nav-item active">
            <div v-if="auth" class="dropdown">
              <a
                v-if="auth"
                class="dropdown-toggle nav-link text-white"
                id="menu"
                data-toggle="dropdown"
              >
                <big>Фрилансер</big>
              </a>
              <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
                <a @click="goPage('tasks')" href class="dropdown-item">Заказы</a>
                <a @click="goPage('myJob')" href class="dropdown-item">Мои работы</a>
              </div>
            </div>
          </li>
          <li v-if="admin" class="nav-item active">
            <a class="nav-link" href="#" @click="goPage('arbitration')">
              <big>Арбитраж</big>
            </a>
          </li>
          <li class="nav-item active">
            <a class="nav-link" @click="goPage('about')" href>
              <big>Про нас</big>
            </a>
          </li>
        </ul>
      </div>
      <div class="navbar-nav">
        <div v-if="auth" class="dropdown">
          <a
            v-if="auth"
            class="btn-secondary text-white dropdown-toggle"
            style="background-color:transparent"
            id="menu"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <b>{{$store.getters.get_user_info.user.username}} </b>
            <img
              class="avatar"
              :src="$store.getters.get_url_media + $store.getters.get_user_info.img"
            />
          </a>
          <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">
            <a @click="goPage('profile')" href="#" class="dropdown-item">Профиль</a>
            <a @click="goPage('myActiveTasks')" href="#" class="dropdown-item">Я фрилансер</a>
            <a @click="goPage('customer')" href="#" class="dropdown-item">Я заказчик</a>
            <a @click="goPage('balance')" href="#" class="dropdown-item">Баланс</a>
            <a @click="goPage('addPost')" href="#" class="dropdown-item">Добавить статью</a>
            <div class="dropdown-divider"></div>
            <a @click="logout" href="#" class="dropdown-item">Выйти</a>
          </div>
        </div>
        <a
          v-if="!auth"
          href="#"
          @click="goPage('login')"
          class="btn btn-outline-secondary mr-2"
        >Войти</a>
        <a v-if="!auth" href="#" @click="goPage('reg')" class="btn btn-outline-warning">Регистрация</a>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "Menu",
  computed: {
    auth() {
      if (this.$store.getters.get_auth) return true;
      else return false;
    },
    admin() {
      if (this.$store.getters.get_auth && this.$store.getters.get_user_info.user.username == "Administrator")
        return true;
      else return false;
    }
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    logout() {
      this.$store.commit("set_auth", false);
      sessionStorage.removeItem("token");
      $.ajaxSetup({
        headers: { Authorization: "" }
      });
      window.location = "/exit";
    }
  }
};
</script>

<style lang="scss">
footer {
  padding: 15px;
  background: #333a41;
  color: #f1efef;
  float: left;
  width: 100%;
  margin-top: 50px;
}

footer a {
  color: #788c9e;
}

footer a:hover {
  color: #79b0e2;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50% 50%;
}

#menu {
  cursor: pointer;
}
</style>
