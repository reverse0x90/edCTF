import DS from 'ember-data';

export default DS.Model.extend({
  category: DS.belongsTo('category'),
  title: DS.attr('string'),
  points: DS.attr('number'),
  description: DS.attr('string'),
  solved: DS.attr('boolean'),
  num_solved: DS.attr('boolean'),
});