<template>
  <div class="container">
    <h1>Azure DevOps Repo Cleanup Tool</h1>
    <form @submit.prevent="generateReport">
      <input v-model="form.org_url" placeholder="Organization URL" required />
      <input v-model="form.project" placeholder="Project" required />
      <input v-model="form.repo" placeholder="Repository" required />
      <input v-model="form.pat" placeholder="Personal Access Token (PAT)" required type="password" />
      <input v-model="form.cutoff_date" type="date" required />
      <div class="btns">
        <button type="submit">Generate Report</button>
        <button @click.prevent="deleteBranches">Delete Stale Branches</button>
      </div>
    </form>
    <div v-if="result">
      <h2>Results</h2>
      <p>Total Branches: {{ result.total }}</p>
      <p>Stale Branches: {{ result.stale }}</p>
      <a v-for="file in result.files" :href="backend + '/download/' + file" download :key="file">Download {{ file }}</a>
    </div>
    <div v-if="deleted.length">
      <h2>Deleted Branches</h2>
      <ul><li v-for="b in deleted" :key="b">{{ b }}</li></ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      backend: 'http://localhost:5001',
      form: { org_url: '', project: '', repo: '', pat: '', cutoff_date: '' },
      result: null,
      deleted: []
    };
  },
  methods: {
    async generateReport() {
      try {
        const res = await axios.post(this.backend + '/report', this.form);
        this.result = res.data;
        this.deleted = [];
      } catch (e) {
        alert('Error generating report');
      }
    },
    async deleteBranches() {
      try {
        const res = await axios.post(this.backend + '/delete', this.form);
        this.deleted = res.data.deleted;
      } catch (e) {
        alert('Error deleting branches');
      }
    }
  }
};
</script>

<style>
body { font-family: sans-serif; background: #f6f6f6; padding: 20px; }
.container { background: white; padding: 20px; border-radius: 8px; max-width: 600px; margin: auto; box-shadow: 0 0 10px #ccc; }
input { display: block; margin: 10px 0; padding: 8px; width: 100%; }
.btns { display: flex; gap: 10px; }
button { padding: 10px; cursor: pointer; }
a { display: block; margin-top: 10px; }
</style>
