<template>
  <div class="home">
    <Tasks :tasks="tasks" :mess="mess" @reload="loadTasks"></Tasks>
  </div>
</template>

<script>
import Tasks from "@/components/Tasks/Tasks.vue";
import { get } from "./../Ajax/Http";

export default {
  name: "my_tasks",
  props: {
    mess: ""
  },
  components: {
    Tasks
  },
  data() {
    return {
      tasks: []
    };
  },
  created() {
    this.loadTasks();
  },
  methods: {
    loadTasks() {
      const url = this.$store.getters.get_url_server + "api/v1/my/tasks/";
      get(url, response => {
        this.tasks = response;
        console.log("Все задания успешно загружены");
      });
    }
  }
};
</script>
