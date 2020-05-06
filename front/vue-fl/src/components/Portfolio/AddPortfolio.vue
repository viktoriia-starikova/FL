<template>
  <div>
    <FlashMessage></FlashMessage>
    <main class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="form-section">
            <h2>Добавить работу в портфолио</h2>
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
                    class="textinput textInput form-control"
                  />
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
                    v-model="text"
                    name="text"
                    cols="40"
                    rows="10"
                    class="textarea form-control"
                  ></textarea>
                </div>
              </div>
              <div v-if="img" class="selected-input">
                <b>Обложка</b>
                <div>
                  <input @change="imgChange()" type="file" id="img" class="input-file" />
                  <label for="img" class="btn btn-tertiary js-labelFile">
                    <i class="icon fa fa-check"></i>
                    <span class="js-fileName">Загрузить обложку</span>
                  </label>
                </div>
                <b>Вы выбрали:</b>
                <span v-for="file in img">{{file.name}}</span>
              </div>

              <div v-if="!img" class="not-selected-input">
                <b>Обложка</b>
                <div>
                  <input @change="imgChange()" type="file" id="img" class="input-file" />
                  <label for="img" class="btn btn-tertiary js-labelFile">
                    <i class="icon fa fa-check"></i>
                    <span class="js-fileName">Загрузить обложку</span>
                  </label>
                </div>
              </div>

              <div v-show="files.length<1" class="not-selected-input">
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

              <div v-show="files.length>0" class="selected-input">
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
      </div>
    </main>
  </div>
</template>



<script>
import { get, postFiles } from "./../../Ajax/Http";

export default {
  data() {
    return {
      file: "",
      image: "",
      img: "",
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
      var formData = new FormData();
      formData.append("img", this.img[0]);
      formData.append("title", this.title);
      formData.append("text", this.text);

      const url = this.$store.getters.get_url_server + "api/v1/addPortfolio/";
      postFiles(
        url,
        response => {
          this.addFiles(response);
          this.$router.push({ name: "profile" });
        },
        formData,
        error => {
          if (response.status === 400) {
            this.mess = response.statusText;
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
    },
    imgChange() {
      var files = $("#img");
      var filesList = files.prop("files");
      this.img = filesList;
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
        formData.append("portfolioWork", id);
        
        const url = this.$store.getters.get_url_server + "api/v1/file/";
        postFiles(
          url,
          response => {
            console.log("Файл загружен");
          },
          formData,
          response => {
            console.log("Файл не загружен");
            this.mess = response.statusText;
            this.flashMessage.error({
              title: "Ошибка",
              message: "Пожалуйста, попробуйте в другой раз!"
            });
          }
        );
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
