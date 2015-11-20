import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  user: {},
  team: {},
  challenges: [],
  store: undefined,
  challengeSorting: ['points'],
  sortedChallenges: Ember.computed.sort('challenges', 'challengeSorting'),
  setChallenges: function(){
    var chall_ids = this.get('team.solved');
    var store = this.get('store');

    if(chall_ids){
      var t = this;
      this.get('ctf.challengeboard').then(function(){
        var challenges = [];

        for (var i = 0; i < chall_ids.length; i++) {
          var id = chall_ids[i];
          var challenge = store.peekRecord('challenge', id);
          console.log('here!!!',challenge);
          if(challenge){
            challenges.push(challenge);
          }
        }
        t.set('challenges', challenges);
      });
    }
  }.observes('team').on('init'),
  actions: {
    closeProfileModal: function() {
      this.set('modal.isProfile', false);
    },
  },
});
