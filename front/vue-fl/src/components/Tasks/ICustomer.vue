<template>
  <div>
    <main class="container">
      <div class="shadow rounded alert alert-light">
        <div class="row">
          <div class="col-md-8">
            <div class="col-10" style="padding: 0px">
              <h3 class="h3">
                <b>Я заказчик</b>
              </h3>
              <span>
                <a @click="goPage('fl')" href="#">Биржа фриланса</a>
                <a @click="loadProf($store.getters.get_user_info.user.id)" href="#">/ Аккаунт</a>
                <span class="text-muted">/ Я заказчик</span>
              </span>
            </div>
          </div>
          <div class="col-md-4 mt-1 pr-1">
            <button
              @click="goPage('addTask')"
              data-turbolinks="false"
              type="button"
              class="shadow btn btn-warning btn-lg btn-block"
            >Разместить заказ</button>
          </div>
        </div>
      </div>
      <div class="row">
        <div v-if="tasks && tasks.length>0" class="col-md-8">
          <div class="alert alert-light shadow" v-for="task in displayedTasks">
            <h3>{{task.title }}</h3>
            <p>{{task.description| truncate(320, '...')}}</p>
            <div class="row">
              <div class="col-10" style="padding: 0px">
                <div class="mt-2">
                  <p>
                    <a
                      class="category"
                      @click="loadTasksByCategory(task.category)"
                      href="#"
                    >{{task.category.name}}</a>
                  </p>
                  <span class="text-muted">
                    <b class="user_image">Дата:</b>
                    {{task.createdDate| filterDateTime}}
                  </span>
                  <p>
                    <b class="user_image">Автор:</b>
                    <a @click="loadProf(task.author.id)" href="#">{{task.author.username}}</a>
                  </p>
                </div>
              </div>
              <div v-if="task.price!=0" class="col-2" style="padding: 0px">
                <p class="price">
                  <b>${{task.price}}</b>
                </p>
              </div>
            </div>
            <a href @click="loadTask(task.id)" class="btn btn-outline-warning">Читать далее</a>
          </div>
          <div id="pag" class="clearfix btn-group">
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
        <div v-if="tasks.length<1" class="col-md-8">
          <div class="shadow-lg alert alert-light">
            <h2>Как найти исполнителя?</h2>
            <p>Найти исполнителя для Вашего заказа можно выполнив несколько простых шагов:</p>
            <b>&bull; Добавьте проект</b>
            <p>Размещение заказа займет всего несколько минут.</p>
            <p>Ключевые поля формы публикации заказа:</p>
            <b>- Название и описание</b>
            <p>
              Название должно кратко отражать суть заказа, а описание содержать максимальный объем информации о нем.
              При отсутствии прилагаемого файла с текстом задания только описание позволит исполнителям оценить объем работ и стоимость услуг.
            </p>
            <b>- Бюджет</b>
            <p>Бюджет заказа информирует исполнителей о сумме вознаграждения за успешное выполнение задания.</p>
            <b>- Категория</b>
            <p>
              Категория является одним из наиболее важных элементов информации о заказе.
              Правильный выбор категории позволит привлечь максимальное число исполнителей, специализирующихся в данной области.
            </p>
            <b>&bull; Принимайте предложения от фрилансеров</b>
            <p>
              Фрилансеры, желающие выполнить Ваш заказ, будут размещать заявки непосредственно на странице заказа.
              Изучайте предложения фрилансеров, свободно общайтесь с ними с помощью приватных сообщений или других средств связи.
              <br />Обращайте внимание на портфолио фрилансеров и отзывы, оставленные другими заказчиками.
              Немаловажными характеристиками также являются рейтинг фрилансеров и продолжительность их работы в сервисе.
            </p>
            <b>&bull; Укажите выбранного исполнителя</b>
            <p>
              Перед началом сотрудничества обязательно укажите выбранного исполнителя на странице заказа!
              Только указав выбранного исполнителя Вы сможете в дальнейшем опубликовать отзыв в его адрес.
            </p>
            <b>&bull; Оставьте отзыв о сотрудничестве</b>
            <p>
              По окончании сотрудничества оставьте отзыв об исполнителе на странице заказа.
              <br />Положительный — оценка выше трех звезд считается положительной, только после полного выполнения исполнителем всех обязательств перед Вами.
              <br />Отрицательный — оценка три звезды и ниже считается отрицательной, только в случае, если принятые обязательства не были выполнены.
              <br />Кратко опишите процесс сотрудничества и оцените профессиональные качества исполнителя.
            </p>
          </div>
        </div>
        <aside class="col-md-4">
          <div id="multi-derevo" class="p-3 rounded nb-3 alert alert-light shadow">
            <h3 style="cursor: pointer">
              <b @click="clearTasks()">Я заказчик</b>
            </h3>
            <p>
              <a class="a" href="#" @click="loadTasks()">Список заказов</a>
            </p>
            <p>
              <a class="a" href="#" @click="loadProf($store.getters.get_user_info.user.id)">Аккаунт</a>
            </p>
            <p>
              <a class="a" href="#" @click="goPage('balance')">Баланс</a>
            </p>
          </div>
        </aside>
      </div>
    </main>
  </div>
</template>

<script>
import { get, post } from "./../../Ajax/Http";

export default {
  created() {},
  data() {
    return {
      tasks: [],
      perPage: 5,
      pages: [],
      page: 1
    };
  },
  computed: {
    displayedTasks() {
      return this.paginate(this.tasks);
    }
  },
  methods: {
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
    clearTasks() {
      this.tasks = [];
    },
    loadTasksByCategory(category) {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/myTasksByCategory/" +
        category.id +
        "/";
      get(url, response => {
        if (response) {
          this.tasks = response;

          this.checkedCategory = category;
        }
      });
    },
    loadTask(id) {
      this.$router.push({ name: "task_detail", params: { taskId: id } });
    },
    loadTasks() {
      const url = this.$store.getters.get_url_server + "api/v1/my/tasks/";
      get(url, response => {
        this.tasks = response;
      });
    },
    paginate(tasks) {
      let page = this.page;
      let perPage = this.perPage;
      let from = page * perPage - perPage;
      let to = page * perPage;
      return tasks.slice(from, to);
    },
    setPages() {
      let numberOfPages = Math.ceil(this.tasks.length / this.perPage);
      this.pages = [];
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    }
  },
  watch: {
    tasks() {
      this.setPages();
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