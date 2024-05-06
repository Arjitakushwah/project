<script setup>
    import router from "@/router";
    import store from "@/store"
</script>
<template>
    <div class="container mt-4">
      <h3>Upload a Song</h3>
      <p>Fill in the details and upload your song:</p>
      <form @submit.prevent="uploadSong">
        <div class="form-group mb-2">
          <label for="songname" class="form-label">Song Name</label>
          <input type="text" class="form-control" id="songname" name="songname" v-model="songName" required>
        </div>
        <div class="form-group mb-2">
          <label for="artist" class="form-label">Artist Name</label>
          <input type="text" class="form-control" id="artist" name="artist" v-model="artistName" required>
        </div>
        <div class="form-group mb-2">
          <label for="albumname" class="form-label">Album Name(optional)</label>
          <input type="text" class="form-control" id="albumname" v-model="albumName" name="albumname">
        </div>
        <div class="form-group mb-2">
          <label for="lyrics" class="form-label">Lyrics</label>
          <textarea class="form-control" id="lyrics" name="lyrics" v-model="lyrics" rows="4"></textarea>
        </div>
        <div class="form-group mb-2">
          <label for="duration" class="form-label">Duration (in seconds)</label>
          <input type="number" class="form-control" id="duration" v-model="duration" name="duration" required>
        </div>
        <div class="form-group mb-2">
          <label for="songFile" class="form-label">Upload Song File</label>
          <input type="file" class="form-control-file" id="songFile" name="songFile" accept=".mp3" ref="songFileInput" required>
        </div>
        <button type="submit" class="btn btn-primary">Upload</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        songName: '',
        artistName: '',
        albumName: '',
        lyrics: '',
        duration: ''
      };
    },
    methods: {
      async uploadSong() {
        const formData = new FormData();
        formData.append('songName', this.songName);
        formData.append('artistName', this.artistName);
        formData.append('albumName', this.albumName);
        formData.append('lyrics', this.lyrics);
        formData.append('duration', this.duration);
        formData.append('songFile', this.$refs.songFileInput.files[0]);
        console.log(formData.values().next())
        try {
          const response = await fetch('http://127.0.0.1:5000/api/creator/uploadsong', {
            method: 'POST',
            body: formData,
            headers: {
                // "Content-Type": "multipart/form-data",
              "Authentication-Token": store.state.token
            }
          });
          if (response.ok) {
            router.push({ name: "Success" });
          } else {
            console.error('Failed to upload song');
          }
        } catch (error) {
          console.error('Error uploading song:', error);
        }
      }
    }
  };
  </script>
  