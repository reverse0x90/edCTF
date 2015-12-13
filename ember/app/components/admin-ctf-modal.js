import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  ctfController: null,
  live: true,
  name: '',
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isAdminCtf', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
  setupFocus: function() {
    Ember.$('#ctfName').focus();
  }.on('didInsertElement'),
   actions: {
    createCtf: function(){
      var name = this.get('name');
      var live = this.get('live');
      var createCtf = this.get('ctfController.create');
      createCtf(name, live);
    },
    closeAdminCtfModal: function() {
      this.set('modal.isAdminCtf', false);
      this.set('name', '');
      this.set('live', true);
      this.set('ctfController.errorMessage', '');
      this.set('ctfController.errorFields', {});
    },
  },
});
