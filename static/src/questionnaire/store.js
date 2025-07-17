import { defineStore } from "pinia";
import axios from "axios";

export const useQuestionnaireStore = defineStore("questionnaire", {
  state: () => ({
    schema: [],
    formData: {},
    selected: null,
    schemaId: null
  }),
  getters: {
    // progress per category: { total, answered }
    progress: (state) =>
      state.schema.map((cat) => {
        const total = (cat.questions || []).length;
        const answered = (cat.questions || []).reduce((acc, _, idx) => {
          const categoryDictory = state.formData[cat.category_title] || {};
          const key = `${cat.category_title}-${idx}`;
          return acc + (categoryDictory.hasOwnProperty(key) ? 1 : 0);
        }, 0);
        return { total, answered };
      }),
    // overall progress across all categories
    overallProgress() {
      // Return zero progress if no categories
      if (!this.schema.length) {
        return { total: 0, answered: 0 };
      }
      // Sum total and answered counts across all categories using progress getter
      return this.progress.reduce(
        (acc, { total, answered }) => {
          acc.total += total;
          acc.answered += answered;
          return acc;
        },
        { total: 0, answered: 0 }
      );
    },
  },
  actions: {
    async fetchSchema(country = "AT") {
      try {
        const { data } = await axios.get("/questionnaire/definitions/", {
          params: { country },
        });
        this.schemaId = data.id;        
        this.schema = data.definition;
      } catch (error) {
        console.error("Failed to fetch schema:", error);
      }
    },
    // handle individual field completion events
    setDone({ id, done, value }) {
      if (done) {
        this.formData[id] = value;
      } else {
        delete this.formData[id];
      }
    },
    // bulk update formData for a given category
    updateCategoryData(categoryId, data) {
        if (!(categoryId in this.formData)) {
          this.formData[categoryId] = {};
        }
        this.formData[categoryId] = {
          ...this.formData[categoryId],
          ...data,
        };
    },
  },
  persist: {
    storage: sessionStorage, // data in sessionStorage is cleared when the page session ends.
  },
});
