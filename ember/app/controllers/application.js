import Ember from 'ember';

export default Ember.Controller.extend({
  modal: {},
  authController: null,
  validatorController: null,
  ctf: null,
  user: {},
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
      auth.login(authenticationData);
      // If there was no error during authentication close the login modal 
      if (!auth.get('errorMessage')) {
        this.set('user', auth.user);
        this.set('modal.isLogin', false);
      }
    },
    register: function(registrationData) {
      var t = this;
      var auth = t.get('authController');
      
      // Attempt to register the team
      auth.register(registrationData);

      // If there was no error during registration close the register modal 
      if (!auth.get('errorMessage')) {
        this.set('user', auth.user);
        this.set('modal.isRegister', false);
      }
      
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
