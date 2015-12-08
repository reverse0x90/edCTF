import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  actions: {
    closeLogoutModal: function() {
      this.sendAction('logout');
      this.set('modal.isLogout', false);
    },
  }
});
