import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  scoreboard: DS.belongsTo('scoreboard'),
  position: DS.attr('number'),
  teamname: DS.attr('string'),
  points: DS.attr('number'),
  correct_flags: DS.attr('number'),
  wrong_flags: DS.attr('number'),
  solves: DS.attr('array'),
  numSolved: Ember.computed('solves', function() {
    return this.get('solves').length;
  }),
});
