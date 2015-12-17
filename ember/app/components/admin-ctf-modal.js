import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  ctfController: null,
  live: true,
  name: '',
  closeModal: function(){
    var t = this;
    return function(callback){
      t.set('modal.isAdminCtf', false);
      t.set('name', '');
      t.set('live', true);
      t.set('ctfController.modalErrorMessage', '');
      t.set('ctfController.modalErrorFields', {});
      if(callback){
        callback();
      }
    };
  }.property('closeModal'),
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.get('closeModal')();
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
      this.get('closeModal')();
    },
  },
});
