<template>
  <div>
    <FlashMessage></FlashMessage>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="shadow form-section">
            <h2>Редактировать задание</h2>
            <form method="post">
              <div id="div_id_title" class="form-group">
                <label for="id_title" class="col-form-label requiredField">
                  <b>Заголовок</b>
                  <b style="color: red;">*</b>
                </label>
                <div class>
                  <input
                    v-model="title"
                    type="text"
                    name="title"
                    maxlength="50"
                    required="required"
                    class="textinput textInput form-control"
                  />
                  <p id="p">{{mess1}}</p>
                </div>
              </div>
              <div class="form-group">
                <label for="id_text" class="col-form-label requiredField">
                  <b>Описание</b>
                  <b style="color: red;">*</b>
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
                    v-model="description"
                    name="text"
                    cols="40"
                    rows="10"
                    class="textarea form-control"
                    required="required"
                  ></textarea>
                </div>
                <p id="p">{{mess2}}</p>
              </div>
              <p>
                <b>Бюджет</b>
                <b style="color: red;">*</b>
                <b>, $</b>
              </p>
              <number-input size="small" v-model="price" :min="1" inline center controls></number-input>
              <p>
                <b>Дата сдачи</b>
                <b style="color: red;">*</b>
              </p>
              <p>
                <Datepicker class="app" v-model="deadline" format="YYYY-MM-DD H:i:s" width="150px" />
              </p>
              <b>Категория</b>
              <b style="color: red;">*</b>
              <select v-model="selectedCategory" class="custom-select mt-3">
                <option
                  :selected="selectedCategory"
                  v-for="category in categories"
                >{{category.name}}</option>
              </select>
              <div v-show="files.length<1" class="not-selected-input mt-3">
                <b>Файлы</b>
                <div class="form-group">
                  <input
                    @change="inputChange()"
                    type="file"
                    name="file"
                    id="file"
                    class="input-file"
                    multiple="true"
                  />
                  <label for="file" class="btn btn-tertiary js-labelFile">
                    <i class="icon fa fa-check"></i>
                    <span class="js-fileName">Загрузить файл</span>
                  </label>
                </div>
              </div>

              <div v-show="files.length" class="selected-input mt-3">
                <b>Файлы</b>
                <div class="form-group">
                  <input
                    @change="inputChange()"
                    type="file"
                    name="file"
                    id="file"
                    class="input-file"
                    multiple="true"
                  />
                  <label for="file" class="btn btn-tertiary js-labelFile">
                    <i class="icon fa fa-check"></i>
                    <span class="js-fileName">Загрузить файл</span>
                  </label>
                </div>
                <b v-show="files.length">На данный момент:</b>
                <span v-for="file in files">{{file.name || file.file}}</span>
              </div>
              <button
                @click="updateTask"
                type="button"
                class="button btn btn-outline-warning btn-block btn-dark"
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
import Datepicker from "vuejs-datetimepicker";
import { get, postFiles, post, del } from "./../../Ajax/Http";

