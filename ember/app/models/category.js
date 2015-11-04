import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  challenges: DS.hasMany('challenge', {async: false}),
  challengeboard: DS.belongsTo('challengeboard'),
});

