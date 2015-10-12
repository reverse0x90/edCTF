import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  teamname: '',
  password: '',
  classNames: ['login-box-margin'],
  setupFocus: function() {
    Ember.$('#inputTeamName').focus()
  }.on('didInsertElement'),
  actions: {
    submitLogin: function() {
      var teamname = this.get('teamname');
      var password = this.get('password');
      this.sendAction('login', {'teamname': teamname, 'password': password });
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
