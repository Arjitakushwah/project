<script setup>
import router from "@/router";
import store from "@/store"
</script>
<template>
  <div class="container">
    <h2>Edit Album Details</h2>
    <form @submit.prevent="editAlbum">
      <div class="form-group mb-3">
        <label for="albumTitle">Album Title</label>
        <input type="text" class="form-control" id="albumTitle" v-model="album.title" required>
      </div>
      <button type="submit" class="btn btn-primary">edit name</button>
    </form>
    <h1>Songs in album</h1>
    <ul v-if="album.songs.length > 0">
      <li v-for="song in album.songs" :key="song.id">
        <router-link :to="'/creator/song/' + song.id">{{ song.name }}</router-link>
        <button @click="removeSongFromAlbum(song.id)">Remove Song</button>
      </li>
    </ul>
    <p v-else>No song added in this album</p>

    <h2>Add Songs to Album</h2>
    <div v-if="songs.length > 0" class="song-checkboxes">
      <label v-for="song in songs" :key="song.id" class="song-checkbox">
        <input type="checkbox" :value="song.id" v-model="selectedSongs">
        {{ song.name }}
      </label>
    </div>
    <p v-else>No song found</p>
    <button @click="addSongsToAlbum">Add Selected Songs</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songs: [],
      selectedSongs: [],
      albumId: null,
      album: {
        songs: []
      }
    };
  },
  mounted() {
    this.albumId = this.$route.params.id;
    this.fetchSongs();
  },
  methods: {
    fetchSongs() {
      fetch('http://127.0.0.1:5000/api/creator/songs', {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.songs = data;
          this.fetchAlbumDetails();
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
        });
    },
    fetchAlbumDetails() {
      fetch(`http://127.0.0.1:5000/api/album/${this.albumId}`, {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.album = data;
          this.filterSongs();
        })
        .catch(error => {
          console.error('Error fetching album details:', error);
        });
    },
    filterSongs() {
      this.songs = this.songs.filter(song => !this.isSongInAlbum(song.id));
    },
    isSongInAlbum(songId) {
      return this.album.songs.some(song => song.id === songId);
    },
    addSongsToAlbum() {
      console.log('Selected songs:', this.selectedSongs);

      fetch(`http://127.0.0.1:5000/api/album/${this.albumId}/add_songs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': store.state.token
        },
        body: JSON.stringify({
          song_ids: this.selectedSongs
        })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to add songs to album');
          }
          console.log('Songs added to album successfully');
          router.push({ name: "creator_dashboard" });
        })
        .catch(error => {
          console.error('Error adding songs to album:', error);
        });
    },
    removeSongFromAlbum(songId) {
      fetch(`http://127.0.0.1:5000/api/album/${this.albumId}/remove_song/${songId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': store.state.token
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to remove song from album');
          }
          console.log('Song removed from album successfully');
          router.push({ name: "creator_dashboard" });
        })
        .catch(error => {
          console.error('Error removing song from album:', error);
        });
    },
    async editAlbum() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/editalbum/${this.album.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': store.state.token
          },
          body: JSON.stringify(this.album)
        });

        if (response.ok) {
          console.log('album details updated successfully');
          router.push({ name: "creator_dashboard" });
        } else {
          console.error('Failed to update album details');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
  }
} 
</script>