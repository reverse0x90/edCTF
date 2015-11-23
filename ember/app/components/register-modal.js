import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: null,
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
      var email = this.get('teamEmail');
      var username = this.get('teamName');
      var teamname = this.get('teamName');
      var password = this.get('password');
      var confirmpassword = this.get('confirmPassword');
      this.sendAction('sendRegister', {'email': email, 'username': username, 'teamName': teamname, 'password': password, 'confirmPassword': confirmpassword });
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