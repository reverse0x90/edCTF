import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    openRegisterModal: function() {
      this.set('isShowingRegisterModal', true);
    },
    closeRegisterModal: function() {
      this.set('isShowingRegisterModal', false);
    },
    registerToLoginModal: function(){
        this.set('isShowingRegisterModal', false);
        this.set('isShowingLoginModal', true);
    },
  }
});