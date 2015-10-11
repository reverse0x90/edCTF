import Ember from 'ember';

export default Ember.Component.extend({
  challenge: {},
  modal: {},
  classNames: ['challenge-submit', 'challenge-cancel'],
  setup: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      console.log(e.keyCode);
      if (e.keyCode === 27) {
        this.set('modal.isChallenge', false);
      }
    });
  }.on('didInsertElement'),
  teardown: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  actions: {
    closeChallengeModal: function() {
      this.set('modal.isChallenge', false);
    },
    submitFlag: function() {
      console.log('From was submitted');
    },
  }
});

