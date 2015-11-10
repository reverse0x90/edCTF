import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  user: {},
  checkIfSolved: function(){
    var challenge_id = this.get('modal.solvedChallenge');
    if (challenge_id !== false){
      this.get('user.team.solved').addObject(challenge_id);
      this.set('modal.solvedChallenge', false);
      // figure out how to refresh the route here
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