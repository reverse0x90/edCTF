import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: null,
  teamname: '',
  password: '',
  rememberMe: false,
  classNames: ['login-box-margin'],
  closeModal: function(){
    var t = this;
    return function(callback){
      t.get('authController').set('errorMessage', '');
      t.get('authController').set('errorFields', {});
      t.set('modal.isLogin', false);
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
    Ember.$('#inputteamname').focus();
  }.on('didInsertElement'),
  actions: {
    submitLogin: function() {
      var teamname = this.get('teamname');
      var password = this.get('password');
      var rememberMe = this.get('rememberMe');
      this.sendAction('sendLogin', {'teamname': teamname, 'password': password, 'rememberMe': rememberMe});
    },
    closeLoginModal: function() {
      this.get('closeModal')();
    },
    loginToRegisterModal: function(){
      var t = this;
      this.get('closeModal')(function(){
        t.set('modal.isRegister', true);
      });
    },
  }
});
