<script setup>
import store from "@/store"
</script>

<template>
  <div class="container mt-4">
  <h1>list of of songs</h1>
  <ul v-if="songs.length>0">
    <li v-for="song in songs" :key="song.id"><router-link :to="'/user/song/' + song.id">{{ song.name }}</router-link>
    </li>
  </ul>
  <p v-else>No song found</p>
</div>
</template>

<script>
export default {
  data() {
    return {
      songs: []
    };
  },
  mounted() {
    this.fetchSongs();
  },
  methods: {
    fetchSongs() {
      fetch('http://127.0.0.1:5000/api/song', {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          console.log(response)
          if (!response.ok) {
            throw new Error('Failed to fetch list of songs.');
          }
          return response.json();
        })
        .then(data => {
          this.songs = data;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching list of songs:', error);
        });
    }
  }
};
</script>