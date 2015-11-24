import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: null,
  teamname: '',
  password: '',
  rememberMe: false,
  classNames: ['login-box-margin'],
  setupFocus: function() {
    Ember.$('#inputteamname').focus();
  }.on('didInsertElement'),
  actions: {
    submitLogin: function() {
      var teamname = this.get('teamname');
      var password = this.get('password');
      var rememberMe = this.get('rememberMe');
      this.sendAction('sendLogin', {'teamname': teamname, 'password': password, 'rememberMe': rememberMe});
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    closeLoginModal: function() {
      this.set('modal.isLogin', false);
      this.get('authController').set('errorMessage', '');
      this.get('authController').set('errorFields', {});
    },
    loginToRegisterModal: function(){
      this.set('modal.isLogin', false);
      this.set('modal.isRegister', true);
      this.get('authController').set('errorMessage', '');
      this.get('authController').set('errorFields', {});
    },
  }
});
