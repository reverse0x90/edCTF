import DS from 'ember-data';

export default DS.Model.extend({
  numtopteams: DS.attr('number'),
  topteams: DS.attr('array'),
  teams: DS.hasMany('team'),
});
