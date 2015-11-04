import DS from 'ember-data';

export default DS.Model.extend({
  scoreboard: DS.belongsTo('scoreboard'),
  position: DS.attr('number'),
  teamname: DS.attr('string'),
  points: DS.attr('number'),
  correct_flags: DS.attr('number'),
  wrong_flags: DS.attr('number'),
  solved: DS.attr('array'),
});
