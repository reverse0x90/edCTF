import Ember from 'ember';

export default Ember.Controller.extend({
  applicationController: Ember.inject.controller('application'),
<<<<<<< HEAD
  challenge: 'challenge string',
=======
>>>>>>> e60b50d5f7fdbf86e8229e5fe428999d4f26389c
  isShowingChallengeModal: false,
  actions: {
    openLoginModal: function() {
      this.get('applicationController').set('isShowingLoginModal', true);
    },
    openChallenge: function(challenge_id) {
        this.set('challenge', this.store.find('challenge', challenge_id));
        this.set('isShowingChallengeModal', true);
    },
  }
});
