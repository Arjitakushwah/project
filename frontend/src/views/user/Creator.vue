<script setup>
import store from "@/store"
</script>
<template>
<div class="container">
  <h1>list of all creators</h1>
  <ul v-if="creators.length>0">
    <li v-for="creator in creators" :key="creator.id"><router-link :to="'/user/creator/' + creator.id">{{ creator.name
        }}</router-link></li>
  </ul>
  <p v-else>No creator found</p>
</div>
</template>

<script>
export default {
  data() {
    return {
      creators: [] 
    };
  },
  mounted() {
    this.fetchCreators(); 
  },
  methods: {
    fetchCreators() {
      fetch('http://127.0.0.1:5000/api/creators', {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          console.log(response)
          if (!response.ok) {
            throw new Error('Failed to fetch list of creators.');
          }
          return response.json();
        })
        .then(data => {
          this.creators = data;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching list of creators:', error);
        });
    }
  }
};
</script>