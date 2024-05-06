<script setup>
import store from "@/store";
</script>
<template>
    <div class="container mt-4">
      <form @submit.prevent="search" class="d-flex">
        <input v-model="searchQuery" class="form-control me-2" type="search" placeholder="Search" aria-label="Search" name="query">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
      <div v-if="searchResults">
        <h1>Search Results</h1>
        <h2>Songs</h2>
        <ul v-if="searchResults.songs.length">
          <li v-for="song in searchResults.songs" :key="song.id">
            <a :href="'/user/song/' + song.id">{{ song.name }}</a>
          </li>
        </ul>
        <p v-else>No songs found</p>
  
        <h2>Albums</h2>
        <ul v-if="searchResults.albums.length">
          <li v-for="album in searchResults.albums" :key="album.id">
            <a :href="'/user/album/' + album.id">{{ album.name }}</a>
          </li>
        </ul>
        <p v-else>No albums found</p>
  
        <h2>Creators</h2>
        <ul v-if="searchResults.creators.length">
          <li v-for="creator in searchResults.creators" :key="creator.id">
            <a :href="'/user/creator/' + creator.id">{{ creator.name }}</a>
          </li>
        </ul>
        <p v-else>No creators found</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        searchQuery: '',
        searchResults: null,
      };
    },
    methods: {
      async search() {
        if (!this.searchQuery.trim()) {
          console.log('Please enter a search query');
          return;
        } 
        try{
          const response = await fetch(`http://127.0.0.1:5000/api/search?query=${this.searchQuery}`, {
            headers: {
            "Authentication-Token": store.state.token
          }
          })
          const data = await response.json();
        this.searchResults = data;

        }
        catch(error) {
            console.error('Error performing search:', error);
          };
      },
    },
  };
  </script>
  
  
  