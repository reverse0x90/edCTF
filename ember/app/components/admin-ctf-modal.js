import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  ctfController: null,
  online: true,
  name: '',
  
  closeModal: function(){
    const t = this;
    return function(callback){
      t.set('modal.isAdminCtf', false);
      t.set('name', '');
      t.set('online', true);
      t.set('modal.errorMessage', '');
      t.set('modal.errorFields', {});
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
      const name = this.get('name');
      const online = this.get('online');
      this.get('ctfController').send('createCtf', name, online);
    },
    closeAdminCtfModal: function() {
      this.get('closeModal')();
    },
  },
});
