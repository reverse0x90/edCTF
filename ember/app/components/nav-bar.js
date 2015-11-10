import Ember from 'ember';

export default Ember.Component.extend({
  ctf: {},
  modal: {},
  authController: null,
  actions: {
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
    openLogoutModal: function(){
      this.set('modal.isLogout', true);
    },
    openProfileModal: function(){
      this.set('modal.isProfile', true);
    },
    sendLogout: function(){
      this.sendAction('logout');
    },
  }
});
