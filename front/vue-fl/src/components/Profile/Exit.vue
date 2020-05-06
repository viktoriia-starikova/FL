<template>
  <main class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="form-section">
          <h2>Вы вышли из аккаунта!</h2>
          <a href @click="goPage('login')">Войти в личный кабинет</a>
        </div>
      </div>
    </div>
  </main>
</template>


<script>
export default {
  methods: {
    goPage(item) {
      this.$router.push({ name: item });
    }
  }
};
</script>


<style>
</style>
