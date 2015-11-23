import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: null,
  validatorController: null,
  ctf: null,
  user: {},
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

    // Update ctf model data every 5 minutes
    var interval = 1000 * 60 * 5;
    var modelReload = function() {
      reloadModels(this.get('ctf'));
      Ember.run.later(this, modelReload, interval);
    };
    Ember.run.later(this, modelReload, interval);
  },
  actions: {
    login: function(authenticationData) {
      var t = this;
      var auth = t.get('authController');

      // Attempt to login the team
      auth.login(authenticationData, function(success){
        // If there was no error during authentication close the login modal 
        if(success){
          t.set('modal.isLogin', false);
          
          var team = t.store.findRecord('team', auth.user.team_id);
          t.set('user', auth.user);
          t.set('user.team', team);
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
          t.set('user', auth.user);
          t.set('modal.isRegister', false);
        }
      });
    },
    logout: function() {
      this.set('user', {});
      this.get('authController').logout();
    },
    openLoginModal: function() {
      this.set('modal.isLogin', true);
    },
    openRegisterModal: function() {
      this.set('modal.isRegister', true);
    },
  }
});
