import { markRaw } from 'vue';

// Mixin to track when a field becomes "done" based on value changes
export const FieldDoneMixin = {
  data() {
    return { progressed: false }
  },
  emits: ['progressed'],
  watch: {
    modelValue(value) {
      let progressed = false
      if (Array.isArray(value)) progressed = value.length > 0
      else progressed = value != null && value !== ''
      this.progressed = progressed
      this.$emit('progressed', { id: this.question.id, progressed, value })
    } 
  }
};

export const TextAreaField = {
  name: 'TextAreaField',
  props: {
    modelValue: { type: String, default: '' },
    question:    { type: Object, required: true }
  },
  mixins: [FieldDoneMixin],
  emits: ['update:modelValue', 'progressed'],
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
  mixins: [FieldDoneMixin],
  emits: ['update:modelValue', 'progressed'],
  template: `
    <fieldset :id="question.id" class="mb-4">
      <legend class="font-medium mb-1">{{ question.question }}</legend>
      <div v-for="opt in question.params.options" :key="opt" class="flex items-center gap-2 mb-1">
        <input
          type="radio"
          :name="question.id"
          :value="opt"
          class="form-check-input"
          :checked="modelValue === opt"
          @change="$emit('update:modelValue', opt)"
        />
        <label class="form-check-label">{{ opt }}</label>
      </div>
    </fieldset>`
};

export const CheckboxField = {
  name: 'CheckboxField',
  props: {
    modelValue: { type: Array, default: () => [] },
    question:   { type: Object, required: true }
  },
  mixins: [FieldDoneMixin],
  emits: ['update:modelValue', 'progressed'],
  methods: {
    toggle(val) {
      // Compute new array without mutating props
      const next = this.modelValue.includes(val)
        ? this.modelValue.filter(v => v !== val)
        : [...this.modelValue, val];
      this.$emit('update:modelValue', next);
    }
  },
  template: `
    <fieldset :id="question.id" class="mb-4">
      <legend class="font-medium mb-1">{{ question.question }}</legend>
      <div v-for="opt in question.params.options" :key="opt" class="flex items-center gap-2 mb-1">
        <input
          type="checkbox"
          class="form-check-input"
          :value="opt"
          :checked="modelValue.includes(opt)"
          @change="toggle(opt)"
        />
        <label class="form-check-label">{{ opt }}</label>
      </div>
    </fieldset>`
};

export const RangeField = {
  name: 'RangeField',
  props: {
    modelValue: { type: [Number, String], default: 0 },
    question:   { type: Object, required: true }
  },
  mixins: [FieldDoneMixin],
  emits: ['update:modelValue', 'progressed'],
  data() {
    return { current: this.modelValue ?? this.question.params.min ?? 0 };
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
        :min="question.params.min"
        :max="question.params.max"
        :step="question.params.step || 1"
        :value="current"
        @input="e => { this.current = e.target.value; $emit('update:modelValue', Number(e.target.value)) }"
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
    schema: { type: Array, required: true },
    modelValue: { type: Object, default: () => ({}) }
  },
  data() {
    // mark fieldRegistry raw to avoid Proxying component definitions
    return { fieldRegistry: markRaw(fieldRegistry) };
  },
  emits: ['update:modelValue', 'submit', 'progressed'],
  methods: {
    update(id, value) {
      const next = { ...this.modelValue, [id]: value };
      this.$emit('update:modelValue', next);
    },
    // Flatten category → questions into iterable array
    flatQuestions() {
      const arr = [];
      this.schema.forEach(category => {
        (category.questions || []).forEach((q, idx) => {
          arr.push({
            ...q,
            id: `${category.category_title}-${idx}`,
            category: category.category_title,
            categoryDescription: category.category_description,
          });
        });
      });
      return arr;
    }
  },
  template: `
    <form class="space-y-6">
      <template v-for="(group, idx) in groupByCategory" :key="idx">
        <h2 class="text-xl font-semibold">{{ group.category }}</h2>
        <p v-if="group.categoryDescription" class="text-gray-600 mb-2">{{ group.categoryDescription }}</p>
        <component
          v-for="q in group.items"
          :key="q.id"
          :is="fieldRegistry[q.question_type.toLowerCase()] || UnknownField"
          :question="q"
          :model-value="modelValue[q.id] ?? (q.question_type==='checkbox'? [] : '')"
          @update:modelValue="val => update(q.id, val)"
          @progressed="$emit('progressed', $event)"
        />
      </template>
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
