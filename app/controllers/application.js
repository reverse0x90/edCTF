import Ember from 'ember';

export default Ember.Controller.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    login: function(authenticationData) {
      // Pass the authentication data up
      this.sendAction('login', authenticationData);
    },
    openLoginModal: function() {
      this.set('isShowingLoginModal', true);
      
    },
    openRegisterModal: function() {
      this.set('isShowingRegisterModal', true);
    },
  }
});
