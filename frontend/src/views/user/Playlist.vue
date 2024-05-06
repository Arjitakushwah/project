<script setup>
import store from "@/store";
import router from "@/router";
</script>

<template>
  <div class="container mt-4">
  <h1>{{ playlist.name }} </h1>
  <h1>List of songs</h1>

  <ul v-if="playlist.songs.length > 0">
    <li v-for="song in playlist.songs" :key="song.id">
      <router-link :to="'/user/song/' + song.id">{{ song.name }}</router-link>
    </li>
  </ul>
  <p v-else>no song available in this playlist</p>
  <router-link :to="'/user/AddSongplaylist/' + playlist.id" class="btn btn-info">EDIT PLAYLIST </router-link>
</div>
</template>
<script>
export default {
  data() {
    return {
      playlistId: null,
      playlist: {
        songs:[]
      }
    };
  },
  mounted() {
    this.playlistId = this.$route.params.id;
    this.fetchPlaylistDetails();
  },
  methods: {
    fetchPlaylistDetails() {
      fetch(`http://127.0.0.1:5000/api/playlist/${this.playlistId}`, {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.playlist = data;
        })
        .catch(error => {
          console.error('Error fetching playlist details:', error);
        });
    }
  }
}
</script>