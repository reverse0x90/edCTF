import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  challenges: DS.hasMany('challenge', {async: false}),
  challengeSorting: ['points', 'id'],
  sortedChallenges: Ember.computed.sort('challenges', 'challengeSorting'),
  challengeboard: DS.belongsTo('challengeboard'),
});

