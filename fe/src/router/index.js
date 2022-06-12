import Vue from "vue";
import VueRouter from "vue-router";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
    redirect: "/1",
    children: [
      {
        path: "1",
        name: "HandleCenter",
        component: () => import("../views/HandleCenter.vue"),
      },
      {
        path: "2",
        name: "Search",
        component: () => import("../views/Search.vue"),
      },
      {
        path: "history/:email",
        name: "History",
        component: () => import("../views/History.vue"),
      },
      {
        path: "3",
        name: "SearchSimilarity",
        component: ()=> import("../views/SearchSimilarity.vue"),
      },
    ],
  },

  {
    path: "/result_search/:key/md5",
    // path: "/result/search/:key/md5",
    name: "Result",
    component: () => import("../views/Result.vue"),
  },
  {
    // path: "/result_sim/:key/:id0Rmd5",
    path:"/result_sim/:key/md5",
    name: "ReasultSim",
    component:() => import("../views/ResultSim.vue"),
  },
  {
    path: "/admin_home",
    name: "Admin",
    component: () => import("../views/admin/AdminHome.vue"),
    redirect: "/manage",
    children: [
      { path: "/manage", component: () => import("../views/admin/Manage.vue") },
      {
        path: "/statistics",
        component: () => import("../views/admin/Statistics.vue"),
      },
      {
        path: "/userchart",
        component: () => import("../views/admin/Userchart.vue"),
      },
    ],
  },
];

const router = new VueRouter({
  routes,
});

export default router;
