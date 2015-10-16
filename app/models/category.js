import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  ctf: DS.belongsTo('ctf'),
  challenges: DS.hasMany('challenge', { async: true }),
});

