<script setup>
import router from "@/router";
import store from "@/store"
</script>
<template>
    <div class="container">
        <h3 class="mt-4">Edit your creator profile details</h3>
        <br>
        <form @submit.prevent="EditCreator">
      <div class="form-group">
        <label for="name">Creator Name:</label>
        <input v-model="name" type="text" id="name" name="name" class="form-control" />
      </div>
      <br>
      <div class="form-group">
        <label for="bio">Bio:</label>
        <input v-model="bio" type="text" id="bio" name="bio" class="form-control" />
      </div>
      <br>
      <button type="submit" class="btn btn-primary">Save Changes</button>
    </form>

  </div>
    
</template>
<script>
export default {
  data() {
    return {
      creatorId: '', 
      name: '',
      bio: ''
    };
  },
  mounted() {
    this.creatorId = this.$route.params.id;
    this.fetchCreatorDetails();
  },
  methods: {
    async fetchCreatorDetails() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/creator/${this.creatorId}`,
        {
            headers: {
          "Authentication-Token": store.state.token
        }
        });
        if (!response.ok) {
          throw new Error('Failed to fetch creator details');
        }
        const creatorData = await response.json();
        this.name = creatorData.name;
        this.bio = creatorData.bio;
      } catch (error) {
        console.error('Error fetching creator details:', error);
      }
    },
    async EditCreator() {
      try {
        const updatedData = {
          name: this.name,
          bio: this.bio
        };
        const response = await fetch(`http://127.0.0.1:5000/api/edit_creator/${this.creatorId}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": store.state.token
          },
          body: JSON.stringify(updatedData)
        });
        if (!response.ok) {
          throw new Error('Failed to update creator details');
        }
        console.log('Creator details updated successfully');
        router.push({ name: "creator_dashboard" });
      } catch (error) {
        console.error('Error editing creator details:', error);
      }
    }
  }
};
</script>