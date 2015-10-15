import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  currentTransition: null,
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
    var currentTransition = this.get('currentTransition');
    credentials = null;
    t.set('isAuthenticated', true);
    if ( currentTransition ) {
      console.log("redirecting to: ", currentTransition.targetName)
      t.set('currentTransition', null) 
      currentTransition.retry();
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