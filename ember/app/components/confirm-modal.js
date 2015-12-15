import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isConfirm', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  actions: {
    closeConfirmModal: function() {
      this.set('modal.isConfirm', false);
    },
  },
});
