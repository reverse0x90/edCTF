import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  teamEmail: '',
  teamName: '',
  password: '',
  confirmPassword: '',
  classNames: ['login-box-margin'],
  setupFocus: function() {
    Ember.$('#inputEmail').focus();
  }.on('didInsertElement'),
  actions: {
  submitRegister: function() {
      var teamEmail = this.get('teamEmail');
      var teamName = this.get('teamName');
      var password = this.get('password');
      var confirmPassword = this.get('confirmPassword');
      this.sendAction('sendRegister', {'teamEmail': teamEmail, 'teamName': teamName, 'password': password, 'confirmPassword': confirmPassword });
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
    closeRegisterModal: function() {
      this.set('modal.isRegister', false);
    },
    registerToLoginModal: function(){
        this.set('modal.isRegister', false);
        this.set('modal.isLogin', true);
    },
  }
});