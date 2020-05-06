<template>
  <div id="app">
    <Menu>
    </Menu>
    <router-view/>
  </div>
</template>

<script>
  import Menu from '@/components/Menu.vue'
  export default {
    name: 'app',
    components: {
      Menu
    },
    created(){
      const token = sessionStorage.getItem("token");
      if (token){
        this.$store.commit("set_auth", true)
        $.ajaxSetup({
            headers: {'Authorization': "Token " + token},
        });
        this.$store.dispatch("user_info")
      }
      else {
        this.$store.commit("set_auth", false)
      }
    },
  }
</script>


<style lang="scss">
.asteriskField{
  color: red;
}
.btn:active {
  box-shadow: 0 5px #666;
  transform: translateY(4px);
}
  body{
    background: #fafafa
  }
  .alert-light {
    border-color: #bfbfbf
  }
  .user_image {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    margin-right: 5px;
    margin-left: 14px
  }
  .material-icons{
        color: orange;
        position: inherit;
        padding: 3px;
        top: 5px;
        cursor: pointer;
  }
  .form-section {
      background: #fafafa;
      padding: 20px;
      border: 1px solid #bfbfbf;
      box-sizing: border-box;
      width: 100%;
      -webkit-box-shadow: 0 2px 3px 0 rgb(74,74,74,.21);
      -moz-box-shadow: 0 2px 3px 0 rgb(74,74,74,.21);
      box-shadow: 0 2px 3px 0 rgb(74,74,74,.21);
  }

  .form-section > h2 {
    color: #b38a22;
    margin-bottom: 10px;
  }
</style>
