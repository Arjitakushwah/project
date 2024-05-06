<script setup>
import store from "@/store"
</script>
<template>
    <div>
        <div class="container">
            <div class="card mt-5 mx-auto" style="max-width: 500px;">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <h2>Name:{{ creator.name }}</h2>
                        <router-link :to="'/user/rate_creator/' + creator.id" class="btn btn-primary">Rate this
                            Creator</router-link>

                    </div>
                    <h5 class="card-subtitle mb-4 text-muted">BIO: {{ creator.bio }}</h5>
                    <h5 class="card-subtitle mb-4 text-muted">Rating: {{ creator.rating }}</h5>

                    <h6 class="card-subtitle mb-2 text-muted">List of Albums:</h6>
                    <ul v-if="creator.albums.length > 0">
                        <li v-for="album in creator.albums" :key="album.id"><router-link
                                :to="'/user/album/' + album.id">{{ album.title
                                }}</router-link>
                        </li>
                    </ul>
                    <p v-else>No album Creater by this creator</p>

                    <h6 class="card-subtitle mb-2 text-muted">List of Songs:</h6>
                    <ul v-if="creator.songs.length > 0">
                        <li v-for="song in creator.songs" :key="song.id"><router-link :to="'/user/song/' + song.id">{{
                            song.name }}</router-link>

                        </li>
                    </ul>
                    <p v-else>No song created by this creator</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            creator: {
                albums: [],
                songs: []
            }
        };
    },
    mounted() {
        this.fetchCreatorDetails(this.$route.params.id);
    },
    methods: {
        fetchCreatorDetails(CreatorId) {
            fetch(`http://127.0.0.1:5000/api/creator/${CreatorId}`, {
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
                    this.creator = data;
                    console.log(data)
                })
                .catch(error => {
                    console.error('Error fetching song details:', error);
                });
        }
    }
};
</script>