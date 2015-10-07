import Ember from 'ember';

export default Ember.Controller.extend({
  isShowingLoginModal: false,
  actions: {
    toggleLoginModal: function() {
      this.toggleProperty('isShowingLoginModal');
    }
  }
});
