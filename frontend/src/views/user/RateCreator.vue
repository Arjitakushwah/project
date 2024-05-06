<script setup>
import store from "@/store";
import router from "@/router";
</script>
<template>
  <div class="container mt-4">
    <form @submit.prevent="submitRating">
      <div class="form-group">
        <label for="rating">Rating:</label>
        <div class="form-check" v-for="ratingOption in ratingOptions" :key="ratingOption.value">
          <input class="form-check-input" type="radio" :id="`rating${ratingOption.value}`" v-model="selectedRating"
            :value="ratingOption.value">
          <label class="form-check-label" :for="`rating${ratingOption.value}`">{{ ratingOption.label }}</label>
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Submit Rating</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedRating: null,
      ratingOptions: [
        { value: 1, label: '1 - Terrible' },
        { value: 2, label: '2 - Poor' },
        { value: 3, label: '3 - Average' },
        { value: 4, label: '4 - Good' },
        { value: 5, label: '5 - Excellent' }
      ],
      entityId: null 
    };
  },
  methods: {
    submitRating() {
      fetch(`http://127.0.0.1:5000/api/creator/${this.$route.params.id}/rate`, {
        method: 'POST',
        headers: {

          'Content-Type': 'application/json',
          'Authentication-Token': store.state.token
        },
        body: JSON.stringify({
          rating: this.selectedRating
        })
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to submit rating');
          }
          console.log('Rating submitted successfully');
          router.push({ name: "CreatorPage", params: { id: this.$route.params.id } });
        })
        .catch(error => {
          console.error('Error submitting rating:', error);
        });
    }
  }
};
</script>