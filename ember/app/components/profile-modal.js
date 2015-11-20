import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  user: {},
  actions: {
    closeProfileModal: function() {
      this.set('modal.isProfile', false);
    },
  },
});
