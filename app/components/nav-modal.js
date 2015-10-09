import Ember from 'ember';

export default Ember.Component.extend({
  actions: {
    login: function(authenticationData) {
      // Pass the authentication data up
      this.sendAction('login', authenticationData);
    },
  }
});

