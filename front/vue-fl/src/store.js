import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    url_server: "http://127.0.0.1:8000/",
    url_media: "http://127.0.0.1:8000",
    auth_user: false,
    user: '',

  },
  getters: {
      get_url_server(state) {
          return state.url_server
      },
      get_auth(state) {
          return state.auth_user
      },
      get_user_info(state) {
          return state.user
      },
      get_url_media(state) {
          return state.url_media
      },
      get_user_avtoriz(state) {
          return state.auth_user
      },
    },
  mutations: {
      set_auth(state, value) {
          state.auth_user = value
      },
      set_user_info(state, value) {
          state.user = value
      },
      set_user_info(state, value) {
          state.user = value
      },
  },
  actions: {
    user_info(context) {
                $.ajax({
                    async: false,
                    url: context.getters.get_url_server + "api/v2/",
                    type: "GET",
                    success: (response) => {
                        context.commit('set_user_info', response)
                    },
                    error: (response) => {
                        if (response.status === 400) {
                          console.log('Данные пользователя не загружены')
                        }
                    }
                });
            },
  }
})
