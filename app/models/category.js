import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  challengeboard: DS.belongsTo('challengeboard'),
  challenges: DS.hasMany('challenge'),
});

