import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  categories: DS.hasMany('category', {async: false}),
  categorySorting: ['name', 'id'],
  sortedCategories: Ember.computed.sort('categories', 'categorySorting'),
});
