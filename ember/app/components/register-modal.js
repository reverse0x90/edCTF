import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  authController: null,
  email: '',
  teamname: '',
  password: '',
  confirmPassword: '',
  closeModal: function(){
    var t = this;
    return function(callback){
      t.get('authController').set('errorMessage', '');
      t.get('authController').set('errorFields', {});
      t.set('modal.isRegister', false);
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
    Ember.$('#inputEmail').focus();
  }.on('didInsertElement'),
  actions: {
    submitRegister: function() {
      var email = this.get('email');
      var username = this.get('username');
      var teamname = this.get('teamname');
      var password = this.get('password');
      var confirmpassword = this.get('confirmPassword');
      this.sendAction('sendRegister', {'email': email, 'username': username, 'teamname': teamname, 'password': password, 'confirmPassword': confirmpassword });
    },
    closeRegisterModal: function() {
      this.get('closeModal')();
    },
    registerToLoginModal: function(){
      var t = this;
      this.get('closeModal')(function(){
        t.set('modal.isLogin', true);
      });
    },
  },
});