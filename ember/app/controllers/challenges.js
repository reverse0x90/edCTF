import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  session: {},
  sortedChallengeboard: {},
  setSolvedChallenges: function(){
    // Add new challenge to solved if it exists
    var chall_id = this.get('modal.solvedChallenge');
    if (chall_id || chall_id === 0){
      var challenge = this.store.peekRecord('challenge', chall_id);
      if (challenge){
        var points = this.get('session.team.points');
        if (points) {
          this.set('session.team.points', points+challenge.get('points'));
        }
      }
      
      var usersolved = this.get('session.team.solves');
      if (usersolved){
        var timestamp = [chall_id, Date.now() / 1000 | 0];
        usersolved.addObject(timestamp);
      }
      this.set('modal.solvedChallenge', false);
    }

    // Updated isSolved for all challenges
    var solves = this.get('session.team.solves');
    if(solves){
      var challenges = this.store.peekAll('challenge');
      if(challenges){
        var teamSolves = [];
        var teamSolvesTuples = solves.toArray();
        for(var i = 0;i < teamSolvesTuples.length; i++){
          teamSolves.push(teamSolvesTuples[i][0]);
        }
        challenges.forEach(function(challenge){
          var challenge_id = Number(challenge.get('id'));
          if(teamSolves.indexOf(challenge_id) > -1){
            challenge.set('isSolved', true);
          } else {
            challenge.set('isSolved', false);
          }
        });
      }
    }
  }.observes('ctf.challengeboard.categories', 'session', 'modal.solvedChallenge'),
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