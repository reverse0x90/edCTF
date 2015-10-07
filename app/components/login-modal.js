import Ember from 'ember';

export default Ember.Component.extend({
  actions: {
    toggleLoginModal: function() {
      this.toggleProperty('isShowingLoginModal');
    }
  }
});
