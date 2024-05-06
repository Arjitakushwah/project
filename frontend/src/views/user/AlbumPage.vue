<script setup>
import store from "@/store"
</script>
<template>
  <div>
    <div class="container">
      <div class="card mt-5 mx-auto" style="max-width: 500px;">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="card-subtitle mb-2 text-muted">Album Name: {{ album.title }}</h5>
            <router-link :to="'/user/rate_album/' + album.id" class="btn btn-primary">Rate this Album</router-link>
          </div>
          <h6 class="card-subtitle mb-2 text-muted">Creator Name: {{ album.creator }}</h6>
          <h6 class="card-subtitle mb-2 text-muted">Release Date: {{ album.release_date }}</h6>
          <h6 class="card-subtitle mb-2 text-muted">Rating: {{ album.rating }}</h6>
          <h1>Songs in album</h1>
          <ul v-if="album.songs.length>0">
            <li v-for="song in album.songs" :key="song.id"><router-link :to="'/user/song/' + song.id">{{ song.name
                }}</router-link></li>
          </ul>
          <p v-else>No song added to this album</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      album: {
        songs:[]
      }
    };
  },
  mounted() {
    this.fetchAlbumDetails(this.$route.params.id);
  },
  methods: {
    fetchAlbumDetails(AlbumId) {
      fetch(`http://127.0.0.1:5000/api/album/${AlbumId}`, {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => {
          if (!response.ok) {
            console.log(response)
            throw new Error('Failed to fetch song details.');
          }
          return response.json();
        })
        .then(data => {
          this.album = data;
          console.log(data)
        })
        .catch(error => {
          console.error('Error fetching song details:', error);
        });
    }
  }
};
</script>
