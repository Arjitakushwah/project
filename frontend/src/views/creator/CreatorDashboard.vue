<script setup>
import { RouterView } from "vue-router";
import router from "@/router";
import store from "@/store"
</script>
<template>

  <div v-if='!creatorData.flagged'class="container mt-4">
    <div class="card">
      <div class="card-header">
        <h4>creator name: {{ creatorData.name }}</h4>
        <p>email: {{ creatorData.email }}</p>
        <p>Bio: {{ creatorData.bio }}</p>
        <router-link :to="'/creator/Edit_Creator/' + creatorData.id "><button class="btn btn-secondary btn-sm">Edit creator details</button></router-link>
      </div>
    </div>
    <br>
    <div class="row">
      <div class="col col-md-4">
        <div class="card" style="width: 18rem; height: 10rem;">
          <div class="card-body">
            <h2 class="card-title">Total Songs Uploaded </h2>
            <h3>{{ creatorData.total_songs }}</h3>
          </div>
        </div>
      </div>

      <div class="col col-md-4">
        <div class="card" style="width: 18rem; height: 10rem;">
          <div class="card-body">
            <h2 class="card-title">Total Albums </h2>
            <h3>{{ creatorData.total_albums }}</h3>
          </div>
        </div>
      </div>

      <div class="col col-md-4">
        <div class="card" style="width: 18rem; height: 10rem;">
          <div class="card-body">
            <h2 class="card-title">Average Rating </h2>
            <h3>{{ creatorData.average_rating }}</h3>
          </div>
        </div>
      </div>
    </div>
    <!-- List of Albums -->
    <div class="mt-4">
      <h2>Albums</h2>
      <ul v-if=" creatorData.albums.length > 0 ">
        <li v-for="album in creatorData.albums" :key="album.id" class="list-item">
          <router-link :to="'/creator/album/' + album.id">{{ album.name }}</router-link>
          &nbsp;
          <router-link :to="'/creator/Edit_Album/' + album.id"><button class="btn btn-secondary btn-sm">Edit album</button></router-link>&nbsp;
          <button class="btn btn-danger btn-sm" @click="deleteAlbum(album.id)">Delete</button>
        </li>
      </ul>
      <p v-else>No album created</p>
    </div>
    <!-- List of Songs -->
    <div class="mt-4">
      <h2>Songs</h2>
        <ul v-if=" creatorData.songs.length > 0" >
          <li v-for="song in creatorData.songs" :key="song.id" class="list-item">
            <router-link :to="'/creator/song/' + song.id">{{ song.name }}</router-link>&nbsp;
            <router-link :to="'/creator/Edit_Song/' + song.id"><button class="btn btn-secondary btn-sm">Edit Song</button></router-link>&nbsp;
            <button class="btn btn-danger btn-sm" @click="deleteSong(song.id)">Delete</button>
          </li>
        </ul>
        <p v-else>No song created</p>
      </div>
    <!-- Create Album Form -->
    <div class="card mt-4 mx-auto" style="max-width: 500px;">
      <div class="card-header">
        <h5>Create New Album</h5>
      </div>
      <div class="card-body">
        <form @submit.prevent="createAlbum">
          <div class="form-group mb-3">
            <label for="albumTitle">Album Title</label>
            <input type="text" class="form-control" id="albumTitle" v-model="albumTitle" required>
          </div>
          <button type="submit" class="btn btn-primary">Create Album</button>
        </form>
      </div>
    </div>
  </div>
  <div class="container mt-4" v-else>
    Your Creator Account has been blocked by the admin
  </div>
</template>

<script>
export default {
  data() {
    return {
      albumTitle: '',
      creatorData: {
        albums: [],
        songs: [],
        flagged:0
      },
    };
  },
  mounted() {
    this.fetchDashboardData();
  },
  methods: {
    fetchDashboardData() {
      fetch('http://127.0.0.1:5000/api/creator/dashboard', {
        headers: {
          'Content-Type': 'application/json',
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          if (response.ok) {
            return response.json();
          }
        })
        .then(data => {
          this.creatorData = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    async createAlbum() {
      try {
        const albumData = {
          title: this.albumTitle
        };
        const response = await fetch('http://127.0.0.1:5000/api/creator/create_album', {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          },
          body: JSON.stringify(albumData)
        });

        if (response.status === 201) {
          router.push({ name: "Success" });
        } else {
          console.error('Failed to create album');
        }
      } catch (error) {
        console.error('Error:', error);
      }


    },
    async deleteAlbum(albumId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/deleteAlbum/${albumId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          },
        });

        if (response.ok) {
          this.creatorData.albums = this.creatorData.albums.filter(album => album.id !== albumId);
          console.log('Album deleted successfully');
          this.fetchDashboardData()
        } else {
          console.error('Failed to delete album');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async deleteSong(songId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/deletesong/${songId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          },
        });

        if (response.ok) {
          this.creatorData.songs = this.creatorData.songs.filter(song => song.id !== songId);
          console.log('Song deleted successfully');
          this.fetchDashboardData()
      }
          
         else {
          console.error('Failed to delete song');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }

  }
}
</script>

<style scoped>
  .list-item {
    margin-bottom: 10px;
  }
</style>