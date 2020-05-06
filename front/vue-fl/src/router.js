import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import Login from './components/Profile/Login.vue'
import Exit from './components/Profile/Exit.vue'
import Balance from './components/Profile/Balance.vue'
import MyPosts from './views/My_posts.vue'
import MyTask from './components/Tasks/MyTask.vue'
import Profile from './views/Profile.vue'
import PostDetail from './components/Posts/PostDetail.vue'
import DeletePost from './components/Posts/DeletePost.vue'
import AddPost from './components/Posts/AddPost.vue'
import EditPost from './components/Posts/EditPost.vue'
import Registr from './components/Profile/Registr.vue'
import PublicProfile from './components/Profile/PublicProfile.vue'
import About from './components/About.vue'
import MyJob from './components/DoneJobs/MyJob.vue'
import Tasks from './components/Tasks/Tasks.vue'
import AddTask from './components/Tasks/AddTask.vue'
import Dialog from './components/Chat/Dialog.vue'
import TaskDetail from './components/Tasks/TaskDetail.vue'
import EditTask from './components/Tasks/EditTask.vue'
import MyActiveTasks from './components/Tasks/MyActiveTasks.vue'
import AddDoneJob from './components/DoneJobs/AddDoneJob.vue'
import AddPortfolio from './components/Portfolio/AddPortfolio.vue'
import EditPortfolio from './components/Portfolio/EditPortfolio.vue'
import Arbitration from './components/Arbitration/Arbitration.vue'
import Review from './components/ModalWindows/Review.vue'
import PortfolioWorkDetail from './components/Portfolio/PortfolioWorkDetail.vue'
import PayPal from './components/PayPal/PayPal.vue'
import ICustomer from './components/Tasks/ICustomer.vue'
import FL from './components/FL.vue'
import store from './store'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/dialog/:id/',
      name: 'dialog',
      component: Dialog
    },
    {
      path: '/portfolioWorkDetail/:id/',
      name: 'portfolioWorkDetail',
      component: PortfolioWorkDetail
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/myJob',
      name: 'myJob',
      component: MyJob
    },
    {
      path: '/tasks',
      name: 'tasks',
      component: Tasks
    },
    {
      path: '/review',
      name: 'review',
      component: Review
    },
    {
      path: '/addTask',
      name: 'addTask',
      component: AddTask
    },
    {
      path: '/customer',
      name: 'customer',
      component: ICustomer
    },
    {
      path: '/payPal',
      name: 'payPal',
      component: PayPal
    },
    {
      path: '/publicProfile/:Id/',
      name: 'publicProfile',
      component: PublicProfile
    },
    {
      path: '/exit',
      name: 'exit',
      component: Exit
    },
    {
      path: '/arbitration',
      name: 'arbitration',
      component: Arbitration
    },
    {
      path: '/balance',
      name: 'balance',
      component: Balance
    },
    {
      path: '/add',
      name: 'addPost',
      component: AddPost,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'home'})
        }
      }
    },
    {
      path: '/addPortfolio',
      name: 'addPortfolio',
      component: AddPortfolio,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'home'})
        }
      }
    },
    {
      path: '/my',
      name: 'my_posts',
      component: MyPosts,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'home'})
      }
    }
    },
    {
      path: '/myActiveTasks',
      name: 'myActiveTasks',
      component: MyActiveTasks,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'home'})
      }
    }
    },
    {
      path: '/my/tasks',
      name: 'my_tasks',
      component: MyTask,

    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: '/fl',
      name: 'fl',
      component: FL,
    },
    {
      path: '/post/:postId/',
      name: 'post_detail',
      component: PostDetail
    },
    {
      path: '/task/:taskId/',
      name: 'task_detail',
      component: TaskDetail
    },
    {
      path: '/addJob/:taskId/',
      name: 'addJob',
      component: AddDoneJob
    },
    {
      path: '/editPortfolio/:Id/',
      name: 'editPortfolio',
      component: EditPortfolio,
    },
    {
      path: '/editTask/:Id/',
      name: 'editTask',
      component: EditTask,
    },
    {
      path: '/delete/:Id/',
      name: 'delete_post',
      component: DeletePost,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'fl'})
        }
      }
    },
    {
      path: '/edit/:Id/',
      name: 'edit_post',
      component: EditPost,
      beforeEnter: (to,from, next) => {
        if (store.getters.get_auth){
          next()
        }
        else {
          next({name: 'fl'})
        }
      }
    },
    {
      path: '/reg/',
      name: 'reg',
      component: Registr,
    },
  ]
})
