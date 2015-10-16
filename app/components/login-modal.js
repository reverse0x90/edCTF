import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: undefined,
  teamName: '',
  password: '',
  classNames: ['login-box-margin'],
  setupFocus: function() {
    Ember.$('#inputTeamName').focus();
  }.on('didInsertElement'),
  actions: {
    submitLogin: function() {
      var teamName = this.get('teamname');
      var password = this.get('password');
      this.sendAction('sendLogin', {'teamName': teamName, 'password': password });
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    closeLoginModal: function() {
      this.set('modal.isLogin', false);
    },
    loginToRegisterModal: function(){
        this.set('modal.isLogin', false);
        this.set('modal.isRegister', true);
    },
  }
});
