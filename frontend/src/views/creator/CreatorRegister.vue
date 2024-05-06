<script setup>
import router from "@/router";
import store from "@/store"
</script>

<template>
  <div class="container mt-4">
    <p class="mb-2">You don't have a creator's account</p>
    <h2>Register as a Creator</h2>
    
    <form @submit.prevent="CreatorRegister">
      <div class="form-group">
        <label for="name">Enter Yor Creator Name</label>
        <input v-model="name" type="text" id="name" name="name" class="form-control" />
        <p v-if="error.email === 'block'" class="error-message">Please enter a valid email address.</p>

      </div>
      <div class="form-group mt-2">
        <label for="bio">Add Creator's Bio</label>
        <input v-model="bio" type="text" id="bio" name="bio" class="form-control" />
      </div>
      <p v-if="error.bio === 'block'" class="error-message">bio is required.</p>
      <button type="submit" class="btn btn-primary mt-2">Create Creator's Account</button>
    </form>
  </div>

</template>
<script>
export default {
  data() {
    return {
      name: '',
      bio: '',
      error: {
        name: 'none',
        bio: 'none',
      }
    };
  },
  methods: {

    CreatorRegister() {
      fetch('http://127.0.0.1:5000/api/creator/register', {
        method: 'POST',
        headers: {
          "Authentication-Token": store.state.token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.name,
          bio: this.bio
        })
      }).then(response => {
        if (response.status == 201) {
          return response.json()
        }
        else {
          return {
            roles: [],
            token: null
          }
        }
      })
        .then(response => {
          if (response["roles"].includes("creator")) {
            store.commit("setRoles", response["roles"]);
            router.push({ name: "creator_dashboard" });
          }
        })
        .catch(error => {
          console.error('Error registering creator:', error);
        });
    }
  }
}
</script>
