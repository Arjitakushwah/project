<script setup>
import store from "@/store"
</script>
<template>
  <div>
    <div class="container">
      <div class="card mt-5 mx-auto" style="max-width: 500px;">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center">
            <h2>{{ song.name }}</h2>
            <router-link :to="'/user/rate_song/' + song.id" class="btn btn-primary">Rate this song</router-link>
            <router-link :to="'/user/report_song/' + song.id" class="btn btn-danger">Report Song</router-link>
          </div>
          <h5 class="card-subtitle mb-4 text-muted">Singer: {{ song.singer }}</h5>
          <h5 class="card-subtitle mb-4 text-muted">Rating: {{ song.rating }}</h5>
          <p >Duration: {{ song.duration }} seconds</p>
          <p>Released on: {{ song.date_created }}</p>
          <audio controls :src="songAudioSrc">
      Your browser does not support the audio element.
    </audio>
          <h2 class="card-text mt-3">Lyrics</h2>
          <pre class="card-text">{{ song.lyrics }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      song: {},
      songAudioSrc: ""
    };
  },
  mounted() {
    const songId = this.$route.params.id;
    fetch(`http://127.0.0.1:5000/api/song/${songId}`, {
      headers: {
        "Authentication-Token": store.state.token 
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch song details.");
        }
        return response.json();
      })
      .then(data => {
        this.song = data;
        fetch(`http://127.0.0.1:5000/api/song/${songId}/file`, {
          headers: {
            "Authentication-Token": store.state.token
          }
        })
          .then(response => {
            if (!response.ok) {
              throw new Error("Failed to fetch song file.");
            }
            return response.blob();
          })
          .then(blob => {
            this.songAudioSrc = URL.createObjectURL(blob);
          })
          .catch(error => {
            console.error("Error fetching song file:", error);
          });
      })
      .catch(error => {
        console.error("Error fetching song details:", error);
      });
  }
};
</script>
