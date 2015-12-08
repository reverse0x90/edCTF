import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  session: {},
  sortedChallengeboard: {},
  resetSolvedToggle: false,
  setSolvedChallenges: function(){
    var solves = this.get('session.team.solves');

    // Updated issolved for all challenges
    if(solves){
      var challenges = this.store.peekAll('challenge');
      if(challenges){
        challenges.forEach(function(challenge){
          var challenge_id = challenge.get('id');
          var found = solves.find(function(item){
            // '1' == 1 ==> true
            if(Number(challenge_id) === Number(item[0])){
              return true;
            }
            return false;
          });
          if(found || found === 0){
            challenge.set('issolved', true);
          } else {
            challenge.set('issolved', false);
          }
        });
      }
    }
  }.observes('ctf.challengeboard.categories', 'session', 'resetSolvedToggle'),
  setSolvedChallenge: function(){
    // Add new challenge to solved if it exists
    var chall_id = Number(this.get('modal.solvedChallenge'));
    if (chall_id || chall_id === 0){
      var challenge = this.store.peekRecord('challenge', chall_id);
      if (challenge){
        var points = this.get('session.team.points');
        if (points) {
          this.set('session.team.points', points+challenge.get('points'));
        }
        challenge.set('numsolved', challenge.get('numsolved') + 1);
      }
      
      var solves = this.get('session.team.solves');
      if (solves){
        var timestamp = [chall_id, Date.now() / 1000 | 0];
        solves.addObject(timestamp);
      }
      this.set('modal.solvedChallenge', -1);
      this.toggleProperty('resetSolvedToggle');
    }
  }.observes('modal.solvedChallenge'),
  actions: {
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openChallenge: function(id) {
      this.store.find('challenge', id).then((challenge) => {
        this.set('modal.challenge', challenge);
      });
      this.set('modal.isChallenge', true);
    },
  }
});