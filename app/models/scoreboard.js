import DS from 'ember-data';

export default DS.Model.extend({
  numtopteams: DS.attr('number'),
  topteamsdata: DS.attr(),
  teams: DS.hasMany('team', {async: false}),
});
