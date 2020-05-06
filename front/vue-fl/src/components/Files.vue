<template>
  <div v-if="files.length>0" class="row filesDiv">
    <div v-for="file in files" class="col justify-content-start">
      <img v-if="docFile(file.file)" class="file" :src="$store.getters.get_url_media + '/Media/txt.png'"/>
      <img
        v-if="getExtencion(file.file) == 'png' || 
        getExtencion(file.file) == 'jpg' || 
        getExtencion(file.file) == 'svg' || 
        getExtencion(file.file) == 'gif'"
        class="file"
        :src="$store.getters.get_url_media + file.file"
      />
      <img v-if="rarFile(file.file)" class="file" :src="$store.getters.get_url_media + '/Media/rar.png'" />
      <img v-if="anotherFile(file.file)" class="file" :src="$store.getters.get_url_media + '/Media/wtf.png'"/>
      <p>
        <a
          style="color: gray;"
          :href="$store.getters.get_url_media + file.file"
        >{{getFileName(file.file)}}</a>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Files",
  props: {
    files: ""
  },
  methods: {
    getFileName(filename) {
      const fullName = filename.split("/").pop();
      if (fullName.length > 15) return ".." + fullName.substr(9);
      return fullName;
    },
    getExtencion(filename) {
      return filename.split(".").pop();
    },
    anotherFile(filename) {
      const extencion = this.getExtencion(filename);
      return (
        extencion != "rar" &&
        extencion != "7zip" &&
        extencion != "png" &&
        extencion != "jpg" &&
        extencion != "svg" &&
        extencion != "gif" &&
        extencion != "txt" &&
        extencion != "doc" &&
        extencion != "docx"
      );
    },
    rarFile(filename) {
      const extencion = this.getExtencion(filename);
      return extencion == "rar" || extencion == "7zip";
    },
    docFile(filename) {
      const extencion = this.getExtencion(filename);
      return extencion == "txt" || extencion == "doc" || extencion == "docx";
    }
  }
};
</script>
<style>
.filesDiv {
  border-top: 2px solid #f0f0f0;
  padding: 10px;
  border-bottom: 1px solid #f0f0f0;
  text-align: center;
  color: gray;
}
</style>