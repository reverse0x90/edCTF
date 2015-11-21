import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  user: {},
  team: {},
  challenges: [],
  store: undefined,
  challengeSorting: ['timestamp:desc'],
  sortedChallenges: Ember.computed.sort('challenges', 'challengeSorting'),
  setChallenges: function(){
    var challengeTimestamps = this.get('team.solves');
    var store = this.get('store');

    if(challengeTimestamps){
      var t = this;
      this.get('ctf.challengeboard').then(function(){
        var challenges = [];

        for (var i = 0; i < challengeTimestamps.length; i++) {
          var id = challengeTimestamps[i][0];
          var time = new Date(challengeTimestamps[i][1] * 1000);
          var foundChallenge = store.peekRecord('challenge', id);

          if(foundChallenge){
            var foundCategory = store.peekRecord('category', foundChallenge.get('category').id);
            if(foundCategory){
              var challenge = {
                title: foundChallenge.get('title'),
                points: foundChallenge.get('points'),
                category: foundCategory.get('name'),
                timestamp: time.toUTCString()
              };
              challenges.push(challenge);
            }
          }
        }
        challenges = Ember.A(challenges);
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
