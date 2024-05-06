<script setup>
import Navbar from "@/components/Navbar.vue"
</script>

<template>
  <Navbar />
  <div class="container mt-5 text-center">
    <h1>Welcome to Music Streaming App</h1>
    <p>Discover and enjoy your favorite music!</p>
    <div class="row">
      <div class="col-md-6 offset-md-3">
        <router-link to="/register" class="btn btn-success btn-block mb-2">Register</router-link>
      </div>
      <div class="col-md-6 offset-md-3">
        <router-link to="/login" class="btn btn-primary btn-block mb-2">Login</router-link>
      </div>
    </div>
  </div>
</template>