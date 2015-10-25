import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: undefined,
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
      this.get('authController').set('errorMessage', '');
      this.get('authController').set('errorFields', {});
    },
    registerToLoginModal: function(){
      this.set('modal.isRegister', false);
      this.set('modal.isLogin', true);
      this.get('authController').set('errorMessage', '');
      this.get('authController').set('errorFields', {});
    },
  }
});