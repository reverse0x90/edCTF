import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    login: function() {
      // Do the authentication stuff here
      var authenticate = true;
      this.sendAction('login', authenticate);
    },
    openLoginModal: function() {
      this.set('isShowingLoginModal', true);
    },
    closeLoginModal: function() {
      this.set('isShowingLoginModal', false);
    },
    loginToRegisterModal: function(){
        this.set('isShowingLoginModal', false);
        this.set('isShowingRegisterModal', true);
    },
  }
});
