import Ember from 'ember';

export default Ember.Controller.extend({
  isAuthenticated: false,
  remember: false,
  currentTransition: null,
  errorMessage: '',
  errorFields:{},
  validator: Ember.inject.controller('validator'),
  whiteList: ['index', 'scoreboard', 'about', 'home', '404'],
  blackList: [/challenges/, /admin/, /admin(\/.*)/],
  session: {
    'isAuthenticated': false,
    'username': null,
    'email': null,
    'team': null,
    'isAdmin': false,
  },
  inwhiteList: function(string){
    if ( this.get('whiteList').indexOf(string)>=0 ) {
      return true;
    }
    else {
      return false;
    }
  },
  inblackList: function(string){
    var blackList = this.get('blackList');
    for (var i=0; i < blackList.length; i++) {
      var res = blackList[i].exec(string);
      if(res){
        return true;
      }
    }
    return false;
  },
  checkLoggedIn: function(callback){
    if(this.get('session.isAuthenticated')){
      callback();
    } else {
      var t = this;
      var namespace = t.store.adapterFor('application').namespace;
      Ember.$.ajax({
        url: namespace+'/session',
        type: 'GET',
        success: function (result){
          var session = {};
          if(result.isauthenticated){
            session.isAuthenticated = true;
            session.username = result.username;
            session.email = result.email;
            session.isAdmin = result.isadmin;
            if(result.team === null){
              session.team = null;
            } else {
              session.team = t.store.findRecord('team', result.team);
            }
          } else {
            session.isAuthenticated = false;
          }
          t.set('session', session);
          callback();
        }, error: function () {
          callback();
        },
      });
    }
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
        'username': credentials.teamname,
        'password': credentials.password,
      };
      
      // Server communication
      var namespace = this.store.adapterFor('application').namespace;
      Ember.$.ajax({
        url: namespace+'/session',
        type: 'POST',
        data: JSON.stringify(loginData),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        crossDomain:false,
        processData: false,
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", Ember.$.cookie('csrftoken'));
        },
        success: function (result){
          var session = {};
          if(result.error){
            session.isAuthenticated = result.isauthenticated || false;
            t.set('errorMessage', result.error);
            t.set('errorFields', {'teamname': true, 'password': true});
          } else {
            t.set('errorMessage', '');
            t.set('errorFields', {});
            if(result.isauthenticated){
              session.isAuthenticated = true;
              session.username = result.username;
              session.email = result.email;
              session.isAdmin = result.isadmin;
              if(result.team === null){
                session.team = null;
              } else {
                session.team = t.store.findRecord('team', result.team);
              }
            } else {
              session.isAuthenticated = false;
            }

            // If the the user was redirected to authenticate send them to the page they originally requested
            if(currentTransition){
              t.set('currentTransition', null);
              currentTransition.retry();
            }
          }
          t.set('session', session);
          callback();
        },
        error: function () {
          validator.invalidLogin();
          t.set('errorMessage', validator.get('error'));
          t.set('errorFields', validator.get('errorFields'));
          callback();
        },
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
        teamname: registrationData.teamname,
        password: registrationData.password
      };

      var namespace = this.store.adapterFor('application').namespace;
      Ember.$.ajax({
        url: namespace+'/teams',
        type: 'POST',
        data: JSON.stringify(team),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        crossDomain:false,
        processData: false,
        beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", Ember.$.cookie('csrftoken'));
        },
        success: function (result) {
          var session = {};
          if(result.error){
            t.set('errorMessage', result.error);
            session.isAuthenticated = result.isauthenticated || false;
            if(result.errorfields){
              t.set('errorFields', {
                'username': result.errorfields.username || false,
                'email': result.errorfields.email || false,
                'teamname': result.errorfields.teamname || false,
                'password': result.errorfields.password || false,
                'confirmPassword': result.errorfields.password || false,
              });
            } else {
              t.set('errorFields', {});
            }
          } else {
            t.set('errorMessage', '');
            t.set('errorFields', {});
            if(result.isauthenticated){
              session.isAuthenticated = true;
              session.username = result.username;
              session.email = result.email;
              session.isAdmin = result.isadmin;
              if(result.team === null){
                session.team = null;
              } else {
                session.team = t.store.findRecord('team', result.team);
              }
            } else {
              session.isAuthenticated = false;
            }
          }
          registrationData = null;
          t.set('session', session);
          callback();
        },
        error: function () {
          t.set('errorMessage', 'Server error');
          t.set('errorFields', {});
          callback();
        }
      });
    }
  },
  logout: function(callback){
    // Send logout request to server
    var t = this;
    var namespace = this.store.adapterFor('application').namespace;

    Ember.$.ajax({
      url: namespace+'/session',
      type: 'DELETE',
      crossDomain:false,
      beforeSend: function(xhr) {
          xhr.setRequestHeader("X-CSRFToken", Ember.$.cookie('csrftoken'));
        },
      success: function(){
        // Do the deauthentication
        t.set('session', {'isAuthenticated': false});
        callback();
      },
      error: function () {
        // Set isAuthenticated to false regardless
        t.set('session', {'isAuthenticated': false});
        callback();
      }
    });
  },
});