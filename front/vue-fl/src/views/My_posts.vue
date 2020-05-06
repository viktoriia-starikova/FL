<template>
  <div class="home">
    <Posts :posts="posts" :mess="mess" @reload="loadPosts"></Posts>
  </div>
</template>

<script>
import Posts from "@/components/Posts/Posts.vue";
import { get } from "./../Ajax/Http";

export default {
  name: "home",
  props: {
    mess: ""
  },
  components: {
    Posts
  },
  data() {
    return {
      posts: ""
    };
  },
  created() {
    this.loadPosts();
  },
  methods: {
    loadPosts() {
      const url = this.$store.getters.get_url_server + "api/v1/my";
      get(url, response => {
        this.posts = response;
        console.log("Все посты успешно загружены");
      });
    }
  }
};
</script>
