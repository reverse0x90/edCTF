import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  username: '',
  remember: false,
  currentTransition: null,
  errorMessage: '',
  validator: Ember.inject.controller('validator'),
  whiteList: ['index', 'scoreboard', 'about'],
  inwhiteList: function(string){
    // Do the authentication stuff here
    if ( this.get('whiteList').indexOf(string)>=0 ) {
      return true;
    }
    else {
      return false;
    }
  },
  login: function(credentials){
    var t = this;
    var currentTransition = t.get('currentTransition');
    var validator = this.get('validator');

    // Make sure the form is valid
    if (!validator.isvalidLogin(credentials)) {
      t.set('errorMessage', validator.get('error'));
    }
    // Form is value clear the error message field and authenticate the team
    else {
      t.set('errorMessage', '');
      credentials = null;
      t.set('isAuthenticated', true);
      // If the the user was redirected to authenticate send them to the page they originally requested
      if ( currentTransition ) {
        t.set('currentTransition', null);
        currentTransition.retry();
      }
    }
  },
  register: function(registrationData){
    // Do the registration stuff here
    registrationData = null;
  },
  logout: function(){
    // Do the authentication stuff here
    this.set('isAuthenticated', false);
  },
});