<script setup>
import store from "@/store"
import router from "@/router";
</script>
<template>
  <div>
    <h2>Report Song</h2>
    <form @submit.prevent="submitReport">
      <p>You want to report the song?</p>
      <button type="submit" class="btn btn-danger">Yes,Report Song</button>
    </form>
  </div>
</template>

<script>
export default {
  methods: {
    async submitReport() {
      try {
        const songId = this.$route.params.id;
        const response = await fetch(`http://127.0.0.1:5000/api/report_song/${songId}`, {

          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          }
        });
        if (!response.ok) {
          throw new Error('Failed to report song');
        }
        router.push({ name: "User_songpage", params: { id: this.$route.params.id } });
      } catch (error) {
        console.error('Error reporting song:', error);
      }
    }
  }
};
</script>