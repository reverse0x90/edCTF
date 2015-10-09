import Ember from 'ember';

export default Ember.Route.extend({
  isAuthenticated: false,
  actions: {
    login: function(authenticationData) {
      this.set('isAuthenticated', authenticationData);
      console.log('isAuthenticated: ', this.get('isAuthenticated'));
    },
  }
});
