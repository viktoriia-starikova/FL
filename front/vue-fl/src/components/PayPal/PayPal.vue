
<template>
  <main class="container">
    <div class="row">
      <div class="col-md-8">
        <div class="alert alert-light">
          <div>
            <h1>Пополнить баланс</h1>
            <p class="mt-2"><b>Сумма пополнения, $</b></p>
            <input v-model="cost" class="form-control mb-4" type="number" id="example-number-input">
          </div>
          <hr>
          <div ref="paypal"></div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  name: "PayPal",

  data: function() {
    return {
      loaded: false,
      cost: 0
    };
  },
  mounted: function() {
    const script = document.createElement("script");
    script.src = "https://www.paypal.com/sdk/js?client-id=AZlasdOHARc22ZTCbENp-39E4ViRI4v2R8lAGui4qGneX0lG9NTJo4vwyDXwoQmyR4-nUaAUZ9pkFTKu";
    script.addEventListener("load", this.setLoaded);
    document.body.appendChild(script);
  },
  methods: {
    setLoaded: function() {
      this.loaded = true;
      window.paypal
        .Buttons({
          createOrder: (data, actions) => {
            return actions.order.create({
              purchase_units: [
                {
                  description: "Пополнение счета FL",
                  amount: {
                    currency_code: "USD",
                    value: this.cost
                  }
                }
              ]
            });
          },
          onApprove: async (data, actions) => {
            const order = await actions.order.capture();
            
            console.log(order);
          },
          onError: err => {
            console.log(err);
          }
        })
        .render(this.$refs.paypal);
    }
  }
};
</script>