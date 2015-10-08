import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
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
