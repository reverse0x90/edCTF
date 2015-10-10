import Ember from 'ember';

export default Ember.Component.extend({
  isShowingChallengeModal: false,
  actions: {
    openChallengeModal: function() {
      this.set('isShowingChallengeModal', true);
    },
    closeChallengeModal: function() {
      this.set('isShowingChallengeModal', false);
    },
  }
});
