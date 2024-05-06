<script setup>
import store from "@/store"
</script>
<template>
  <div class="welcome-quote text-center my-4">
    <h2>Welcome to Your App</h2>
    <p>Discover and enjoy your favorite music!</p>
  </div>
  <div class="container mt-4">
    <div class="d-flex mt-4 justify-content-between align-items-center">
      <h2>Songs</h2>
      <router-link to="/user/songs" class="btn btn-info">All Songs</router-link>
    </div>
    <hr>
    <div class="row">
      <div v-for="song in songs.slice(0, 4)" :key="song.id" class="col col-md-3">
        <div class="card border-primary" style="width: 14rem; height: 8rem;">
          <div class="card-body">
            <h5 class="card-title">{{ song.name }}</h5>
            <router-link :to="'/user/song/' + song.id" class="card-link btn btn-primary">View Lyrics</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h2>Albums</h2>
      <router-link to="/user/albums" class="btn btn-info">All albums</router-link>
    </div>
    <hr>
    <div class="row">
      <div v-for="album in albums.slice(0, 4)" :key="album.id" class="col col-md-3">
        <div class="card border-primary" style="width: 14rem; height: 8rem;">
          <div class="card-body">
            <h5 class="card-title">{{ album.title }}</h5>
            <router-link :to="'/user/album/' + album.id" class="card-link btn btn-primary">Album Details</router-link>
          </div>
        </div>
      </div>
      </div>
  </div>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h2>My Playlist</h2>
      <router-link to="/user/CreatePlaylist" class="btn btn-info">Create Playlist</router-link>
    </div>
    <hr>
    <div class="row">
      <div v-for="playlist in user.playlist.slice(0, 4)" :key="playlist.id" class="col col-md-3">
        <div class="card border-primary" style="width: 14rem; height: 8rem;">
          <div class="card-body">
            <h5 class="card-title">{{ playlist.name }}</h5>
            <router-link :to="'/user/playlist/' + playlist.id" class="card-link btn btn-primary">View Playlist</router-link>
          </div>
        </div>
      </div>
      </div>
  </div>

  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
      <h2>Creators</h2>
      <router-link to="/user/creators" class="btn btn-info">All Creators</router-link>
    </div>
    <hr>
    <div class="row">
      <div v-for="creator in creators.slice(0, 4)" :key="creator.id" class="col col-md-3">
        <div class="card border-primary" style="width: 14rem; height: 8rem;">
          <div class="card-body">
            <h5 class="card-title">{{ creator.name }}</h5>
            <router-link :to="'/user/creator/' + creator.id" class="card-link btn btn-primary">Creator Profile</router-link>
          </div>
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songs: [],
      albums:[],
      user:{
        playlist:[]
      },
      creators:[]
    };
  },
  mounted() {
    this.fetchSongs();
    this.fetchAlbums();
    this.fetchUserData();
    this.fetchCreators();
  },
  methods: {
     fetchSongs() {
      fetch('http://127.0.0.1:5000/api/song',{
        headers: {
          "Authentication-Token": store.state.token
        }
      })
         .then(response => response.json())
        .then(data => {
        this.songs = data;
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
        });
    },
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
    },
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
