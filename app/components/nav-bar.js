import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    openLoginModal: function() {
      this.set('isShowingLoginModal', true);
    },
    openRegisterModal: function() {
      this.set('isShowingRegisterModal', true);
    },
  }
});
