import Ember from 'ember';
import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  challenges: DS.hasMany('challenge', {async: false}),
  challengesorting: ['points', 'id'],
  sortedchallenges: Ember.computed.sort('challenges', 'challengesorting'),
  challengeboard: DS.belongsTo('challengeboard'),
});

