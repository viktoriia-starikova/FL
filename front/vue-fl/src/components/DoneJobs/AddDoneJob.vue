<template>
  <div>
    <FlashMessage></FlashMessage>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Добавить работу</h2>
            <form method="post">
              <div class="form-group">
                <label for="id_text" class="col-form-label requiredField">
                  <b>Комментарий</b>
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
                    v-model="text"
                    name="text"
                    cols="40"
                    rows="10"
                    class="textarea form-control"
                  ></textarea>
                </div>
              </div>
              <div v-show="files.length<1" class="not-selected-input">
                <b>Файлы</b>
                <b style="color: red;">*</b>
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

              <div v-show="files.length" class="selected-input">
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
                <b v-show="files.length">Вы выбрали:</b>
                <span v-for="file in files">{{file.name}}</span>
              </div>
              <div>
                <p class="b">{{mess}}</p>
              </div>
              <button
                @click="addDoneJob"
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
import { get, post } from "./../../Ajax/Http";

export default {
  data() {
    return {
      file: "",
      title: "",
      categories: [],
      text: "",
      deadline: "2020-01-16 00:54:00",
      price: 5,
      mess: "",
      files: []
    };
  },
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    },

    addDoneJob() {
      const url = this.$store.getters.get_url_server + "api/v1/my/doneJobs/";
      post(
        url,
        response => {
          this.addFiles(response);
        },
        {
          message: this.text,
          task: this.$route.params.taskId
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
    },
    inputChange() {
      var files = $("#file");
      var filesList = files.prop("files");
      this.files = filesList;
    },
    addFiles(id) {
      var files = $("#file");
      // если файл выбран, то
      var filesList = files.prop("files");
      for (let file of filesList) {
        var formData = new FormData();
        // добавляем в объект FormData файл
        formData.append("file", file);
        formData.append("doneJob", id);
        $.ajax({
          url: this.$store.getters.get_url_server + "api/v1/file/",
          data: formData,
          processData: false,
          contentType: false,
          type: "POST",
          success: response => {
            console.log("Файл загружен");
            this.$router.push({ name: "myJob" });
          },
          error: response => {
            console.log("Файл не загружен");
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, попробуйте в другой раз!"
            });
          }
        });
      }
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
