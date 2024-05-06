<script setup>
import store from "@/store"
</script>
<template>
  <div class="container mt-4">
    <h2>User Profile</h2>
    <div v-if="user">
      <div class="card">
        <div class="card-body">
          <p><strong>Name:</strong> {{ user.name }}</p>
          <p><strong>Email:</strong> {{ user.email }}</p>
        </div>
      </div>
      <h3>playlist</h3>
      <div v-if="user.playlist.length > 0">
        <ul>
          <li v-for="playlist in user.playlist" :key="playlist.id" class="list-item">
            <router-link :to="'/user/playlist/' + playlist.id">{{ playlist.name }}</router-link>&nbsp;
            <router-link :to="'/user/AddSongplaylist/' + playlist.id"><button class="btn btn-primary btn-sm">Edit Playlist</button></router-link>&nbsp;
            <button @click="deleteplaylist(playlist.id)" class="btn btn-danger btn-sm">Delete</button>
          </li>
        </ul>
      </div>
      <div v-else>
        no playlist created
      </div>
      <router-link :to="'/user/CreatePlaylist'"><button>Create Playlist</button></router-link>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: null,
    };
  },
  mounted() {
    this.fetchUserData();
  },
  methods: {
    fetchUserData() {
      fetch('http://127.0.0.1:5000/api/user', {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          console.log(response)
          if (!response.ok) {
            throw new Error('Failed to fetch user profile.');
          }
          return response.json();
        })
        .then(data => {
          console.log(data)
          this.user = data;
        })
        .catch(error => {
          console.error('Error fetching user profile:', error);
        });
    },
    deleteplaylist(playlistId) {
      fetch(`http://127.0.0.1:5000/api/deleteplaylist/${playlistId}`, {
        method: 'DELETE',
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to delete playlist.');
          }
          this.user.playlist = this.user.playlist.filter(playlist => playlist.id !== playlistId);
          console.log('Playlist deleted successfully');
        })
        .catch(error => {
          console.error('Error deleting playlist:', error);
        });
    }
  }
}
</script>
<style scoped>
.list-item {
  margin-bottom: 10px;
}
</style>