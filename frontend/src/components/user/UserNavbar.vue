<script setup>
import store from "@/store";
import router from "@/router";
import { computed } from 'vue';
const CreatorLink = computed(() => {
  if (store.getters.getRoles.includes('creator')) {
    return '/creator/dashboard';
  } else {
    return '/user/creator/register';
  }
});

</script>
<template>
    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Music Streaming App</router-link>

        <ul class="nav justify-content-end">
          <li class="nav-item">
            <router-link to="/user/search" class="nav-link"> Search </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/dashboard" class="nav-link"> Home </router-link>
          </li>
          <li class="nav-item">
            <router-link :to="CreatorLink" class="nav-link"> Creators Account </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/profile" class="nav-link"> Profile </router-link>
          </li>
          <li class="nav-item">
            <router-link to="/logout" class="nav-link" @click="logout"> Logout </router-link>
          </li>
        </ul>
      </div>
    </nav>
</template>

  
