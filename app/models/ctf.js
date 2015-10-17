import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  challengeboard: DS.belongsTo('challengeboard', {async: true}),
  scoreboard: DS.belongsTo('scoreboard', {async: true}),
});