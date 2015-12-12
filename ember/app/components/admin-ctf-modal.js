import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
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

    },
    submitRegister: function() {
      var email = this.get('email');
      var username = this.get('username');
      var teamname = this.get('teamname');
      var password = this.get('password');
      var confirmpassword = this.get('confirmPassword');
      this.sendAction('sendRegister', {'email': email, 'username': username, 'teamname': teamname, 'password': password, 'confirmPassword': confirmpassword });
    },
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
    closeAdminCtfModal: function() {
      this.set('modal.isAdminCtf', false);
    },
  },
});
