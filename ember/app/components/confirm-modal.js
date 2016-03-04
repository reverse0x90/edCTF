import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  message: '',
  callback: null,
  confirmed: false,
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
    confirmationDeny: function(){
      this.set('modal.isConfirm', false);
      var callback = this.get('callback');
      if(callback){
        callback(false);
      }
    },
    confirmationAllow: function(){
      this.set('modal.isConfirm', false);
      var callback = this.get('callback');
      if(callback){
        callback(true);
      }
    },
  },
});