export default {
  data() {
    return {
      file: "",
      title: sessionStorage.getItem("title"),
      categories: [],
      description: "",
      deadline: "2020-01-16 00:54:00",
      price: 5,
      selectedCategory: "",
      selectedCategoryObject: "",
      files: [],
      mess1: "",
      mess2: ""
    };
  },
  created() {
    this.loadCategories();
    this.loadTask();
    this.loadFiles();
  },
  components: { Datepicker },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },
    goTaskDetail() {
      this.$router.push({
        name: "task_detail",
        params: { taskId: this.$route.params.Id }
      });
    },
    loadCategories() {
      const url = this.$store.getters.get_url_server + "api/v1/categories/";
      get(url, response => {
        this.categories = response;
      });
    },
    loadTask() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/task/" +
        this.$route.params.Id +
        "/";
      get(url, response => {
        this.task = response;
        this.title = this.task.title;
        this.description = this.task.description;
        this.price = this.task.price;
        this.deadline = this.task.deadline;
        this.selectedCategory = this.task.category.name;
      });
    },
    loadFiles() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/allFilesByTask/" +
        this.$route.params.Id +
        "/";
      get(url, response => {
        this.files = response;
      });
    },
    updateFiles() {
      var files = $("#file");
      const url = this.$store.getters.get_url_server + "api/v1/file/";
      var filesList = files.prop("files");
      if (filesList.length < 1) {
        this.goTaskDetail();
      }
      for (let file of filesList) {
        var formData = new FormData();
        formData.append("file", file);
        formData.append("task", this.$route.params.Id);
        postFiles(
          url,
          response => {
            this.goTaskDetail();
          },
          formData,
          response => {
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, попробуйте в другой раз!"
            });
          }
        );
      }
    },
    DeleteFiles() {
      const files = $("#file");
      // если файл выбран, то
      const filesList = files.prop("files");
      if (filesList.length < 1) {
        this.goTaskDetail();
      } else {
        const url =
          this.$store.getters.get_url_server +
          "api/v1/files/task/" +
          this.$route.params.Id +
          "/";
        del(url, response => {
          this.updateFiles();
        });
      }
    },
    updateTask() {
      const url =
        this.$store.getters.get_url_server +
        "api/v1/task/detail/" +
        this.$route.params.Id +
        "/";
      put(
        url,
        response => {
          this.DeleteFiles();
        },
        {
          title: this.title,
          description: this.description,
          price: this.price,
          deadline: this.deadline,
          category: this.selectedCategoryObject
        },
        response => {
          if (response.status === 400) {
            this.mess1 = response.responseJSON.title
              ? response.responseJSON.title[0]
              : "";
            this.mess2 = response.responseJSON.description
              ? response.responseJSON.description[0]
              : "";
            this.flashMessage.error({
              title: "Не удается обновить заказ",
              message: "Пожалуйста, попробуйте в другой раз!"
            });
          }
        }
      );
    },
    addTagB() {
      this.description += "<b> </b>";
    },
    addTagH() {
      this.description += "<h3> </h3>";
    },
    addTagI() {
      this.description += "<i> </i>";
    },
    addTagU() {
      this.description += "<u> </u>";
    },
    addTagS() {
      this.description += "<s> </s>";
    },
    addTagImg() {
      this.description += '<img src= " http:// " class="img-thumbnail"/>';
    },
    addTagA() {
      this.description += '<a href="http:// "></a>';
    },
    addTagO() {
      this.description += "<ol>\n    <li> </li> \n</ol>";
    },
    inputChange() {
      var files = $("#file");
      var filesList = files.prop("files");
      this.files = filesList;
    },
    addFiles(id) {
      const files = $("#file");
      const filesList = files.prop("files");
      for (let file of filesList) {
        var formData = new FormData();
        formData.append("file", file);
        formData.append("task", id);
        const url = this.$store.getters.get_url_server + "api/v1/file/";
        postFiles(
          url,
          response => {
            console.log("Файл загружен");
            window.location.reload();
          },
          formData,
          response => {
            console.log("Файл не загружен");
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, попробуйте в другой раз!"
            });
          }
        );
      }
    }
  },
  watch: {
    selectedCategory() {
      this.selectedCategoryObject = this.categories.find(
        c => c.name === this.selectedCategory
      ).id;
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
.not-selected-input .btn-tertiary {
  color: #555;
  padding: 0;
  line-height: 40px;
  width: 300px;
  margin: auto;
  display: block;
  border: 2px solid #555;
}
.not-selected-input .btn-tertiary:hover,
.not-selected-input .btn-tertiary:focus {
  color: #888;
  border-color: #888;
}
.not-selected-input .input-file {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}
.not-selected-input .input-file + .js-labelFile {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 10px;
  cursor: pointer;
}
.not-selected-input .input-file + .js-labelFile .icon:before {
  content: "\f093";
}
.not-selected-input .input-file + .js-labelFile.has-file .icon:before {
  content: "\f00c";
  color: #5aac7b;
}

.selected-input .btn-tertiary {
  color: #ffc107;
  padding: 0;
  line-height: 40px;
  width: 300px;
  margin: auto;
  display: block;
  border: 2px solid #ffc107;
}
.selected-input .btn-tertiary:hover,
.not-selected-input .btn-tertiary:focus {
  color: #f8d56b;
  border-color: #f8d56b;
}
.selected-input .input-file {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}
.selected-input .input-file + .js-labelFile {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  padding: 0 10px;
  cursor: pointer;
}
.selected-input .input-file + .js-labelFile .icon:before {
  content: "\f093";
}
.selected-input .input-file + .js-labelFile.has-file .icon:before {
  content: "\f00c";
  color: #5aac7b;
}
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
