<template>
    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Music Streaming App</router-link>
        <ul class="nav justify-content-end">
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/" class="nav-link" @click="logout">Logout</router-link>
          </li>
        </ul>
      </div>
    </nav>
</template>

<script>
  export default {
    methods: {
      logout() {
        console.log('User logged out');
      },
    },
  };
  </script>
