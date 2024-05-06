<script setup>
import router from "@/router";
import store from "@/store"
</script>
<template>
    <div class="container">
        <h1>Edit Song</h1>
        <form @submit.prevent="saveChanges">
            <div class="form-group">
                <label for="song_name">Song Name</label>
                <input type="text" class="form-control" id="song_name" v-model="song.name" required />
            </div>
            <div class="form-group">
                <label for="artist_name">Artist Name</label>
                <input type="text" class="form-control" id="artist_name" v-model="song.singer" required />
            </div>
            <div class="form-group">
                <label for="lyrics">Lyrics</label>
                <textarea class="form-control" id="lyrics" v-model="song.lyrics" rows="4">
          </textarea>
            </div>
            <div class="form-group">
                <label for="duration">Duration (in seconds)</label>
                <input type="number" class="form-control" id="duration" v-model="song.duration" required />
            </div>
            <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            song: {
                id: null,
                name: '',
                singer: '',
                album_name: '',
                lyrics: '',
                duration: ''
            }
        };
    },
    mounted() {
        this.fetchSongDetails();
    },
    methods: {
        async fetchSongDetails() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/song/${this.$route.params.id}`, {
                    headers: {
                        'Content-Type': 'application/json',
                        "Authentication-Token": store.state.token
                    }
                })
                if (response.ok) {
                    const data = await response.json();
                    this.song = data;
                    console.log(data)
                } else {
                    console.error('Failed to fetch song details');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },
        async saveChanges() {
            try {
                const response = await fetch(`http://127.0.0.1:5000/api/editsong/${this.song.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authentication-Token': store.state.token
                    },
                    body: JSON.stringify(this.song)
                });

                if (response.ok) {
                    console.log('Song details updated successfully');
                    router.push({ name: "creator_dashboard" });
                } else {
                    console.error('Failed to update song details');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }
};
</script>