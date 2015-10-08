import Ember from 'ember';

export default Ember.Component.extend({
  isShowingChallengeModal: false,
  challengeCategory: 'Category',
  challengePoints: 100,
  challengeTitle: 'Title',
  challengeDescription: 'This is the challenge description.',
  actions: {
    openChallengeModal: function() {
      this.set('isShowingChallengeModal', true);
    },
    closeChallengeModal: function() {
      this.set('isShowingChallengeModal', false);
    },
  }
});
