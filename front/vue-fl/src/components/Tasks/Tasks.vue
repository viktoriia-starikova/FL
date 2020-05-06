<template>
 <div>
 <main class="container">
   <div class="shadow rounded alert alert-light">
     <div class="row">
       <div  class="col-md-8">
         <div class="col-10" style="padding: 0px">
             <h3 class="h3"><b>Удаленная работа для фрилансеров</b></h3>
             <span >
             <a @click="goPage('fl')" href="#">Биржа фриланса </a>

             <span class="text-muted" v-if="!checkedCategory" href="#">/ Удаленная работа </span>
             <a @click="loadTasks()" v-if="checkedCategory" href="#">/ Удаленная работа </a>
             <span  class="text-muted" v-if="checkedCategory">/ {{checkedCategory.name}} </span>
           </span>
         </div>
       </div>
       <div class="col-md-4 mt-1 pr-1" >
         <button @click="goPage('addTask')" data-turbolinks="false" type="button" class="shadow btn btn-warning btn-lg btn-block">Разместить заказ </button>
       </div>
     </div>
   </div>
   <div class="row">
     <div v-if="tasks && tasks.length<1" class="col-md-8">
       <h3>Нет заданий</h3>
     </div>
     <div v-if="tasks && tasks.length>0"  class="col-md-8">
         <div v-if="!task.approved" class="shadow alert alert-light" v-for="task in displayedTasks">
           <h3>{{task.title }}</h3>
           <p>{{task.description| truncate(320, '...')}}</p>
           <div class="row">
             <div class="col-10" style="padding: 0px">
               <div class="mt-2">
                 <p><a class="category" @click="loadTasksByCategory(task.category)" href="#">{{task.category.name}}</a></p>
                 <span class="text-muted" ><b class="user_image">Дата: </b>{{task.createdDate| filterDateTime}}</span>
                 <p><b class="user_image">Автор: </b><a @click="loadProf(task.author.id)" href="#">{{task.author.username}}</a></p>
               </div>
             </div>
             <div v-if="task.price!=0" class="col-2" style="padding: 0px">
                 <p class="price"><b>${{task.price}}</b></p>
             </div>
           </div>

           <a href="" @click="loadTask(task.id)" class="btn btn-outline-warning">Читать далее</a>
         </div>
         <div v-if="tasks.length>0" id="pag" class="clearfix btn-group">
              <button type="button" class="btn btn-warning" v-if="page != 1" @click="page--"> Предыдущая </button>
              <button type="button" class="btn btn-outline-warning" v-for="pageNumber in pages.slice(page-1, page+5)" @click="page = pageNumber"> {{pageNumber}} </button>
              <button type="button" @click="page++" v-if="page < pages.length" class="btn btn-warning"> Следующая </button>
         </div>
   </div>
   <aside class="col-md-4 ">
      <div id="multi-derevo" class='p-3 rounded nb-3 alert alert-light shadow' >
        <h3 style="cursor: pointer"><b @click="loadTasks()">Все категории</b></h3>
        <p>
          <ul class="ul-li">
            <li v-for="category in categories">
             <span><a class="a" v-if="!category.parent" href="#" @click="loadTasksByCategory(category)">{{category.name}}</a></span>
              <ul v-if="category.parent">
                <li class="ul-li">
                    <span><a class="a" @click="loadTasksByCategory(category)" href="#"><p>{{category.name}}</p></a></span>
                </li>
              </ul>
            </li>
          </ul>
        </p>
      </div>
    </aside>
     </div>
    </main>
    <footer>
      <div class="container">
        <p class="float-right">
          <a href="#">Наверх</a>
        </p>
        <p>Впервые на нашем сайте? <a href="/">Посетите главную </a> или прочитайте <a @click="goPage('about')" href="">о нас</a>.</p>
      </div>
    </footer>
 </div>
</template>

<script>
import { get, post } from "./../../Ajax/Http";

