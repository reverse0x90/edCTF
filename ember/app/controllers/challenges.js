import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  ctf: null,
  user: {},
  isSolved: function (challengeID) {
    var solved = this.get('user');

    console.log("solved: ", solved);
    
  }
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