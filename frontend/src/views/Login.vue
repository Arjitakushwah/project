<script setup>
import Navbar from "@/components/Navbar.vue"
import router from "@/router";
import store from "@/store";
</script>

<template>
  <Navbar />
  <div class="container mt-4">
    <h2>Login</h2>
    <form @submit="UserLogin">
      <div class="form-group mt-4">
        <label for="email">Email:</label>
        <input v-model="email" type="email" id="email" name="email" class="form-control"  />
        <p v-if="error.email === 'block'" class="error-message">Please enter a valid email address.</p>
      </div>
      <div class="form-group mt-2">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" name="password" class="form-control"  />
      </div>
      <p v-if="error.password === 'block'" class="error-message">Password is required.</p>
      <p v-if="error.message" class="error-message">{{ error.message }}</p>
      <button type="submit" class="btn btn-primary mt-2">Login</button>
    </form>

    <p>
      Don't have an account? <router-link to="/register">Register</router-link>
    </p>
    
  </div>
</template>

<script>
export default
  {
    data() {
      return {
        email: "",
        password: null,
        error: {
          email: "none",
          password: "none",
          message: null
        }

      }
    },
    methods: {
      validate() {
        this.error = {
          email: "none",
          password: "none"
        }
        let valid = true;

        if (!this.email.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
          this.error.email = "block";
          valid = false;
        }

        if (!this.password) {
          this.error.password = "block";
          valid = false;
        }
        return valid;
      },
      UserLogin(event) {
        event.preventDefault();
        if (this.validate()) {
          fetch("http://127.0.0.1:5000/api/login",
            {
              method: "POST",
              headers:
              {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                email: this.email,
                password: this.password
              })
            }).then(response => {
              if (response.ok) {
                return response.json()
              }
              else {
            throw new Error('Invalid credentials');
          }
            }).then(response => {
              const roles = response.roles || [];
          const token = response.token || null;

          store.commit("setRoles", roles);
          store.commit("setToken", token);

          if (roles.includes("user")) {
            router.push({ name: "userdashboard" });
          } else if (roles.includes("admin")) {
            router.push({ name: "admindashboard" });
          } else {
            throw new Error('Unauthorized user');
          }
        }).catch(error => {
          console.error("Login failed:", error.message);
          this.error.message=error.message;
        });
        }
      }
    }
  }
</script>

<style scoped>
.error-message {
  color: red;
}
</style>