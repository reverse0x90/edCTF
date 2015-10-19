import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  actions: {
    closeProfileModal: function() {
      this.set('modal.isProfile', false);
    },
  },
});
