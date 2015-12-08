import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  categories: DS.hasMany('category', {async: false}),
  categorysorting: ['name', 'id'],
  sortedcategories: Ember.computed.sort('categories', 'categorysorting'),
});
