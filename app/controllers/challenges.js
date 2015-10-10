import Ember from 'ember';

export default Ember.Controller.extend({
  applicationController: Ember.inject.controller('application'),
  challenge: 'challenge string',
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
