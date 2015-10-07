import Ember from 'ember';

export default Ember.Component.extend({
  isShowingLoginModal: false,
  isShowingRegisterModal: false,
  actions: {
    toggleLoginModal: function() {
      this.toggleProperty('isShowingLoginModal');
    },
    toggleRegisterModal: function() {
      this.toggleProperty('isShowingRegisterModal');
    },
    toggleLoginRegisterModals: function(){
        this.toggleProperty('isShowingLoginModal');
        this.toggleProperty('isShowingRegisterModal');
    },
  }
});
