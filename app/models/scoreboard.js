import DS from 'ember-data';

export default DS.Model.extend({
  numtopteams: DS.attr('number'),
  topteams: DS.attr('array'),
  topteams2: DS.attr(),
  teams: DS.hasMany('team', {async: false}),
});
