import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  classNames: ['login-box-margin'],
  actions: {
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
    closeRegisterModal: function() {
      this.set('modal.isRegister', false);
    },
    registerToLoginModal: function(){
        this.set('modal.isRegister', false);
        this.set('modal.isLogin', true);
    },
  }
});