export default {
       name:"Tasks",
       props: {
         mess:'',
       },
       created(){
         this.loadTasks()
         this.loadCategories()
       },
       data() {
         return {
           page: 1,
           categories:[],
           tasks: [],
           perPage: 5,
           pages: [],
           categoryChilds: new Map(),
           checkedCategory: "",
         }
       },
       computed: {
         auth() {
             if (this.$store.getters.get_auth) return true
             else return false
         },
         displayedTasks() {
           return this.paginate(this.tasks);
         },
     },
       methods: {
         goPage(item) {
             this.$router.push({name: item})
         },
         loadTasks() {
           const url = this.$store.getters.get_url_server + 'api/v1/tasks/';
           get(url, response => {
               this.tasks=response.filter(r=>!r.approved);
               this.checkedCategory = "";
           });
         },
         loadCategoryChilds(id) {
           const url = this.$store.getters.get_url_server + 'api/v1/categoryChilds/' + id +'/';
           get(url, response => {
               if(response){
                 this.categoryChilds.set(id, response);
               }
             });
         },
         loadTasksByCategory(category) {
           const url = this.$store.getters.get_url_server + 'api/v1/allTasksByCategory/' + category.id +'/';
           get(url, response => {
               if(response){
                  this.tasks=response;
                  this.checkedCategory = category;
               };
             });
         },
         loadCategories() {
           const url = this.$store.getters.get_url_server + 'api/v1/categories/';
           get(url, response => {
               this.categories=response;
             });
         },
         loadTask(id) {
           this.$router.push({ name: 'task_detail', params: { taskId: id }})
         },
         loadProf(id) {
            if(this.$store.getters.get_user_info.user.id == id){
              this.$router.push({ name: "profile", params: { Id: id } });
            }
            else{
              this.$router.push({ name: "publicProfile", params: { Id: id } });
            }
          },
         setPages () {
           let numberOfPages = Math.ceil(this.tasks.length / this.perPage);
           this.pages=[]
           for (let index = 1; index <= numberOfPages; index++) {
             this.pages.push(index);
           }
         },
         paginate (tasks) {
           let page = this.page;
           let perPage = this.perPage;
           let from = (page * perPage) - perPage;
           let to = (page * perPage);
           return tasks.slice(from, to);
         }
       },
       watch: {
         tasks() {
           this.setPages()
         },
       },
       filters: {
           // Фильтр полной даты числами
           filterDateTime(item) {
               let old_date = new Date(item)
               return `
                ${old_date.getDate()}.${old_date.getMonth()+1}.${old_date.getFullYear()} в ${old_date.getHours()}:${old_date.getMinutes()}`
           },
         },
}
</script>


<style>
.h3 {
  margin-top: auto;
  margin-bottom: 0px;
  float: bottom;
}

  .a:hover {
  }

  .a {
  color: #0066cc;
  text-decoration: none;
  outline: none;
  }

  .a:active, a:focus {
  color: #818182;
  }


  #multi-derevo {
  border: 1px solid #bfbfbf;
  box-sizing: border-box;
  padding: 20px;
  width: 100%;
  font-size: 1.2em;
  }

  .ul-li {
   list-style-image:none;
   list-style-position:outside;
   list-style-type:none;
   margin-top: 10px;
   margin-left: 0;
   padding-left: 0;
  }
    ul li {
    line-height: 1.2em;
   }
      ul li ul li {
       margin: 0 0 0 1.2em;
      }


#pag {
 margin-bottom: 50px;

}

.price{
  margin-left: auto;
  margin-right: 20px;
  float: right;
  font-size: 140%;
  color: orange;
}

.material-icons{
     color: orange;

     position: inherit;
     padding: 3px;
     top: 5px;
     cursor: pointer;
}
#loginModal{
     color: orange;
     position: inherit;
     padding: 3px;
     top: 5px;
     cursor: not-allowed;
}

.category{
  color: gray;
  margin-left: 14px;
}

.glyphicon-thumbs-up{
     color: orange;
     position: relative;
     cursor: pointer;
}
</style>
