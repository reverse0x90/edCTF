import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: undefined,
  ctf: undefined,
  init: function(){
     this._super();
     
    // update ctf model data every 5 minutes
    var interval = 1000 * 60 * 5;
    var modelReload = function() {
      this.get('ctf').reload();
      Ember.run.later(this, modelReload, interval);
    };
    Ember.run.later(this, modelReload, interval);
  },
  actions: {
    login: function(authenticationData) {
      var t = this;
      var auth = t.get('authController');

      // Attempt to login the team
      auth.login(authenticationData);
      // If there was no error during authentication close the login modal 
      if (!auth.get('errorMessage')) {
        this.set('modal.isLogin', false);
      }
    },
    register: function(registrationData) {
      var t = this;
      var auth = t.get('authController');
      
      // Attempt to register the team
      auth.register(registrationData);

      // If there was no error during registration close the register modal 
      if (!auth.get('errorMessage')) {
        this.set('modal.isRegister', false);
      }
      
    },
    logout: function() {
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
