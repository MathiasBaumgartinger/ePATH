export const TextAreaField = {
  name: 'TextAreaField',
  props: {
    modelValue: { type: String, default: '' },
    question:    { type: Object, required: true }
  },
  emits: ['update:modelValue'],
  template: `
    <div class="mb-4">
      <label :for="question.id" class="block font-medium mb-1">{{ question.question }}</label>
      <textarea
        :id="question.id"
        :rows="question.params?.rows || 3"
        class="border rounded p-2 w-full"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
      />
    </div>`
};

export const RadioField = {
  name: 'RadioField',
  props: {
    modelValue: [String, Number],
    question:   { type: Object, required: true }
  },
  emits: ['update:modelValue'],
  template: `
    <fieldset :id="question.id" class="mb-4">
      <legend class="font-medium mb-1">{{ question.question }}</legend>
      <div v-for="opt in question.params.options" :key="opt.value" class="flex items-center gap-2 mb-1">
        <input
          type="radio"
          :name="question.id"
          :value="opt.value"
          class="form-check-input"
          :checked="modelValue === opt.value"
          @change="$emit('update:modelValue', opt.value)"
        />
        <label class="form-check-label">{{ opt.label }}</label>
      </div>
    </fieldset>`
};

export const CheckboxField = {
  name: 'CheckboxField',
  props: {
    modelValue: { type: Array, default: () => [] },
    question:   { type: Object, required: true }
  },
  emits: ['update:modelValue'],
  methods: {
    toggle(val) {
      const next = this.modelValue.includes(val)
        ? this.modelValue.filter(v => v !== val)
        : [...this.modelValue, val]
      this.$emit('update:modelValue', next)
    }
  },
  template: `
    <fieldset :id="question.id" class="mb-4">
      <legend class="font-medium mb-1">{{ question.question }}</legend>
      <div v-for="opt in question.params.options" :key="opt.value" class="flex items-center gap-2 mb-1">
        <input
          type="checkbox"
          class="form-check-input"
          :checked="modelValue.includes(opt.value)"
          @change="toggle(opt.value)"
        />
        <label class="form-check-label">{{ opt.label }}</label>
      </div>
    </fieldset>`
};

export const RangeField = {
  name: 'RangeField',
  props: {
    modelValue: { type: [Number, String], default: 0 },
    question:   { type: Object, required: true }
  },
  emits: ['update:modelValue'],
  data() {
    return { current: this.modelValue || this.question.params.default_value || 0 };
  },
  watch: {
    modelValue(val) { this.current = val; }
  },
  template: `
    <div class="mb-4">
      <label :for="question.id" class="block font-medium mb-1">{{ question.question }} ({{ current }})</label>
      <input
        type="range"
        :id="question.id"
        class="w-full"
        :min="question.params.min_value"
        :max="question.params.max_value"
        :step="question.params.step || 1"
        :value="current"
        @input="e => { current = e.target.value; $emit('update:modelValue', Number(e.target.value)) }"
      />
    </div>`
};

export const fieldRegistry = {
  textarea: TextAreaField,
  radio:    RadioField,
  checkbox: CheckboxField,
  range:    RangeField,
};

export const QuestionnaireForm = {
  name: 'QuestionnaireForm',
  props: {
    schema: { type: Object, required: true },
    modelValue: { type: Object, default: () => ({}) }
  },
  data() {
    return { fieldRegistry };
  },
  emits: ['update:modelValue', 'submit'],
  methods: {
    update(id, value) {
      const next = { ...this.modelValue, [id]: value };
      this.$emit('update:modelValue', next);
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$emit('submit', this.modelValue);
    },
    // Flatten category → questions into iterable array
    flatQuestions() {
      const arr = [];
      Object.entries(this.schema).forEach(([catKey, catObj]) => {
        const catDesc = catObj.description || '';
        Object.entries(catObj.questions || {}).forEach(([qKey, qObj]) => {
          arr.push({
            ...qObj,
            id: qKey,
            category: catKey,
            categoryDescription: catDesc,
          });
        });
      });
      return arr;
    }
  },
  template: `
    <form @submit="onSubmit" class="space-y-6">
      <template v-for="(group, idx) in groupByCategory" :key="idx">
        <h2 class="text-xl font-semibold">{{ group.category }}</h2>
        <p v-if="group.categoryDescription" class="text-gray-600 mb-2">{{ group.categoryDescription }}</p>
        <component
          v-for="q in group.items"
          :key="q.id"
          :is="fieldRegistry[q.type.toLowerCase()] || UnknownField"
          :question="q"
          :model-value="modelValue[q.id] ?? q.params?.default_value ?? (q.type==='checkbox'?[]: '')"
          @update:modelValue="val => update(q.id, val)"
        />
      </template>
      <button type="submit" class="mt-4 px-4 py-2 rounded bg-blue-600 text-white">Submit</button>
    </form>`,
  computed: {
    groupByCategory() {
      const map = {};
      this.flatQuestions().forEach(q => {
        if (!map[q.category]) map[q.category] = { category: q.category, categoryDescription: q.categoryDescription, items: [] };
        map[q.category].items.push(q);
      });
      return Object.values(map);
    }
  },
  components: {
    UnknownField: {
      props: { question: Object },
      template: `<p class="text-red-600">Unknown field type: {{ question.type }}</p>`
    },
    ...fieldRegistry,
  }
};

export default {
  install(app) {
    app.component(QuestionnaireForm.name, QuestionnaireForm);
  }
};
