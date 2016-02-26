import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: null,
  teamname: '',
  password: '',
  rememberMe: false,
  classNames: ['login-box-margin'],
  setupKeys: function() {
    Ember.$('body').on('keyup.modal-dialog', (e) => {
      if (e.keyCode === 27) {
        this.set('modal.isLogin', false);
      }
    });
  }.on('didInsertElement'),
  teardownKeys: function() {
    Ember.$('body').off('keyup.modal-dialog');
  }.on('willDestroyElement'),
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
