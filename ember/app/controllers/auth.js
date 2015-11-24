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
  session: {
    isAuthenticated: false,
    username: null,
    email: null,
    team: null,
  },
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
      callback(true);
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
      var loginData = {
        'username': credentials.teamName,
        'password': credentials.password,
      };
      
      // Server communication
      var namespace = this.store.adapterFor('application').namespace;
      Ember.$.post(namespace+'/session', loginData, function(response){
        if(response.success){
          var user = {
            'team_id': response.team,
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
  register: function(registrationData, callback){
    var t = this;
    var validator = this.get('validator');

    // Make sure the form is valid
    if (!validator.isvalidRegister(registrationData)) {
      this.set('errorMessage', validator.get('error'));
      this.set('errorFields', validator.get('errorFields'));
      callback();
    }
    // Form is valid clear the error message field and register and login the team 
    else {
      var team = {
        email: registrationData.email,
        username: registrationData.username,
        teamname: registrationData.username,
        password: registrationData.password
      };

      var namespace = this.store.adapterFor('application').namespace;
      Ember.$.ajax({
        url: namespace+'/teams',
        type: 'POST',
        data: JSON.stringify(team),
        dataType: 'json',
        ontentType: 'application/json; charset=UTF-8',
        success: function (result) {
          var session = t.get('session');

          if(result.error){
            session.isAuthenticated = result.isauthenticated || false;
            t.set('errorMessage', result.error);
            if(result.errorfields){
              if(result.errorfields.username){
                t.set('errorFields', {'teamName': true});
              }
              if(result.errorfields.email){
                t.set('errorFields', {'teamEmail': true});
              }
              if(result.errorfields.teamname){
                t.set('errorFields', {'teamName': true});
              }
            }
          } else {
            t.set('errorMessage', '');
            t.set('errorFields', {});
            if(result.isauthenticated){
              session.isAuthenticated = true;
              session.username = result.username;
              session.email = result.email;
              session.team = t.store.findRecord('team', result.team);
            } else {
              session.isAuthenticated = false;
            }
          }
          registrationData = null;
          callback();
        },
        error: function (xhr, ajaxOptions, thrownError) {
          console.log('ERROR: ', xhr, ajaxOptions, thrownError);
          t.set('errorMessage', 'Server error');
          t.set('errorFields', {});
          callback();
        }
      });
    }
  },
  logout: function(){
    // Send logout request to server
    var namespace = this.store.adapterFor('application').namespace;
    Ember.$.ajax({url: namespace+'/session',type: 'DELETE'});

    // Do the deauthentication stuff here
    this.set('user', {});
    this.set('isAuthenticated', false);
    localStorage.removeItem('isAuthenticated');
    

    // Redirect to the home page
    this.transitionToRoute('home');
  },
});