import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store';

import HomeView from '../views/HomeView.vue'
import Register from "@/views/Register.vue"
import Login from "@/views/Login.vue"
import Search from "@/views/Search.vue"

import UserHome from "@/views/user/UserHome.vue";
import UserDashboard from "@/views/user/UserDashboard.vue";
import Song from "@/views/user/Song.vue"
import Album from "@/views/user/Album.vue"
import Creator from "@/views/user/Creator.vue"
import SongPage from "@/views/user/SongPage.vue"
import AlbumPage from "@/views/user/AlbumPage.vue"
import CreatorPage from "@/views/user/CreatorPage.vue"
import CreatePlaylist from "@/views/user/CreatePlaylist.vue"
import Playlist from "@/views/user/Playlist.vue"
import AddSongPlaylist from "@/views/user/AddSongPlaylist.vue"
import RateSong from "@/views/user/RateSong.vue"
import RateCreator from "@/views/user/RateCreator.vue"
import RateAlbum from "@/views/user/RateAlbum.vue"
import ReportSong from "@/views/user/ReportSong.vue"
import UserProfile from "@/views/user/UserProfile.vue";

import CreatorHome from "@/views/creator/CreatorHome.vue";
import CreatorDashboard from "@/views/creator/CreatorDashboard.vue";
import CreatorRegister from "@/views/creator/CreatorRegister.vue";
import UploadSong from "@/views/creator/UploadSong.vue";
import Success from "@/views/creator/Success.vue"
import Edit from "@/views/creator/Edit.vue"
import EditAlbum from "@/views/creator/EditAlbum.vue"
import EditCreator from '@/views/creator/EditCreator.vue';


import AdminHome from "@/views/admin/AdminHome.vue";
import AdminDashboard from "@/views/admin/AdminDashboard.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: "/user",
      name: "userhome",
      component: UserHome,
      children: [
        {
          path: 'dashboard',
          name: 'userdashboard',
          component: UserDashboard
        },

        {
          path: 'profile',
          name: 'userprofile',
          component: UserProfile
        },
        {
          path: 'songs',
          name: 'User_Songs',
          component: Song
        },
        {
          path: 'song/:id',
          name: "User_songpage",
          component: SongPage,
          props: true
        },
        {
          path: 'albums',
          name: 'User_Albums',
          component: Album
        },
        {
          path: 'album/:id',
          name: "User_albumpage",
          component: AlbumPage,
          props: true
        },
        {
          path: 'creators',
          name: 'User_Creators',
          component: Creator
        },
        {
          path: 'creator/:id',
          name: 'CreatorPage',
          component: CreatorPage,
          props: true
        },
        {
          path: 'search',
          name: 'User_Search',
          component: Search
        },
        {
          path: 'creator/register',
          name: 'creator_register',
          component: CreatorRegister
        },
        {
          path: 'rate_song/:id',
          name: 'rate_song',
          component: RateSong
        },
        {
          path: 'rate_creator/:id',
          name: 'rate_creator',
          component: RateCreator
        },
        {
          path: 'rate_album/:id',
          name: 'rate_album',
          component: RateAlbum
        },
        {
          path: 'report_song/:id',
          name: 'report_song',
          component: ReportSong
        },
    {
      path: 'CreatePlaylist',
      name: 'CreatePlaylist',
      component: CreatePlaylist
    },

    {
      path: 'playlist/:id',
      name: 'playlist',
      component: Playlist,
    },
    {
      path: 'AddSongplaylist/:id',
      name: 'add_song_playlist',
      component: AddSongPlaylist,
      props: true

    }
      ]
    },
    {
      path: "/creator",
      name: "creatorhome",
      component: CreatorHome,
      children: [
        {
          path: 'dashboard',
          name: 'creator_dashboard',
          component: CreatorDashboard
        },
        {
          path: 'Edit_Creator/:id',
          name: 'EditCreator',
          props: true,
          component: EditCreator
        },
        {
          path: 'uploadsong',
          name: 'uploadsong',
          component: UploadSong
        },
        {
          path: 'success',
          name: 'Success',
          component: Success
        },
        {
          path: 'Edit_Song/:id',
          name: 'EditSong',
          props: true,
          component: Edit
        },
        {
          path: 'Edit_Album/:id',
          name: 'EditAlbum',
          props: true,
          component: EditAlbum
        },
        {
          path: 'song/:id',
          name: "creator_songpage",
          component: SongPage,
          props: true
        },
        {
          path: 'album/:id',
          name: "Creator_albumpage",
          component: AlbumPage,
          props: true
        },
        {
          path: 'rate_song/:id',
          name: 'c_rate_song',
          component: RateSong
        },
        {
          path: 'search',
          name: 'creator_Search',
          component: Search
        },

      ]
    },
    {
      path: "/admin",
      name: "adminhome",
      component: AdminHome,
      children: [
        {
          path: 'dashboard',
          name: 'admindashboard',
          component: AdminDashboard
        },
        {
          path: 'search',
          name: 'Admin_Search',
          component: Search
        },
        
    {
      path: 'song/:id',
      name: "Admin_songpage",
      component: SongPage,
      props: true
    },
    {
      path: 'album/:id',
      name: "Admin_albumpage",
      component: AlbumPage,
      props: true
    },
    {
      path: 'creator/:id',
      name: 'Admin_creator',
      component: CreatorPage,
    }
      ]
    }
    ,
    {
      path: '/logout',
      name: 'Logout'
    }
  ]
})

router.beforeEach((to, from) => {
  if (to.path.startsWith("/user")) {
    if (store.getters.getRoles.includes("user")) {
      return true
    }
    else {
      return { name: "login" }
    }
  }
  else if (to.path.startsWith("/admin")) {
    if (store.getters.getRoles.includes("admin")) {
      return true
    }
    else {
      return { name: "login" }
    }
  }
  else if (to.path.startsWith("/creator")) {
    if (store.getters.getRoles.includes("creator")) {
      return true
    }
    else {
      return { name: "login" }
    }
  }

  else if (to.path == "/logout") {
    store.commit("clearSession");
    return { name: 'login' }
  }
});
export default router
