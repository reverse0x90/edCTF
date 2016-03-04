import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: null,
  adminController: null,
  validatorController: null,
  adminSettings: {},
  ctf: null,
  session: {
    'isAuthenticated': false,
  },
  updateTitle: function() {
    Ember.$(document).attr('title', this.get('ctf.name'));
  }.observes('ctf.name'),
  init: function(){
    this._super();

    // Function to reload async models (currently ember doesn't support this well)
    var reloadModels = function(parentRecord) {
      parentRecord.reload();
      parentRecord.eachRelationship(function(childRecord, childRelation){
        if (childRelation.options && childRelation.options.async){
          var id = parseInt(parentRecord.toJSON()[childRecord]);
          var foundRecord = parentRecord.store.peekRecord(childRecord, id);
          if (foundRecord){
            foundRecord.reload();
          }
        }
      });
    };

    // Update ctf model data every 30 seconds
    var interval = 1000 * 30 * 1;
    var modelReload = function() {
      var online_ctf = this.get('ctf');
      if (online_ctf){
        reloadModels(online_ctf);
      }
      Ember.run.later(this, modelReload, interval);
    };
    Ember.run.later(this, modelReload, interval);
  },
  actions: {
    login: function(authenticationData) {
      var t = this;
      var auth = t.get('authController');

      // Attempt to login the team
      auth.login(authenticationData, function(){
        // If there was no error during authentication close the login modal 
        if(!auth.get('errorMessage')){
          t.set('session', auth.session);
          t.set('modal.isLogin', false);
        }
      });
    },
    register: function(registrationData) {
      var t = this;
      var auth = this.get('authController');
      
      // Attempt to register the team
      auth.register(registrationData, function(){
        // If there was no error during registration close the register modal 
        if (!auth.get('errorMessage')) {
          t.set('session', auth.session);
          t.set('modal.isRegister', false);
        }
      });
    },
    submitFlag: function(challengeid, flag, callback) {
      var flagData = {
        'flag': {
          'key': flag,
        },
      };
      var namespace = this.get('store').adapterFor('application').namespace;
      Ember.$.ajax({
        url: namespace+'/flags/'+challengeid,
        type: 'POST',
        data: JSON.stringify(flagData),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        crossDomain:false,
        processData: false,
        beforeSend: function(xhr) {
          xhr.setRequestHeader('X-CSRFToken', Ember.$.cookie('csrftoken'));
        },
        success: function (result){
          console.log(result);
          callback(true, result);
        }, error: function (err) {
          var error = '';
          if(err.responseJSON.errors){
            error = err.responseJSON.errors.message;
          }
          if(!error){
            error = 'Something went wrong';
          }
          callback(false, error);
        },
      });
    },
    logout: function() {
      var t = this;
      var auth = this.get('authController');

      // Attempt to logout
      auth.logout(function(){
        t.set('session', auth.session);

        // Redirect to the home page
        t.transitionToRoute('home');
      });
    },
    editProfile: function(session, password, confirmPassword){
      if(!session.team){
        this.set('modal.errorFields', {});
        this.set('modal.errorMessage', 'User has no team');
        return;
      }

      var t = this;
      var team = session.team;
      team.then(function(team){
        if(!team.get('teamname')){
          t.set('modal.errorFields', {'teamname': true});
          t.set('modal.errorMessage', 'Invalid team name');
          return;
        }

        if(!team.get('username')){
          t.set('modal.errorFields', {'username': true});
          t.set('modal.errorMessage', 'Invalid username');
          return;
        }

        if(!team.get('email')){
          t.set('modal.errorFields', {'email': true});
          t.set('modal.errorMessage', 'Invalid email');
          return;
        }

        if(password){
          if(((password).localeCompare(confirmPassword))){
            t.set('modal.errorFields', {'password': true});
            t.set('modal.errorMessage', 'Passwords not equal');
            return;
          } else{
            team.set('password', password);
          }
        }

        team.save().then(function(){
          t.send('closeProfileModal');
          team.set('password', undefined);
        }, function(err){
          team.rollbackAttributes();
          if (err.errors.message){
            t.set('modal.errorMessage', err.errors.message);
          } else {
            t.set('modal.errorMessage', 'Server error, unable to edit team');
          }
        });
      });
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
    closeProfileModal: function() {
      this.set('modal.isProfile', false);
    },
  }
});
