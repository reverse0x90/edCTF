import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: undefined,
  ctf: undefined,
  actions: {
    login: function(authenticationData) {
      var t = this;
      var auth = t.get('authController')

      // Attempt to login the team
      auth.login(authenticationData);
      // If there was no error during authentication close the login modal 
      if (!auth.get('errorMessage')) {
        this.set('modal.isLogin', false);
      }
    },
    register: function(registrationData) {
      var t = this;
      var auth = t.get('authController')
      
      // Attempt to register the team
      auth.register(registrationData);

      // If there was no error during registration close the register modal 
      if (!auth.get('errorMessage')) {
        this.set('modal.isRegister', false);
      }
      
    },
    logout: function(authenticationData) {
      this.get('authController').logout();
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
  }
});
