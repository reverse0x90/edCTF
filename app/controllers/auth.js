import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  login: function(credentials){
      // Do the authentication stuff here
      this.set('isAuthenticated', true);
    },
  });