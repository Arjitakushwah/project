<script setup>
import Navbar from "@/components/Navbar.vue"
import router from "@/router";
</script>

<template>
    <Navbar/>
    <div class="container" id="form-container">
    <h1 class="mt-5">Register</h1>
    <form @submit="registerUser" class="mt-3">
      <div class="form-group" :class="{ 'has-error': error.name === 'block' }">
        <label for="name">Name:</label>
        <input v-model="name" type="text" id="name" name="name" class="form-control">
        <p v-if="error.name === 'block'" class="error-message">Name is required (minimum 3 characters).</p>
      </div>
      
      <div class="form-group" :class="{ 'has-error': error.email === 'block' }">
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" name="email" class="form-control" >
        <p v-if="error.email === 'block'" class="error-message">Please enter a valid email address.</p>
      </div>

      <div class="form-group" :class="{ 'has-error': error.password === 'block' }">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" name="password" class="form-control">
        <p v-if="error.password === 'block'" class="error-message">Password is required.</p>
      </div>

      <button type="submit" class="mt-3 btn btn-primary">Register</button>
    </form>
    <p v-if="error.exist === 'block'" class="error-message">Email already in use.</p>
    <p class="mt-3">
      Already have an account? <router-link to="/login" class="btn btn-link">Login</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data(){
    return {
      name: null,
      email: null,
      password: null,
      error:{
        name: 'none',
        email: 'none',
        password: 'none',
        exist: 'none'
      }
    };
  },
  methods: {
    validate_fullname() {
      this.error.name = this.name && this.name.length >= 3 ? 'none' : 'block';
      return this.error.name === 'none';
    },
    validate_email() {
      this.error.email = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email) ? 'none' : 'block';
      return this.error.email === 'none';
    },
    validate_password() {
      this.error.password = this.password ? 'none' : 'block';
      return this.error.password === 'none';
    },
    registerUser(event) {
      this.error.exist = 'none';
      event.preventDefault();
      if (this.validate_fullname() && this.validate_email() && this.validate_password()) {
        fetch("http://127.0.0.1:5000/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            name: this.name
          })
        }).then(response => {
          if (response.status === 201) {
            router.push({ name: "login" });
          } else if (response.status === 400) {
            return response.json();
          } else if (response.status === 409) {
            this.error.exist = 'block';
          }
        }).then(response => {
          if (response) {
            if (!response.email) {
              this.error.email = 'block';
            }
            if (!response.password) {
              this.error.password = 'block';
            }
            if (!response.name) {
              this.error.name = 'block';
            }
          }
        }).catch(error => {
          console.error('Error during registration:', error);
        });
      }
    }
  }
}
</script>

<style>
.has-error .form-control {
  border-color: red; 
}
.error-message {
  color: red;
}
</style>


