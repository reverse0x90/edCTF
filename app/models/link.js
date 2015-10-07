import DS from 'ember-data';

export default DS.Model.extend({
  challenge_id: DS.belongsTo('challenge'),
  name: DS.attr('string'),
  path: DS.attr('string'),
});