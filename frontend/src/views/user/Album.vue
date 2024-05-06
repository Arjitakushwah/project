<script setup>
import store from "@/store"
</script>
<template>
<div class="container mt-4">
  <h1>list of all albums</h1>
  <ul v-if="albums.length>0">
    <li v-for="album in albums" :key="album.id"><router-link :to="'/user/album/' + album.id">{{ album.title
        }}</router-link></li>
  </ul>
  <p v-else>No album found</p>
</div>

</template>

<script>
export default {
  data() {
    return {
      albums: [] 
    };
  },
  mounted() {
    this.fetchAlbums(); 
  },
  methods: {
    fetchAlbums() {
      fetch('http://127.0.0.1:5000/api/albums', {
        headers: {
          "Authentication-Token": store.state.token
        }
      }) 
        .then(response => {
          console.log(response)
          if (!response.ok) {
            throw new Error('Failed to fetch list of albums.');
          }
          return response.json();
        })
        .then(data => {
          this.albums = data;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching list of Albums:', error);
        });
    }
  }
};
</script>