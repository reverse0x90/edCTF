import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  errorMessage: '',
  errorFields: {},
  actions: {
    openAdminCtfModal: function() {
      this.set('modal.isAdminCtf', true);
    },
  },
});
