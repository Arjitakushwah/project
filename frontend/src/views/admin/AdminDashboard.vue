<script setup>
import store from "@/store"
</script>
<template>
  <div class="container mt-4">
    <h2>ADMIN DASHBOARD</h2>
    <div>Total Users: {{ totalUsers }}</div>
    <div>Total Creators: {{ totalCreators }}</div>
    <div>Total Albums: {{ totalAlbums }}</div>
    <div>Total Song: {{ totalSongs }}</div>

    <div class="row">
      <div class="col col-md-4">
        <h3 class="mt-4">Song Rating Statistics</h3>
        <div>
          <canvas id="songRatingsChart"></canvas>
        </div>
      </div>

      <div class="col col-md-4">
        <h3 class="mt-4">Album Rating Statistics</h3>
        <div>
          <canvas id="albumRatingsChart"></canvas>
        </div>
      </div>

      <div class="col col-md-4">
        <h3 class="mt-4">Creator Rating Statistics</h3>
        <div>
          <canvas id="creatorRatingsChart"></canvas>
        </div>
      </div>
    </div>

    <h3 class="mt-4">List of All Songs</h3>
    <div v-if="songs.length > 0">
      <ul>
        <li v-for="song in songs" :key="song.id" class="list-item">
        <router-link :to="'/admin/song/' + song.id">{{song.name }} </router-link>
            <p>
              report count:{{ song.reports }}
              <button class='btn btn-danger btn-sm' @click="removeSong(song.id)">Remove Song</button>
          </p>
          <hr>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No songs available.</p>
    </div>

    <h3 class="mt-4">list of all Albums</h3>
    <div v-if="albums.length > 0">
      <ul>
        <li v-for="album in albums" :key="album.id" class="list-item">
          <p>
        <router-link :to="'/admin/album/' + album.id">{{ album.title }}</router-link>
          <button class='btn btn-danger btn-sm' @click="removeAlbum(album.id)">Remove Album</button>
        </p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No album available.</p>
    </div>

    <h3>list of all creators</h3>
    <div v-if="creators.length > 0">
      <ul>
        <li v-for="creator in creators" :key="creator.id" class="list-item"><router-link
            :to="'/admin/creator/' + creator.id">{{ creator.name }}</router-link>
          <button class='btn btn-danger btn-sm' @click="flagCreator(creator.id)" v-if="!creator.flagged">Flag
            Creator</button>

          <button class="btn btn-secondary btn-sm" @click="whitelistCreator(creator.id)" v-else>Whitelist
            Creator</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No creators available.</p>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      totalUsers: 0,
      totalCreators: 0,
      totalAlbums: 0,
      totalSongs: 0,
      songs: [],
      albums: [],
      creators: [],
      songRatingsChart: null,
      albumRatingsChart: null
    };
  },
  mounted() {
    this.fetchStatistics();
    this.fetchSongs();
    this.fetchAlbums();
    this.fetchCreators();
  },
  methods: {
    async fetchStatistics() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/admin/dashboard', {
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        const data = await response.json();
        this.totalUsers = data.total_users;
        this.totalCreators = data.total_creators;
        this.totalAlbums = data.total_albums;
        this.totalSongs = data.total_songs;
      } catch (error) {
        console.error('Error fetching statistics:', error);
      }
    },
    async fetchSongs() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/song', {
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        this.songs = await response.json();
        if (this.songRatingsChart) {
        this.songRatingsChart.destroy();
      }

      // Render the new chart
      this.renderSongRatingsChart();
      } catch (error) {
        console.error('Error fetching songs:', error);
      }
    },
    async fetchAlbums() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/albums', {
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        this.albums = await response.json();
        if (this.albumRatingsChart) {
        this.albumRatingsChart.destroy();
      }
      this.renderAlbumRatingsChart();
      } catch (error) {
        console.error('Error fetching albums:', error);
      }
    },
    async fetchCreators() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/creators', {
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch list of creators.');
        }

        const data = await response.json();
        this.creators = data;
        this.renderCreatorRatingsChart();
        this.updateCreatorsList()
        console.log(data);
      } catch (error) {
        console.error('Error fetching list of creators:', error);
      }
    },
    async removeSong(songId) {
      try {
        await fetch(`http://127.0.0.1:5000/api/deletesong/${songId}`, {
          method: 'DELETE',
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        this.fetchSongs();
        this.updateCreatorsList()
      } catch (error) {
        console.error('Error removing song:', error);
      }
    },
    async removeAlbum(albumId) {
      try {
        await fetch(`http://127.0.0.1:5000/api/deleteAlbum/${albumId}`, {
          method: 'DELETE',
          headers: {
            "Authentication-Token": store.state.token
          }
        });
        this.fetchAlbums();
        this.updateCreatorsList()
      } catch (error) {
        console.error('Error removing album:', error);
      }
    },
    async flagCreator(creatorId) {
      try {
        await fetch(`http://127.0.0.1:5000/api/flag_creator/${creatorId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          },
          body: JSON.stringify({ flagged: true })
        });
        this.updateCreatorsList()

      } catch (error) {
        console.error('Error in flagging creator:', error);
      }
    },
    async whitelistCreator(creatorId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/whitelist_creator/${creatorId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authentication-Token': store.state.token
          }
        });

        if (!response.ok) {
          throw new Error('Failed to whitelist creator.');
        }
        this.updateCreatorsList()
        console.log(`Creator ${creatorId} whitelisted successfully`);
      } catch (error) {
        console.error('Error whitelisting creator:', error);
      }
    },
    async updateCreatorsList() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/creators', {
          headers: {
            'Authentication-Token': store.state.token
          }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch updated list of creators.');
        }
        const data = await response.json();
        this.creators = data;
      } catch (error) {
        console.error('Error updating list of creators:', error);
      }
    },
    renderSongRatingsChart() {
      const canvas = document.getElementById('songRatingsChart');
  
  // Destroy the previous chart instance if it exists
  if (this.songRatingsChart) {
    this.songRatingsChart.destroy();
  }
      const ctx = canvas.getContext('2d');
      this.songRatingsChart=new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.songs.map(song => song.name),
          datasets: [{
            label: 'Average Rating',
            data: this.songs.map(song => song.rating),
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

    },
    renderAlbumRatingsChart() {
      const canvas = document.getElementById('albumRatingsChart');
  
  // Destroy the previous chart instance if it exists
  if (this.albumRatingsChart) {
    this.albumRatingsChart.destroy();
  }
      const ctx = canvas.getContext('2d');
      this.albumRatingsChart=new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.albums.map(album => album.title),
          datasets: [{
            label: 'Average Rating',
            data: this.albums.map(album => album.rating),
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

    },
    renderCreatorRatingsChart() {
      const ctx = document.getElementById('creatorRatingsChart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.creators.map(creator => creator.name),
          datasets: [{
            label: 'Average Rating',
            data: this.creators.map(creator => creator.rating),
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });

    }
  }
};
</script>
<style scoped>
.list-item {
  margin-bottom: 10px;
}
</style>