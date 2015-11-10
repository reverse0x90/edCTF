import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  points: DS.attr('number'),
  description: DS.attr('string'),
  solved: DS.attr('boolean'),
  num_solved: DS.attr('boolean'),
  category: DS.belongsTo('category'),
  isSolved: false,
});