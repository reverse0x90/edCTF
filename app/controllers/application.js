import Ember from 'ember';

export default Ember.Controller.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  authcontroller: null,
  actions: {
    getLoginCredentials: function(authenticationData) {
      this.get('authcontroller').login(authenticationData)
    },
    openLoginModal: function() {
      this.set('isShowingLoginModal', true);
      
    },
    openRegisterModal: function() {
      this.set('isShowingRegisterModal', true);
    },
  }
});
