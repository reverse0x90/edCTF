import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  online: DS.attr('boolean'),
  ctftime: DS.attr('string'),
  about: DS.belongsTo('about', {async: true}),
  home: DS.belongsTo('home', {async: true}),
  challengeboard: DS.belongsTo('challengeboard', {async: true}),
  scoreboard: DS.belongsTo('scoreboard', {async: true}),
});