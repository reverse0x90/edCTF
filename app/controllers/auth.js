import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  login: function(credentials){
    // Do the authentication stuff here
    credentials = null;
    this.set('isAuthenticated', true);
  },
  logout: function(){
    // Do the authentication stuff here
    this.set('isAuthenticated', false);
  },
});