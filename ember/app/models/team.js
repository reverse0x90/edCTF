import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  scoreboard: DS.belongsTo('scoreboard'),
  position: DS.attr('number'),
  teamname: DS.attr('string'),
  points: DS.attr('number'),
  correctflags: DS.attr('number'),
  wrongflags: DS.attr('number'),
  solves: DS.attr('array'),
  numsolved: Ember.computed('solves', function() {
    return this.get('solves').length;
  }),
});
