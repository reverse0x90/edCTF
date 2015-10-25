import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  remember: false,
  currentTransition: null,
  errorMessage: '',
  errorFields:{},
  validator: Ember.inject.controller('validator'),
  whiteList: ['index', 'scoreboard', 'about'],
  user: {},
  inwhiteList: function(string){
    if ( this.get('whiteList').indexOf(string)>=0 ) {
      return true;
    }
    else {
      return false;
    }
  },
  isRemembered: function(){
    if (localStorage.getItem("isAuthenticated") == 'true') {
      this.set('isAuthenticated', true);
    }

    return this.get('isAuthenticated');
  },
  login: function(credentials){
    var t = this;
    var currentTransition = t.get('currentTransition');
    var validator = this.get('validator');

    // Make sure the form is valid
    if (!validator.isvalidLogin(credentials)) {
      t.set('errorMessage', validator.get('error'));
      t.set('errorFields', validator.get('errorFields'));
    }
    // Form is valid clear the error message field and authenticate the team
    else {
      t.set('errorMessage', '');
      t.set('errorFields', {});

      // Do server communication stuff..

      // Server will return somthing like this
      var user = {
        teamid: 1,
        teamName: 'team1',
        email: 'teamEmail@gmail.com',
        points: 975,
        correctFlags: 5,
        wrongFlags: 30,
        solved: ['Reversing localStorage.setItem("lastname", "Smith");783', 'Reversing 783', 'Reversing 783', 'Reversing 783', 'Reversing 783'],
      };
      t.set('user', user);

      // Set is authenticated to true
      t.set('isAuthenticated', true);

      // If the user clicked the remember me check box set is auth in local storage
      if (credentials.rememberMe == true) {
        localStorage.setItem("isAuthenticated", true); 
      }
        
      // If the the user was redirected to authenticate send them to the page they originally requested
      if ( currentTransition ) {
        t.set('currentTransition', null);
        currentTransition.retry();
      }
    }
  },
  register: function(registrationData){
    var t = this;
    var validator = this.get('validator');
    var authenticationData = {}

    // Make sure the form is valid
    if (!validator.isvalidRegister(registrationData)) {
      t.set('errorMessage', validator.get('error'));
      t.set('errorFields', validator.get('errorFields'));
    }
    // Form is valid clear the error message field and register and login the team 
    else {
      t.set('errorMessage', '');
      t.set('errorFields', {});
      authenticationData = {'teamName': registrationData.teamName, 'password': registrationData.password };
      registrationData = null;
      this.login(authenticationData);
    }
  },
  logout: function(){
    // Do the deauthentication stuff here
    this.set('user', {});
    this.set('isAuthenticated', false);
    localStorage.removeItem('isAuthenticated');

    // Redirect to the home page
    this.transitionToRoute('application');
  },
});