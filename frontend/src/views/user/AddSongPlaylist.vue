<script setup>
import store from "@/store";
import router from "@/router";
</script>

<template>
  <div class="container mt-4">
    <form @submit.prevent="EditPlaylist">
      <div class="form-group mb-3">
        <label for="playlistName">Playlist name</label>
        <input type="text" class="form-control" id="albumTitle" v-model="playlist.name" required>
      </div>
      <button type="submit" class="btn btn-primary">edit name</button>
    </form>

    <h1>List of songs</h1>
    <ul v-if="playlist.songs.length > 0">
      <li v-for="song in playlist.songs" :key="song.id">
        <router-link :to="'/user/song/' + song.id">{{ song.name }}</router-link>
        <button class="btn btn-danger" @click="removeSongFromPlaylist(song.id)">Remove Song</button>
      </li>
    </ul>
    <p v-else>Empty</p>

    <h2>Add Songs to Playlist</h2>
    <div class="song-checkboxes" v-if="songs.length>0">
      <label v-for="song in songs" :key="song.id" class="song-checkbox">
        <input type="checkbox" :value="song.id" v-model="selectedSongs">
        <router-link :to="'/user/song/' + song.id" class="colour">{{ song.name }}</router-link>
      </label>
    </div>
    <p v-else>no song available</p>
    <button class="btn btn-primary" @click="addSongsToPlaylist">Add Selected Songs</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      songs: [],
      selectedSongs: [],
      playlistId: null,
      playlist: {
        songs:[]
      }
    };
  },
  mounted() {
    this.playlistId = this.$route.params.id;
    this.fetchSongs();
  },
  methods: {
    fetchSongs() {
      fetch('http://127.0.0.1:5000/api/song', {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.songs = data;
          this.fetchPlaylistDetails();
        })
        .catch(error => {
          console.error('Error fetching songs:', error);
        });
    },
    fetchPlaylistDetails() {
      fetch(`http://127.0.0.1:5000/api/playlist/${this.playlistId}`, {
        headers: {
          "Authentication-Token": store.state.token
        }
      })
        .then(response => response.json())
        .then(data => {
          this.playlist = data;
          this.filterSongs();
        })
        .catch(error => {
          console.error('Error fetching playlist details:', error);
        });
    },
    filterSongs() {
      this.songs = this.songs.filter(song => !this.isSongInPlaylist(song.id));
    },
    isSongInPlaylist(songId) {
      return this.playlist.songs.some(song => song.id === songId);
    },
    addSongsToPlaylist() {
      console.log('Selected songs:', this.selectedSongs);

      fetch(`http://127.0.0.1:5000/api/playlist/${this.playlistId}/add_songs`, {
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
            throw new Error('Failed to add songs to playlist');
          }
          console.log('Songs added to playlist successfully');
          router.push({ name: "playlist", params: { id: this.playlistId } });
        })
        .catch(error => {
          console.error('Error adding songs to playlist:', error);
        });
    },
    removeSongFromPlaylist(songId) {
      fetch(`http://127.0.0.1:5000/api/playlist/${this.playlistId}/remove_song/${songId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': store.state.token
        }
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to remove song from playlist');
          }
          console.log('Song removed from playlist successfully');
          router.push({ name: "playlist", params: { id: this.playlistId } });
        })
        .catch(error => {
          console.error('Error removing song from playlist:', error);
        });
    },
    EditPlaylist() {
      fetch(`http://127.0.0.1:5000/api/editplaylist/${this.playlistId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': store.state.token
        },
        body: JSON.stringify(this.playlist)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed changing name of playlist');
          }
          console.log('playlist name changed successfully');
          router.push({ name: "playlist", params: { id: this.playlistId } });
        })
        .catch(error => {
          console.error('Error changing name of playlist:', error);
        });
    }

  }
};
</script>

<style>
.song-checkboxes {
  display: flex;
  flex-wrap: wrap;
}

.song-checkbox {
  margin-right: 20px;
}
.colour{
  color: black;
  text-decoration: none;
}
</style>
