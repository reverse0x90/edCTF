import Ember from 'ember';

export default Ember.Controller.extend({
  challenge: '',
  isShowingChallengeModal: false,
  actions: {
      openChallenge: function(challenge_id) {
        this.set('challenge', this.store.find('challenge', challenge_id)),
        this.set('isShowingChallengeModal', true)
    },
  }
});
