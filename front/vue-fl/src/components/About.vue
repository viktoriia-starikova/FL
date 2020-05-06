<template>
  <main class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="form-section">
          <a style="display: inline-block; color: orange" href="https://vk.com">
            <h3 style="display: inline-block;">Мы ВКонтакте </h3>
            <img style=" margin-left : 10px; display: inline-block; width: 35px; height: 35px;" src="https://primepress.co.uk/wp-content/uploads/2018/10/bootstrap-1.png"></img>
          </a>
          <div>
            <a style="display: inline-block; color: orange" href="https://www.instagram.com">
              <h3 style="display: inline-block;">Мы в Instagram</h3>
              <img style="display: inline-block; width: 45px; height: 45px;" src="https://cdn-images-1.medium.com/max/1200/1*CPgwLHR6jno_tOmF0--7eg.jpeg"></img>
            </a>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>


<script>
export default {
  methods: {
      goPage(item) {
          this.$router.push({name: item})
      },
    }
}
</script>


<style>

</style>
