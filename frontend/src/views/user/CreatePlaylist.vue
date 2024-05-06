<script setup>
import store from "@/store"
import router from "@/router";
</script>
<template>
  <div class="container mt-4">
    <h2>Create Playlist</h2>
    <form @submit.prevent="createPlaylist">
      <div class="form-group mb-3">
        <label for="name">Playlist Name:</label>
        <input type="text" class="form-control" id="name" v-model="playlistName" required>
      </div>
      <button class="btn btn-primary"type="submit">Create Playlist</button>
    </form>
  </div>

</template>

<script>
export default {
  data() {
    return {
      playlistName: ''
    };
  },
  methods: {
    createPlaylist() {
      const data = {
        name: this.playlistName
      };
      fetch("http://127.0.0.1:5000/api/createplaylist", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Authentication-Token": store.state.token
        },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to create playlist');
          }
          return response.json();
        })
        .then(data => {
          console.log('Playlist created successfully:', data);
          console.log(data)
          router.push({ name: "add_song_playlist", params: { id: data.id } });
        })
        .catch(error => {
          console.error('Error creating playlist:', error);
        });
    }
  }
}
</script>