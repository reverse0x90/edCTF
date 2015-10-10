import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  actions: {
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
       this.set('modal.isRegister', true);
    },
  }
});
