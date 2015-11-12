import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  points: DS.attr('number'),
  description: DS.attr('string'),
  solved: DS.hasMany('team', {async: true}),
  numSolved: DS.attr('number'),
  category: DS.belongsTo('category'),
  isSolved: false,
});