import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  title: '',
  points: 0,
  description: '',
  flag: '',
  challengeboardController: null,
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isAdminChallenge', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setupFocus: function() {
    Ember.$('#inputEmail').focus();
  }.on('didInsertElement'),
   actions: {
    closeAdminChallengeModal: function() {
      this.set('modal.adminCategory', null);
      this.set('modal.adminChallenge', null);
      this.set('modal.isAdminChallenge', false);
    },
    createChallenge: function() {
      var challenge = {
        category: this.get('modal.adminCategory'),
        title: this.get('title'),
        points: this.get('points'),
        description: this.get('description'),
        flag: this.get('flag'),
      };
      this.get('challengeboardController').send('createChallenge', challenge);
    },
  },
});
