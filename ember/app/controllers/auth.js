import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  remember: false,
  currentTransition: null,
  errorMessage: '',
  errorFields:{},
  validator: Ember.inject.controller('validator'),
  whiteList: ['index', 'scoreboard', 'about', 'home'],
  user: {},
  inwhiteList: function(string){
    if ( this.get('whiteList').indexOf(string)>=0 ) {
      return true;
    }
    else {
      return false;
    }
  },
  checkLoggedIn: function(callback){
    if(this.get('isAuthenticated')){
      callback(true)
    } else {
      var t = this;
      var namespace = t.store.adapterFor('application').namespace;
      Ember.$.get(namespace+'/session', function(data){
        if(data.success){
          if(data.team){
            var user = {
              'team_id': data.team,
              'team': t.store.findRecord('team', data.team),
            };
            t.set('user', user);
          }
          t.set('isAuthenticated', true);
          callback(true);
        } else {
          callback(false);
        }
      });
    }
  },
  isRemembered: function(){
    //if (localStorage.getItem('isAuthenticated') === 'true') {
    //  this.set('isAuthenticated', true);
    //}
    return this.get('isAuthenticated');
  },
  login: function(credentials, callback){
    var t = this;
    var currentTransition = t.get('currentTransition');
    var validator = this.get('validator');

    // Make sure the form is valid
    if (!validator.isvalidLogin(credentials)) {
      t.set('errorMessage', validator.get('error'));
      t.set('errorFields', validator.get('errorFields'));
      callback(false);
    }
    // Form is valid clear the error message field and authenticate the team
    else {
      var data = {
        'username': credentials.teamName,
        'password': credentials.password,
      };
      
      // Server communication
      var namespace = this.store.adapterFor('application').namespace;
      Ember.$.post(namespace+'/session', data, function(data){
        if(data.success){
          var user = {
            'team_id': data.team,
            'team': null,
          };
          t.set('user', user);
          
          // Set is authenticated to true
          t.set('isAuthenticated', true);

          // If the user clicked the remember me check box set is auth in local storage
          if (credentials.rememberMe === true) {
            localStorage.setItem("isAuthenticated", true); 
          }

          // If the the user was redirected to authenticate send them to the page they originally requested
          if ( currentTransition ) {
            t.set('currentTransition', null);
            currentTransition.retry();
          }
          t.set('errorMessage', '');
          t.set('errorFields', {});
          callback(true);
        } else {
          validator.invalidLogin();
          t.set('errorMessage', validator.get('error'));
          t.set('errorFields', validator.get('errorFields'));
          callback(false);
        }
      }).error(function() {
        validator.invalidLogin();
        t.set('errorMessage', validator.get('error'));
        t.set('errorFields', validator.get('errorFields'));
        callback(false);
      });
    }
  },
  register: function(registrationData){
    var t = this;
    var validator = this.get('validator');
    var authenticationData = {};

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

    // Send logout request to server
    var namespace = this.store.adapterFor('application').namespace;
    Ember.$.ajax({url: namespace+'/session',type: 'DELETE'});

    // Redirect to the home page
    this.transitionToRoute('application');
  },
});