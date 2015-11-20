import Ember from 'ember';

export default Ember.Component.extend({
  modal: {},
  actions: {
    closeTeamModal: function() {
      this.set('modal.isTeam', false);
    },
  },
});
